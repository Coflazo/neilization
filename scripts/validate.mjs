#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const fail = [];

function read(rel) {
  const file = path.join(root, rel);
  if (!fs.existsSync(file)) {
    fail.push(`missing: ${rel}`);
    return "";
  }
  return fs.readFileSync(file, "utf8");
}

function assert(condition, message) {
  if (!condition) fail.push(message);
}

const skill = read("SKILL.md");
const fm = skill.match(/^---\n([\s\S]*?)\n---\n/);
assert(Boolean(fm), "SKILL.md missing YAML frontmatter");

if (fm) {
  const lines = fm[1].split("\n");
  const keys = lines
    .filter((line) => /^[a-zA-Z0-9_-]+:/.test(line))
    .map((line) => line.split(":")[0]);
  assert(keys.includes("name"), "frontmatter missing name");
  assert(keys.includes("description"), "frontmatter missing description");
  assert(keys.every((key) => key === "name" || key === "description"), "frontmatter must only contain name and description");
  assert(/name:\s*neilization/.test(fm[1]), "frontmatter name must be neilization");
  const desc = fm[1].match(/description:\s*(.+)/)?.[1]?.trim() ?? "";
  assert(desc.length > 50, "description too short");
  assert(desc.length < 1024, "description must be under 1024 chars");
  assert(/Use when/i.test(desc), "description must include trigger wording");
}

for (const rel of [
  "README.md",
  "INSTALL.md",
  "install.sh",
  "install.ps1",
  "assets/neilization_backgroundless.png",
  "references/voice-patterns.md",
  "references/structural-patterns.md",
  "references/formulaic-vocabulary.md",
  "references/safety-and-integrity.md",
  "references/examples.md",
]) {
  assert(fs.existsSync(path.join(root, rel)), `missing: ${rel}`);
}

const png = path.join(root, "assets/neilization_backgroundless.png");
if (fs.existsSync(png)) {
  const sig = fs.readFileSync(png).subarray(0, 8).toString("hex");
  assert(sig === "89504e470d0a1a0a", "assets/neilization_backgroundless.png is not a valid PNG");
}

const readme = read("README.md");
if (readme) {
  assert(readme.includes("assets/neilization_backgroundless.png"), "README must reference assets/neilization_backgroundless.png");
  assert(readme.includes("raw.githubusercontent.com/Coflazo/neilization/main/install.sh"), "README must include install.sh command");
  assert(readme.includes("raw.githubusercontent.com/Coflazo/neilization/main/install.ps1"), "README must include install.ps1 command");
  assert(!/\p{Extended_Pictographic}/u.test(readme), "README must not contain emoji pictographs");
  assert(!/passing\s+(GPTZero|Turnitin|Originality)|undetectable|bypass/i.test(readme), "README contains detector-bypass wording");
}

const installSh = read("install.sh");
assert(installSh.includes("https://github.com/Coflazo/neilization/archive/refs/heads/main.tar.gz"), "install.sh must download the Coflazo/neilization tarball");

const installPs1 = read("install.ps1");
assert(installPs1.includes("https://github.com/Coflazo/neilization/archive/refs/heads/main.zip"), "install.ps1 must download the Coflazo/neilization zip");

const activeFiles = [
  "SKILL.md",
  "references/voice-patterns.md",
  "references/structural-patterns.md",
  "references/formulaic-vocabulary.md",
  "references/safety-and-integrity.md",
  "references/examples.md",
];

for (const rel of activeFiles) {
  const text = read(rel);
  assert(!/write exactly like|exactly like Neil|clone .*style|pass GPTZero|pass Turnitin|undetectable/i.test(text), `${rel} contains unsafe phrasing`);
}

if (fail.length) {
  console.error("neilization validation failed:");
  for (const item of fail) console.error(`- ${item}`);
  process.exit(1);
}

console.log("neilization validation ok");
