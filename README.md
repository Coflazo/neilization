<table>
<tr>
<td width="150" valign="top">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/neilization_backgroundless.png">
    <img src="assets/neilization_backgroundless_light.png" width="132" alt="Neilization line-art mark">
  </picture>
</td>
<td valign="top">

# neilization

Claude skill for turning plain explanation into public-science prose with a cosmic-perspective lens.

It preserves the base meaning, cuts dead weight, adds supported explanatory bridges, translates scale, and returns a rewrite that a real writer can defend.

It also includes a built-in humanizer pass calibrated against Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) field guide, so the rewrite rejects stock AI patterns instead of merely sounding more polished.

</td>
</tr>
</table>

```text
flat draft -> evidence sorted -> scale made visible -> sharper public prose
```

## Why This Exists

<details open>
<summary><strong>A personal note</strong></summary>

I have been a fan of Neil deGrasse Tyson's work for a long time. The appeal is direct: he can enter almost any room in the population and make the room feel less locked out of the subject. A scientist can explain a paper to another scientist. That is expected. The rarer ability is explaining a scientific idea to the person who already decided, years ago, that science was not written for them.

For our parents' generation, Carl Sagan's *Cosmos* made that bridge feel possible on television. Today the same public role is carried by people like Neil deGrasse Tyson, Brian Cox, Michio Kaku, Becky Smethurst, and many others. We have to admit that many of us watch their videos, and some of us read their books, because they make the universe feel less private.

</details>

<details>
<summary><strong>The public-science problem</strong></summary>

Decades ago, a scientist could more easily treat public understandability as optional: useful, maybe morally good, but not always central to the job. That changed unevenly across countries and institutions. The 1985 [Bodmer Report](https://royalsociety.org/news-resources/publications/1985/public-understanding-science/) helped give the "public understanding of science" movement one of its canonical landmarks. In the United States, the National Science Foundation's broader-impacts criterion became part of grant review in [1997](https://academic.oup.com/bioscience/article/65/4/397/254803). In the United Kingdom, [REF 2014](https://www.rand.org/randeurope/research/projects/2015/hefce-ref2014-impact.html) made "impact" part of a funding-linked research assessment. These are not the same policy, and they did not happen for the same reason, but the direction is hard to miss.

Some scientists understandably disliked the new pressure. If a researcher has limited time and energy, then asking for public explanation can feel like moving effort away from the research itself. That argument used to sound stronger than it does now. Public understanding can affect trust, funding, recruitment, and the willingness of young people, and their parents, to imagine science as something they can enter rather than something they can only admire from outside.

</details>

<details>
<summary><strong>What neilization is trying to do</strong></summary>

`neilization` starts from that tension. It is free to use, and its guidance was calibrated from a large reference corpus spanning thousands of pages of publicly available Neil deGrasse Tyson materials: public-science prose, interviews, testimony, essays, and research PDFs. It is not a neural training run. It does not claim exact personal voice imitation. It studies high-level explanatory moves: how to begin with a human handle, widen the frame, sort evidence, translate scale, and return the cosmic thought back to the person reading.

The skill also carries a humanizer pass calibrated against Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). That pass checks for the habits that make prose feel machine-smoothed: puffed-up importance, vague attribution, promotional diction, stock transitions, decorative formatting, chatbot stage directions, citation artifacts, and neat little three-part packages that look organized before they have earned the organization.

The next stages should add separate branches for other science explainers, each calibrated from public material and each with its own register, tone, and explanatory instincts. The larger goal is simple: make difficult text less private without making it less honest.

</details>

| Moment | Why it matters here |
|---|---|
| Carl Sagan and *Cosmos* | A model for making the scientific imagination public. |
| 1985 Bodmer Report | Public understanding becomes a named institutional concern. |
| NSF broader impacts, 1997 | Scientific merit begins sharing space with broader public consequence in grant review. |
| REF 2014 impact assessment | Research impact becomes visibly tied to funding-linked assessment in the UK. |
| Today's explainers | Public science becomes education, trust-building, audience growth, and career infrastructure at the same time. |

## Install

One line. Finds supported local agent homes. Installs for each.

macOS / Linux / WSL / Git Bash:

```bash
curl -fsSL https://raw.githubusercontent.com/Coflazo/neilization/main/install.sh | bash
```

Windows PowerShell 5.1+:

```powershell
irm https://raw.githubusercontent.com/Coflazo/neilization/main/install.ps1 | iex
```

About 30 seconds. No build step. Node >=18 is only needed for the validator. Safe to re-run.

Trigger: type `/neilization` or say `neilize this`. There is no sticky mode to stop; ask for a normal edit when you do not want the skill.

One agent only, manual install, custom directory, or troubleshooting: see [INSTALL.md](INSTALL.md). Install break? Open your agent and say:

```text
Read README.md and INSTALL.md, install neilization for me.
```

Manual path:

