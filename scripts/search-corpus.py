#!/usr/bin/env python3
"""Search the local Neilization corpus index."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Iterable


DEFAULT_DB = Path(".corpus/neil-corpus.sqlite")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def fts_terms(query: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9_'-]*", query)


def fts_query(query: str, mode: str) -> str:
    terms = fts_terms(query)
    if not terms:
        fail("query has no searchable terms")
    operator = " AND " if mode == "and" else " OR "
    return operator.join(f'"{term}"' for term in terms)


def compact_snippet(text: str, max_words: int = 28) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split(" ")
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(".,;:") + "..."


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        fail(f"corpus database not found: {db_path}. Run scripts/build-corpus.py first.")
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    return con


def search_once(con: sqlite3.Connection, match_query: str, limit: int) -> list[sqlite3.Row]:
    return list(
        con.execute(
            """
            SELECT
                c.id AS chunk_id,
                s.title,
                s.path,
                s.file_type,
                s.extraction_method,
                s.status,
                c.locator,
                c.chunk_index,
                bm25(chunks_fts) AS score,
                snippet(chunks_fts, 0, '[', ']', '...', 28) AS snippet
            FROM chunks_fts
            JOIN chunks c ON c.id = chunks_fts.rowid
            JOIN sources s ON s.id = c.source_id
            WHERE chunks_fts MATCH ?
            ORDER BY score ASC
            LIMIT ?
            """,
            (match_query, limit),
        )
    )


def search(db_path: Path, query: str, limit: int) -> tuple[list[dict], str]:
    con = connect(db_path)
    try:
        rows = search_once(con, fts_query(query, "and"), limit)
        match_mode = "all_terms"
        if not rows:
            rows = search_once(con, fts_query(query, "or"), limit)
            match_mode = "partial_terms" if rows else "none"
    finally:
        con.close()

    results = []
    for row in rows:
        results.append(
            {
                "title": row["title"],
                "path": row["path"],
                "file_type": row["file_type"],
                "extraction_method": row["extraction_method"],
                "status": row["status"],
                "locator": row["locator"],
                "chunk_id": row["chunk_id"],
                "chunk_index": row["chunk_index"],
                "score": row["score"],
                "snippet": compact_snippet(row["snippet"]),
            }
        )
    return results, match_mode


def print_markdown(results: list[dict], query: str, match_mode: str) -> None:
    if not results:
        print(f"No local corpus matches found for: {query}")
        return

    if match_mode == "partial_terms":
        print(f"Partial local corpus matches for: {query}")
        print("No result matched every query term.")
    else:
        print(f"Local corpus matches for: {query}")
    print()
    for index, result in enumerate(results, start=1):
        print(
            f"{index}. {result['title']} "
            f"({result['file_type']}, {result['locator']}, {result['extraction_method']})"
        )
        print(f"   chunk_id: {result['chunk_id']}")
        print(f"   path: {result['path']}")
        print(f"   snippet: {result['snippet']}")
        print()


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search the local Neilization corpus index.")
    parser.add_argument("query", help="Search query.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to .corpus/neil-corpus.sqlite.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum number of results.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> None:
    args = parse_args(argv)
    results, match_mode = search(Path(args.db), args.query, args.limit)
    if args.json:
        print(json.dumps({"query": args.query, "match_mode": match_mode, "results": results}, indent=2, ensure_ascii=False))
    else:
        print_markdown(results, args.query, match_mode)


if __name__ == "__main__":
    main()
