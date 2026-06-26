#!/usr/bin/env python3
"""Build a local full-text corpus index for the Neilization skill.

The generated corpus is intended for local use only. Do not commit `.corpus/`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote
from xml.etree import ElementTree as ET

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - used only on minimal Python installs
    BeautifulSoup = None


DEFAULT_SOURCE = Path("/Users/pc/Desktop/Neil degrasse Tyson")
DEFAULT_OUT = Path(".corpus")
SUPPORTED_EXTENSIONS = {".pdf", ".epub"}


@dataclass
class ExtractedSource:
    path: Path
    title: str
    file_type: str
    sha256: str
    byte_count: int
    extraction_method: str
    page_count: int | None
    chunks: list[dict]
    extracted_chars: int
    status: str
    warning: str


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def command_path(command: str) -> str | None:
    return shutil.which(command)


def require_command(command: str) -> str:
    found = command_path(command)
    if not found:
        fail(f"required command not found on PATH: {command}")
    return found


def run_command(command: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\f", "\n")
    text = text.replace("\x00", "")
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", clean_text(text)).strip()


def visible_chars(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def short_title(path: Path) -> str:
    return path.stem.strip()


def pdf_page_count(path: Path) -> int | None:
    if not command_path("pdfinfo"):
        return None
    result = run_command(["pdfinfo", str(path)], timeout=60)
    if result.returncode != 0:
        return None
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    return int(match.group(1)) if match else None


def pdftotext_pages(path: Path, page_count: int | None) -> list[str]:
    result = run_command(["pdftotext", "-layout", str(path), "-"], timeout=300)
    if result.returncode != 0:
        return []

    pages = result.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()

    if page_count:
        if len(pages) < page_count:
            pages.extend([""] * (page_count - len(pages)))
        elif len(pages) > page_count:
            pages = pages[:page_count]

    return [clean_text(page) for page in pages]


def should_ocr(
    pages: list[str],
    page_count: int | None,
    min_text_chars: int,
    min_page_chars: int,
) -> bool:
    if not pages:
        return True

    total = sum(visible_chars(page) for page in pages)
    counted_pages = page_count or len(pages)
    average = total / max(counted_pages, 1)
    sparse_pages = sum(1 for page in pages if visible_chars(page) < min_page_chars)
    sparse_ratio = sparse_pages / max(counted_pages, 1)

    return total < 250 or (total < min_text_chars and average < min_page_chars) or sparse_ratio > 0.75


def ocr_pdf_pages(path: Path, sha256: str, page_count: int, out_dir: Path, dpi: int) -> tuple[list[str], list[str]]:
    require_command("pdftoppm")
    require_command("tesseract")

    cache_dir = out_dir / "ocr-cache" / sha256[:16]
    cache_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []
    pages: list[str] = []

    for page_number in range(1, page_count + 1):
        cache_file = cache_dir / f"page-{page_number:04d}.txt"
        if cache_file.exists():
            pages.append(clean_text(cache_file.read_text(encoding="utf-8", errors="replace")))
            continue

        print(f"  OCR page {page_number}/{page_count}: {path.name}", flush=True)
        with tempfile.TemporaryDirectory(prefix="neil-ocr-") as temp_name:
            temp_dir = Path(temp_name)
            image_prefix = temp_dir / "page"
            render = run_command(
                [
                    "pdftoppm",
                    "-r",
                    str(dpi),
                    "-f",
                    str(page_number),
                    "-l",
                    str(page_number),
                    str(path),
                    str(image_prefix),
                ],
                timeout=180,
            )
            if render.returncode != 0:
                warnings.append(f"page {page_number}: pdftoppm failed")
                pages.append("")
                continue

            images = sorted(temp_dir.glob("page-*"))
            if not images:
                warnings.append(f"page {page_number}: no rendered image")
                pages.append("")
                continue

            ocr = run_command(
                ["tesseract", str(images[0]), "stdout", "-l", "eng", "--psm", "1"],
                timeout=180,
            )
            if ocr.returncode != 0:
                warnings.append(f"page {page_number}: tesseract failed")
                pages.append("")
                continue

            page_text = clean_text(ocr.stdout)
            cache_file.write_text(page_text, encoding="utf-8")
            pages.append(page_text)

    return pages, warnings


def split_long_text(text: str, max_chars: int, overlap: int) -> list[str]:
    text = compact_text(text)
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            search_start = start + int(max_chars * 0.65)
            candidates = [
                text.rfind(". ", search_start, end),
                text.rfind("? ", search_start, end),
                text.rfind("! ", search_start, end),
                text.rfind("; ", search_start, end),
            ]
            boundary = max(candidates)
            if boundary > start:
                end = boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)

    return chunks


def chunks_from_pages(pages: list[str], max_chars: int, overlap: int) -> list[dict]:
    chunks: list[dict] = []
    current: list[str] = []
    start_page: int | None = None
    end_page: int | None = None

    def flush() -> None:
        nonlocal current, start_page, end_page
        if not current or start_page is None or end_page is None:
            current = []
            start_page = None
            end_page = None
            return
        text = compact_text("\n\n".join(current))
        if text:
            locator = f"page {start_page}" if start_page == end_page else f"pages {start_page}-{end_page}"
            chunks.append(
                {
                    "locator": locator,
                    "page_start": start_page,
                    "page_end": end_page,
                    "text": text,
                }
            )
        current = []
        start_page = None
        end_page = None

    for index, page_text in enumerate(pages, start=1):
        text = compact_text(page_text)
        if not text:
            continue

        if len(text) > max_chars:
            flush()
            for part in split_long_text(text, max_chars, overlap):
                chunks.append(
                    {
                        "locator": f"page {index}",
                        "page_start": index,
                        "page_end": index,
                        "text": part,
                    }
                )
            continue

        pending_length = len(compact_text("\n\n".join([*current, text])))
        if current and pending_length > max_chars:
            flush()

        if start_page is None:
            start_page = index
        end_page = index
        current.append(text)

    flush()
    return chunks


def soup_text(html: str) -> tuple[str, str | None]:
    if BeautifulSoup is None:
        text = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        return clean_text(text), None

    soup = BeautifulSoup(html, "xml")
    for tag in soup(["script", "style", "nav"]):
        tag.decompose()
    heading = soup.find(["h1", "h2", "title"])
    heading_text = compact_text(heading.get_text(" ")) if heading else None
    return clean_text(soup.get_text("\n")), heading_text


def epub_item_paths(zip_file: zipfile.ZipFile) -> list[str]:
    try:
        container = ET.fromstring(zip_file.read("META-INF/container.xml"))
        rootfile = container.find(".//{*}rootfile")
        if rootfile is None:
            return []
        opf_path = rootfile.attrib.get("full-path")
        if not opf_path:
            return []
        opf = ET.fromstring(zip_file.read(opf_path))
        base = posixpath.dirname(opf_path)
        manifest = {
            item.attrib.get("id"): item.attrib
            for item in opf.findall(".//{*}manifest/{*}item")
            if item.attrib.get("id") and item.attrib.get("href")
        }
        paths: list[str] = []
        for itemref in opf.findall(".//{*}spine/{*}itemref"):
            item = manifest.get(itemref.attrib.get("idref"))
            if not item:
                continue
            media_type = item.get("media-type", "")
            href = item.get("href", "")
            if "html" not in media_type and not href.lower().endswith((".html", ".xhtml", ".htm")):
                continue
            paths.append(unquote(posixpath.normpath(posixpath.join(base, href))))
        return paths
    except Exception:
        return []


def extract_epub(path: Path, sha256: str, max_chars: int, overlap: int) -> ExtractedSource:
    chunks: list[dict] = []
    warnings: list[str] = []

    with zipfile.ZipFile(path) as zip_file:
        item_paths = epub_item_paths(zip_file)
        if not item_paths:
            item_paths = sorted(
                name
                for name in zip_file.namelist()
                if name.lower().endswith((".html", ".xhtml", ".htm"))
            )

        for chapter_index, item_path in enumerate(item_paths, start=1):
            try:
                raw = zip_file.read(item_path).decode("utf-8", errors="replace")
            except KeyError:
                warnings.append(f"missing EPUB item: {item_path}")
                continue
            text, heading = soup_text(raw)
            text = compact_text(text)
            if not text:
                continue
            label = f"chapter {chapter_index}"
            if heading:
                label = f"{label}: {heading[:80]}"
            for part in split_long_text(text, max_chars, overlap):
                chunks.append(
                    {
                        "locator": label,
                        "page_start": None,
                        "page_end": None,
                        "text": part,
                    }
                )

    extracted_chars = sum(len(chunk["text"]) for chunk in chunks)
    status = "ok" if chunks else "empty"
    warning = "; ".join(warnings)
    if not chunks and not warning:
        warning = "no readable EPUB text found"

    return ExtractedSource(
        path=path,
        title=short_title(path),
        file_type="epub",
        sha256=sha256,
        byte_count=path.stat().st_size,
        extraction_method="epub-xhtml",
        page_count=None,
        chunks=chunks,
        extracted_chars=extracted_chars,
        status=status,
        warning=warning,
    )


def extract_pdf(path: Path, sha256: str, args: argparse.Namespace) -> ExtractedSource:
    require_command("pdftotext")
    page_count = pdf_page_count(path)
    pages = pdftotext_pages(path, page_count)
    if page_count is None and pages:
        page_count = len(pages)

    warnings: list[str] = []
    method = "pdftotext"
    text_chars = sum(visible_chars(page) for page in pages)

    if not args.skip_ocr and page_count and should_ocr(
        pages,
        page_count,
        args.min_text_chars,
        args.min_page_chars,
    ):
        try:
            ocr_pages, ocr_warnings = ocr_pdf_pages(path, sha256, page_count, Path(args.out), args.ocr_dpi)
            ocr_chars = sum(visible_chars(page) for page in ocr_pages)
            warnings.extend(ocr_warnings)
            if ocr_chars > max(text_chars * 2, 500):
                pages = ocr_pages
                text_chars = ocr_chars
                method = "ocr"
            else:
                warnings.append("OCR did not improve extracted text enough; kept pdftotext output")
        except SystemExit:
            raise
        except Exception as exc:
            warnings.append(f"OCR failed: {exc}")

    chunks = chunks_from_pages(pages, args.chunk_chars, args.overlap_chars)
    extracted_chars = sum(len(chunk["text"]) for chunk in chunks)

    if not chunks:
        status = "empty"
        warnings.append("no readable PDF text found")
    elif text_chars < 500:
        status = "partial"
        warnings.append("very low extracted text coverage")
    else:
        status = "ok"

    return ExtractedSource(
        path=path,
        title=short_title(path),
        file_type="pdf",
        sha256=sha256,
        byte_count=path.stat().st_size,
        extraction_method=method,
        page_count=page_count,
        chunks=chunks,
        extracted_chars=extracted_chars,
        status=status,
        warning="; ".join(dict.fromkeys(warnings)),
    )


def init_db(db_path: Path) -> sqlite3.Connection:
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    con.executescript(
        """
        PRAGMA journal_mode = WAL;

        CREATE TABLE sources (
            id INTEGER PRIMARY KEY,
            path TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            file_type TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            byte_count INTEGER NOT NULL,
            extracted_chars INTEGER NOT NULL,
            extraction_method TEXT NOT NULL,
            page_count INTEGER,
            status TEXT NOT NULL,
            warning TEXT NOT NULL,
            built_at TEXT NOT NULL
        );

        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY,
            source_id INTEGER NOT NULL REFERENCES sources(id),
            locator TEXT NOT NULL,
            page_start INTEGER,
            page_end INTEGER,
            chunk_index INTEGER NOT NULL,
            text TEXT NOT NULL,
            char_count INTEGER NOT NULL
        );

        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            text,
            title,
            locator,
            source_id UNINDEXED,
            chunk_id UNINDEXED,
            tokenize = 'porter unicode61'
        );
        """
    )
    return con


def insert_source(con: sqlite3.Connection, source: ExtractedSource, built_at: str) -> None:
    cur = con.execute(
        """
        INSERT INTO sources (
            path, title, file_type, sha256, byte_count, extracted_chars,
            extraction_method, page_count, status, warning, built_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(source.path),
            source.title,
            source.file_type,
            source.sha256,
            source.byte_count,
            source.extracted_chars,
            source.extraction_method,
            source.page_count,
            source.status,
            source.warning,
            built_at,
        ),
    )
    source_id = cur.lastrowid

    for chunk_index, chunk in enumerate(source.chunks, start=1):
        chunk_cur = con.execute(
            """
            INSERT INTO chunks (
                source_id, locator, page_start, page_end, chunk_index, text, char_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source_id,
                chunk["locator"],
                chunk.get("page_start"),
                chunk.get("page_end"),
                chunk_index,
                chunk["text"],
                len(chunk["text"]),
            ),
        )
        chunk_id = chunk_cur.lastrowid
        con.execute(
            """
            INSERT INTO chunks_fts (rowid, text, title, locator, source_id, chunk_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (chunk_id, chunk["text"], source.title, chunk["locator"], source_id, chunk_id),
        )


def supported_files(source_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def escape_md_cell(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def write_reports(out_dir: Path, source_dir: Path, sources: list[ExtractedSource], built_at: str) -> None:
    manifest = {
        "built_at": built_at,
        "source_dir": str(source_dir),
        "supported_files": len(sources),
        "files": [
            {
                "path": str(source.path),
                "title": source.title,
                "file_type": source.file_type,
                "sha256": source.sha256,
                "byte_count": source.byte_count,
                "extracted_chars": source.extracted_chars,
                "extraction_method": source.extraction_method,
                "page_count": source.page_count,
                "chunks": len(source.chunks),
                "status": source.status,
                "warning": source.warning,
            }
            for source in sources
        ],
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    rows = [
        "# Corpus Coverage",
        "",
        f"Built at: `{built_at}`",
        f"Source folder: `{source_dir}`",
        f"Supported files: `{len(sources)}`",
        "",
        "| Status | Method | Chunks | Chars | Pages | File | Warning |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for source in sources:
        rows.append(
            "| "
            + " | ".join(
                [
                    escape_md_cell(source.status),
                    escape_md_cell(source.extraction_method),
                    escape_md_cell(len(source.chunks)),
                    escape_md_cell(source.extracted_chars),
                    escape_md_cell(source.page_count or ""),
                    escape_md_cell(source.path.name),
                    escape_md_cell(source.warning),
                ]
            )
            + " |"
        )
    (out_dir / "coverage.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def build(args: argparse.Namespace) -> None:
    source_dir = Path(args.source).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        fail(f"source folder does not exist: {source_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)
    files = supported_files(source_dir)
    if not files:
        fail(f"no supported PDF or EPUB files found in {source_dir}")

    db_path = out_dir / "neil-corpus.sqlite"
    built_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    con = init_db(db_path)
    extracted: list[ExtractedSource] = []

    try:
        for index, path in enumerate(files, start=1):
            print(f"[{index}/{len(files)}] {path.name}", flush=True)
            sha256 = file_sha256(path)
            if path.suffix.lower() == ".pdf":
                source = extract_pdf(path, sha256, args)
            elif path.suffix.lower() == ".epub":
                source = extract_epub(path, sha256, args.chunk_chars, args.overlap_chars)
            else:
                continue

            insert_source(con, source, built_at)
            extracted.append(source)
            print(
                f"  {source.status}: {len(source.chunks)} chunks, "
                f"{source.extracted_chars} chars, method={source.extraction_method}",
                flush=True,
            )
        con.commit()
    finally:
        con.close()

    write_reports(out_dir, source_dir, extracted, built_at)
    print(f"wrote {db_path}")
    print(f"wrote {out_dir / 'coverage.md'}")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local Neilization corpus index.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Folder containing source PDFs and EPUBs.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output folder for the local corpus index.")
    parser.add_argument("--chunk-chars", type=int, default=3500, help="Target maximum characters per search chunk.")
    parser.add_argument("--overlap-chars", type=int, default=250, help="Character overlap when splitting long text.")
    parser.add_argument("--min-text-chars", type=int, default=2000, help="Low total text threshold for OCR fallback.")
    parser.add_argument("--min-page-chars", type=int, default=100, help="Low average page text threshold for OCR fallback.")
    parser.add_argument("--ocr-dpi", type=int, default=200, help="DPI used when rendering OCR fallback pages.")
    parser.add_argument("--skip-ocr", action="store_true", help="Do not OCR low-text PDFs.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> None:
    args = parse_args(argv)
    build(args)


if __name__ == "__main__":
    main()