```bash
~/.claude/skills/neilization/
```

Run the package check after install:

```bash
node ~/.claude/skills/neilization/scripts/validate.mjs
```

## What You Get

| Skill surface | What |
|---|---|
| `/neilization <text>` | Rewrites explanatory prose into public-science language with a cosmic-perspective lens. |
| `neilize this` | Natural-language trigger for the same rewrite behavior. |
| `make this more cosmic` | Adds scale, consequence, and wider-frame context without inventing claims. |
| `rewrite this for the public` | Turns technical or institutional prose into clear reader-facing explanation. |
| `include an edit audit` | Returns what was cut, added, reordered, and preserved before the final rewrite. |
| Popular science mode | Mechanism first, then scale, consequence, and a humble close. |
| Civic cosmic mode | Sorts belief, measurement, inference, preference, and public consequence. |
| Formal research mode | Keeps papers, reports, and grants sober: claim, method, limit, consequence. |
| Speech clarity mode | Cleans Q&A, testimony, talks, and transcripts into direct spoken prose. |
| Built-in humanizer pass | Removes formulaic AI-writing residue while preserving disclosure and evidence boundaries. |
| `scripts/validate.mjs` | Checks package structure, frontmatter, README image path, PNG validity, no emojis, and safety wording. |

## Optional Local Corpus Index

If you keep a local folder of Neil deGrasse Tyson source files, the skill can build a private search index from those PDFs and EPUBs. The index lets the agent look up document-specific facts, topics, and examples before answering source-grounded questions.

Build the local index:

```bash
python3 ~/.claude/skills/neilization/scripts/build-corpus.py \
  --source "/Users/pc/Desktop/Neil degrasse Tyson" \
  --out ~/.claude/skills/neilization/.corpus
```

Search it directly:

```bash
python3 ~/.claude/skills/neilization/scripts/search-corpus.py \
  "cosmic perspective" \
  --db ~/.claude/skills/neilization/.corpus/neil-corpus.sqlite
```

`.corpus/` is ignored by git. It is a local artifact containing extracted text, OCR cache files, and the SQLite search index.

Example prompts:

```text
neilize this paragraph
rewrite this for a public science audience
make this more cosmic, but keep it accurate
turn this speech answer into something direct and vivid
```

## What It Is

`neilization` is a writing skill, not a celebrity impersonation tool. It uses high-level public-science techniques: concrete examples, scale translation, evidence sorting, restrained humor, and the habit of moving from the local fact to the wider frame.

The default response is the final rewrite only. If you want the edit trail, ask for an audit:

```text
Neilize this essay and include what you cut, added, reordered, and preserved.
```

## Rewrite Modes

| Source text | Best mode | What improves |
|---|---|---|
| Technical explainers | Popular science | Mechanism, analogy, scale, consequence. |
| Policy or civic prose | Civic cosmic perspective | Evidence categories, contradictions, public stakes. |
| Papers and reports | Formal research clarity | Claim, method, limitation, consequence. |
| Talks or interviews | Speech clarity | Direct answer, concrete example, rhythm. |

## Real Transformations

These are literal test inputs rewritten with this skill's own rules. They are not quotations, sourced examples, or claims of personal voice imitation.

### Urban Heat

**Input**

```text
Cities install heat sensors to understand where neighborhoods become dangerously hot. The data can help officials decide where to plant trees, open cooling centers, and update building rules.
```

**Output**

```text
On a summer afternoon, a city does not heat evenly. Asphalt lots, flat roofs, and treeless blocks hold heat long after the weather report gives one tidy number for the whole place. A heat sensor turns that hidden geography into evidence. Once officials can see which blocks are storing the most heat, shade stops being decoration. It becomes infrastructure, as practical as a drain or a streetlight.
```

**Edit moves**

| Move | Result |
|---|---|
| Opened with a scene | The policy problem becomes visible before it becomes abstract. |
| Named the mechanism | Different surfaces store heat differently. |
| Reframed the consequence | Trees become infrastructure, not ornament. |

### Classroom Assessment

**Input**

```text
Teachers use formative assessment to see what students understand during a lesson. This information helps them adjust instruction before the final test.
```

**Output**

```text
By the time a final exam arrives, the learning has already happened or failed to happen. Formative assessment moves the measurement upstream. A quick question, a messy worksheet, or a wrong answer on the board tells the teacher where the class is losing the thread while there is still time to repair it. It is less like a verdict and more like an instrument panel for the lesson while the lesson is still flying.
```

**Edit moves**

| Move | Result |
|---|---|
| Reordered around timing | The final test becomes the endpoint, not the opening abstraction. |
| Defined the term inline | The reader learns what formative assessment does without a glossary. |
| Added a bounded analogy | The instrument panel image clarifies function without changing the claim. |

### Space Policy

**Input**

```text
Space exploration can inspire students and lead to technological innovation, but public investments must be balanced against other needs.
```

