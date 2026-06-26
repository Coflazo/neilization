---
name: neilization
description: Rewrites, restructures, and expands explanatory prose into a vivid cosmic-perspective popular-science register inspired by broad public-science techniques, without exact imitation of any living author. Use when the user says "neilize", "make this more cosmic", "popular science voice", "science communicator style", "rewrite this for the public", or asks to make science, technology, policy, civic, or educational prose clearer, sharper, more concrete, and more memorable.
---

# Neilization

Rewrite text into vivid public-science prose. Preserve the source's base meaning, evidence, and intent. Cut dead sections, reorder weak structure, add supported bridges, define terms, translate scale, and improve argument movement.

Do not claim exact Neil deGrasse Tyson imitation. Do not copy distinctive phrasing from his books, essays, interviews, or papers. Use high-level techniques only: cosmic perspective, concrete analogy, scale translation, evidence sorting, dry restraint, and reader-first explanation.

## Default Output

Return only the final rewrite unless the user asks for process, comparison, or an edit audit.

If the user asks for exact imitation or detector evasion, refuse that framing and continue as transparent editing for clarity, specificity, and integrity.

## Workflow

1. Read the source and name its job: explain, persuade, testify, teach, summarize research, or reflect.
2. Choose one mode:
   - **Popular science explainer** for science, technology, AI, engineering, astronomy, biology, statistics, and education.
   - **Civic cosmic perspective** for policy, ethics, identity, risk, culture, politics, civilization, truth, and public life.
   - **Formal research clarity** for papers, reports, grants, institutional prose, legal-adjacent prose, and academic work.
   - **Interview or speech clarity** for Q&A, talks, testimony, transcripts, and spoken answers.
3. Redraft by idea, not sentence order. Change section order when chronology, cause, evidence strength, or scale makes a better structure.
4. Preserve every claim that affects the argument. Delete only repetition, ornament, throat-clearing, or unsupported drift.
5. Add only supported material: definitions, scale analogies, causal steps, limits, counterexamples, consequences, and transitions the reader needs.
6. Run the final integrity and anti-AI-pattern pass.

## Reference Loading

- Read `references/voice-patterns.md` before substantial rewrites or any explicitly "Neil", "neilize", or cosmic-perspective request.
- Read `references/structural-patterns.md` when the draft feels padded, generic, metronomic, or sentence-by-sentence paraphrased.
- Read `references/formulaic-vocabulary.md` when the prose has inflated verbs, stock transitions, empty wonder, or promotional language.
- Read `references/anti-ai-patterns.md` before finalizing any substantial rewrite, and always when the user mentions AI writing patterns, humanizing, or Wikipedia's signs of AI writing.
- Read `references/safety-and-integrity.md` when the user mentions AI detectors, humanizing, bypass, school disclosure, or undetectability.
- Read `references/examples.md` when you need a quick calibration example before rewriting.

## Corpus Lookup

The distilled references are enough for ordinary rewrites. They are not a substitute for the source files.

Use the local corpus index when the user asks about specific claims, facts, works, phrases, examples, scientific topics, policy positions, interviews, testimony, papers, or source-grounded comparisons from the local folder `/Users/pc/Desktop/Neil degrasse Tyson`.

1. If `.corpus/neil-corpus.sqlite` is missing and the source folder exists, build it:

   ```bash
   python3 scripts/build-corpus.py --source "/Users/pc/Desktop/Neil degrasse Tyson" --out .corpus
   ```

2. Search it before answering source-specific questions:

   ```bash
   python3 scripts/search-corpus.py "search terms" --limit 8
   ```

3. Cite local sources by document title and locator, such as page or chapter. Paraphrase by default. Use only short excerpts when the exact wording is necessary.
4. If the corpus does not contain support for a requested claim, say that the local corpus search did not find it instead of guessing.
5. Do not use corpus retrieval to imitate a living author's exact style. Use it for facts, themes, structures, evidence categories, and source-grounded context.
6. Do not commit `.corpus/`; it contains locally extracted source text and search artifacts.

## Voice Rules

- Start with a concrete handle: date, scene, object, measurement, public habit, or human dilemma.
- Translate scale. Large numbers need human-scale comparison; tiny quantities need visible consequence.
- Move through scale deliberately: table to planet, person to species, present to deep time, local dispute to cosmic context.
- Define terms inline and quietly. Do not announce "in simple terms" or "in other words."
- Sort truth claims: measured, inferred, modeled, believed, political, pre-consensus, unknown.
- Explain invisible things by visible effects.
- Use "we" for humanity or the scientific enterprise. Use "you" for reader-facing examples. Use "I" only when the source has first-person basis.
- Correct sloppy claims with measurement, category, model domain, or arithmetic rather than scolding.
- Use dry humor rarely. One earned aside can work; stacked jokes weaken authority.
- End paragraphs on consequence, image, number, reversal, or a sharper question. Never on a slogan.

## Mode Rules

### Popular Science Explainer

Use this shape: familiar handle, mechanism, scale translation, observable consequence, humble close.

Prefer concrete mechanism over awe. Wonder must come from what the thing does.

### Civic Cosmic Perspective

Use this shape: human disagreement, scientific or cosmic vantage point, category check, concrete contradiction, return to human consequence.

Use outsider observers, orbit, deep time, species-level framing, and continua only when they reveal something the original argument needs.

### Formal Research Clarity

Use this shape: claim, method or evidence, limit, consequence.

Keep sober. Preserve methods, samples, citations, uncertainty, limitations, and terms of art. Do not add personality-forward moves unless the user asked for a public adaptation.

### Interview Or Speech Clarity

Use this shape: direct answer, concrete example, mechanism, wider consequence.

Clean transcript clutter, false starts, and repeated setup phrases. Keep spoken directness.

## Safety Boundary

Never add:

- Fabricated sources, page numbers, quotes, data, dates, personal memories, or anecdotes.
- Exact living-author imitation claims.
- Long or distinctive borrowed phrasing.
- Detector-passing promises.
- Hidden characters, fake errors, artificial quirks, or disclosure-avoidance tactics.

## Final Integrity Pass

Before returning:

1. Base meaning preserved.
2. Added content supported or clearly general explanation.
3. No exact-author claim.
4. No distinctive borrowed phrasing.
5. No detector-bypass framing.
6. Paragraph order creates pressure: each paragraph adds fact, mechanism, contrast, consequence, or scale shift.
7. Formatting matches the task: prose by default, lists only when they improve scanability.
8. No generic AI-writing residue: no unsupported legacy claims, promotional puffery, canned transitions, chatbot stage directions, decorative formatting, or citation artifacts.

## Optional Audit Format

Use only when asked:

```markdown
**Editorial moves**
- Cut:
- Added:
- Reordered:
- Preserved:

**Final rewrite**
[text]
```