**Output**

```text
A space program is never paid for with awe. It is paid for with budgets, which means it must stand beside schools, bridges, hospitals, and every other claim a civilization makes on its future. The universe is beautiful, and beauty can start the conversation. The public case has to survive the budget hearing: exploration trains a society to solve problems at the edge of what it knows, then returns some of that discipline to Earth in the form of instruments, engineers, and ambition.
```

**Edit moves**

| Move | Result |
|---|---|
| Preserved the tradeoff | The paragraph keeps public budget pressure in view. |
| Grounded the inspiration claim | Awe becomes training, instruments, engineers, and ambition. |
| Returned the cosmic frame to Earth | The argument stays useful for policy instead of drifting into wonder. |

### Generic Technical Prose

**Input**

```text
Machine learning is a transformative technology that leverages data to identify patterns and make predictions across many industries.
```

**Output**

```text
Machine learning begins with examples. Feed a model enough labeled X-rays, loan applications, or weather readings, and it adjusts its internal settings until its guesses stop being terrible. The machine has not acquired wisdom. It has fit a function to a mountain of cases. What changed in the past decade is the size of the mountain.
```

**Edit moves**

| Move | Result |
|---|---|
| Removed hype | "Transformative" and "leverages" become mechanism. |
| Added concrete domains | X-rays, loan applications, and weather readings make the abstraction testable. |
| Ended on scale | The closing sentence names what actually changed. |

## Operating Rules

| Rule | Standard |
|---|---|
| Meaning first | The original claim must still survive. |
| Support only | Added explanation must be supported by the source or safe general context. |
| Cut aggressively | Repetition, throat-clearing, and unsupported drift can go. |
| Reorder freely | The final structure should follow cause, chronology, evidence strength, or scale. |
| Match register | Research stays sober. Public prose can become more vivid. |
| Reject AI residue | Remove generic importance, stock transitions, over-formatting, chatbot residue, and citation artifacts. |
| Stay transparent | No fabricated evidence, copied phrasing, or detector promises. |

## How Claude Loads It

`SKILL.md` is intentionally short. It gives Claude the runtime behavior, the mode selection, the safety boundary, and the final integrity pass.

Reference files stay one level deep:

| File | Role |
|---|---|
| `references/voice-patterns.md` | Public-science cadence, scale translation, evidence sorting. |
| `references/structural-patterns.md` | Paragraph order, pruning, argument pressure. |
| `references/formulaic-vocabulary.md` | Replacements for inflated words and stock transitions. |
| `references/anti-ai-patterns.md` | Humanizer quality gate based on Wikipedia's signs of AI writing. |
| `references/safety-and-integrity.md` | Boundaries for imitation, disclosure, and detector requests. |
| `references/examples.md` | Short calibration examples. |

## Safety Boundary

The skill will not:

- Claim to reproduce a living writer's prose as a personal imitation.
- Copy distinctive sentences from books, essays, interviews, or papers.
- Invent sources, data, dates, page numbers, quotations, memories, or anecdotes.
- Promise detector outcomes.
- Add hidden characters, fake mistakes, disclosure-avoidance tactics, or artificial quirks.
- Treat AI-writing signs as a detector game instead of a prose-quality problem.

It will redirect those requests into transparent editing: clearer claims, stronger structure, accurate evidence, and prose the writer can defend.

## Package Layout

```text
neilization/
|-- SKILL.md
|-- README.md
|-- INSTALL.md
|-- install.sh
|-- install.ps1
|-- assets/
|   |-- neilization_backgroundless.png
|   `-- neilization_backgroundless_light.png
|-- references/
|   |-- anti-ai-patterns.md
|   |-- examples.md
|   |-- formulaic-vocabulary.md
|   |-- safety-and-integrity.md
|   |-- structural-patterns.md
|   `-- voice-patterns.md
`-- scripts/
    `-- validate.mjs
```

## Maintainer Checklist

Before shipping changes:

```bash
node scripts/validate.mjs
```

Then verify:

| Check | Pass condition |
|---|---|
| README image | Uses light and dark marks with a GitHub-compatible `<picture>` block. |
| Examples | Inputs and outputs are constructed, not attributed. |
| Skill frontmatter | Contains only `name` and `description`. |
| References | Stay one level deep and load only when needed. |
| Safety | No exact-imitation, fake-source, or detector-result promises. |
| Humanizer | Wikipedia AI-writing signs are handled as prose-quality checks, not detector promises. |
| Installers | `install.sh` and `install.ps1` point at `Coflazo/neilization`. |
| Style | No emojis, no decorative filler, no copied README structure. |

## Design Notes

This package is designed as a compact tool, not a showcase page. The README uses the mark once, puts setup near the top, proves behavior with real transformations, and keeps the rest scannable for future maintainers.

The intended feel: sober, sharp, readable, and a little cosmic only when the sentence earns it.
