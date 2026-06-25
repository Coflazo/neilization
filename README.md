<table>
<tr>
<td width="150" valign="top">
  <img src="assets/neilization.png" width="130" alt="Neilization line-art mark" />
</td>
<td valign="top">

# neilization

Cosmic-perspective rewriting for public science, civic explanation, research clarity, and spoken answers.

`neilization` is a Claude skill that takes flat explanatory prose and turns it into clearer, more concrete, more public-facing writing. It preserves the source meaning, removes dead weight, adds supported bridges, translates scale, and makes the argument move.

</td>
</tr>
</table>

```text
source text
  -> preserve the base claim
  -> cut what is not doing work
  -> add only supported explanation
  -> translate scale into human terms
  -> return a defensible rewrite
```

This is not a celebrity impersonation package. It uses high-level public-science techniques: concrete analogy, scale translation, evidence sorting, restrained humor, and the view from a wider frame.

## Quick Start

Place the folder here:

```bash
~/.claude/skills/neilization/
```

Use it in Claude with prompts like:

```text
neilize this essay
make this paragraph more cosmic
rewrite this for a public science audience
turn this draft into a sharper explainer
edit this speech answer so it is direct and vivid
```

By default, the skill returns only the rewritten text. Ask for an audit when you want to see what changed.

```text
Neilize this paragraph and include an edit audit.
```

## The Contract

| It must do | It must not do |
|---|---|
| Preserve the source's base meaning. | Invent facts, sources, quotes, dates, or anecdotes. |
| Cut repetition, filler, and unsupported drift. | Copy distinctive phrasing from books, interviews, or essays. |
| Add definitions, causal bridges, limits, and scale analogies when supported. | Promise detector results or disclosure avoidance. |
| Reorder ideas when the argument becomes clearer. | Pretend to reproduce a living writer's personal voice. |
| Match the register to the job: essay, civic, research, or speech. | Turn formal research into personality-forward prose unless asked. |

## Transformations

The examples below are literal test inputs transformed with this skill's own rules. They are not quotations, external examples, or sourced claims.

### 1. Urban Heat

**Input**

```text
Cities install heat sensors to understand where neighborhoods become dangerously hot. The data can help officials decide where to plant trees, open cooling centers, and update building rules.
```

**Neilized output**

```text
On a summer afternoon, a city does not heat evenly. Asphalt lots, flat roofs, and treeless blocks hold heat long after the weather report gives one tidy number for the whole place. A heat sensor turns that hidden geography into evidence. Once officials can see which blocks are storing the most heat, shade stops being decoration. It becomes infrastructure, as practical as a drain or a streetlight.
```

What changed:

- The abstract policy action became a visible city scene.
- The mechanism became measurable: different surfaces store heat differently.
- The close turns "trees" from decoration into infrastructure.

### 2. Classroom Assessment

**Input**

```text
Teachers use formative assessment to see what students understand during a lesson. This information helps them adjust instruction before the final test.
```

**Neilized output**

```text
By the time a final exam arrives, the learning has already happened or failed to happen. Formative assessment moves the measurement upstream. A quick question, a messy worksheet, or a wrong answer on the board tells the teacher where the class is losing the thread while there is still time to repair it. It is less like a verdict and more like an instrument panel for the lesson while the lesson is still flying.
```

What changed:

- The definition is embedded in the explanation.
- The timing problem becomes the structure of the paragraph.
- The analogy clarifies the function without changing the claim.

### 3. Space Policy

**Input**

```text
Space exploration can inspire students and lead to technological innovation, but public investments must be balanced against other needs.
```

**Neilized output**

```text
A space program is never paid for with awe. It is paid for with budgets, which means it must stand beside schools, bridges, hospitals, and every other claim a civilization makes on its future. Its strongest case is not simply that the universe is beautiful, though it is. The case is that exploration trains a society to solve problems at the edge of what it knows, then returns some of that discipline to Earth in the form of instruments, engineers, and ambition.
```

What changed:

- The paragraph keeps the budget tradeoff.
- The inspirational claim is grounded in institutions and training.
- The cosmic frame returns to Earth instead of drifting away from the policy question.

### 4. Generic Technical Prose

**Input**

```text
Machine learning is a transformative technology that leverages data to identify patterns and make predictions across many industries.
```

**Neilized output**

```text
Machine learning begins with examples. Feed a model enough labeled X-rays, loan applications, or weather readings, and it adjusts its internal settings until its guesses stop being terrible. The machine has not acquired wisdom. It has fit a function to a mountain of cases. What changed in the past decade is the size of the mountain.
```

What changed:

- Hype words were replaced with mechanism.
- The claim is narrower and easier to defend.
- Scale becomes the ending, not a slogan.

## Rewrite Modes

| Mode | Best for | Shape |
|---|---|---|
| Popular science explainer | Science, technology, AI, astronomy, engineering, statistics, education | Familiar handle, mechanism, scale, consequence, humble close. |
| Civic cosmic perspective | Culture, policy, ethics, identity, risk, truth, civilization | Human disagreement, wider vantage point, category check, contradiction, human consequence. |
| Formal research clarity | Papers, reports, grants, institutional prose, academic work | Claim, method or evidence, limit, consequence. |
| Interview or speech clarity | Q&A, testimony, talks, transcripts | Direct answer, concrete example, mechanism, wider consequence. |

## How Claude Uses The Skill

`SKILL.md` is the runtime file. It stays short so Claude can load the core behavior quickly.

The `references/` files provide detail only when needed:

- `voice-patterns.md` for public-science cadence, scale translation, and evidence sorting.
- `structural-patterns.md` for paragraph order, argument pressure, and pruning.
- `formulaic-vocabulary.md` for replacing inflated or generic language.
- `safety-and-integrity.md` for detector, disclosure, and imitation boundaries.
- `examples.md` for quick calibration.

The skill chooses a mode, rewrites by idea rather than sentence order, and finishes with an integrity pass:

```text
meaning preserved
added material supported
no copied distinctive phrasing
no fabricated evidence
no detector framing
paragraphs move the argument forward
```

## Quality Bar

A strong rewrite should answer yes to these questions:

| Check | Question |
|---|---|
| Meaning | Does the original claim still survive? |
| Evidence | Is every added detail supported or clearly general explanation? |
| Scale | Can the reader picture the size, time, cost, or consequence? |
| Mechanism | Does wonder come from what the thing does, not hype words? |
| Structure | Does each paragraph add fact, mechanism, contrast, consequence, or scale? |
| Register | Did formal prose stay formal, and public prose become vivid? |
| Integrity | Is the result transparent, defensible, and free of fake evidence? |

## Safety Boundary

`neilization` refuses the wrong job and continues with the right one.

It will not:

- Claim to reproduce a living author's prose as a personal imitation.
- Copy distinctive sentences from books, essays, interviews, or papers.
- Invent sources, data, dates, page numbers, quotations, memories, or anecdotes.
- Promise detector outcomes.
- Add hidden characters, fake mistakes, disclosure-avoidance tactics, or artificial quirks.

It will:

- Rewrite for clarity, rhythm, structure, and public understanding.
- Preserve the user's intended claim.
- Mark uncertainty when the source does not support a stronger statement.
- Keep research and institutional prose sober when the audience requires it.

## Package Layout

```text
neilization/
├── SKILL.md
├── README.md
├── assets/
│   └── neilization.png
├── references/
│   ├── examples.md
│   ├── formulaic-vocabulary.md
│   ├── safety-and-integrity.md
│   ├── structural-patterns.md
│   └── voice-patterns.md
└── scripts/
    └── validate.mjs
```

## Validate

Run the package check:

```bash
node ~/.claude/skills/neilization/scripts/validate.mjs
```

The validator checks:

- `SKILL.md` frontmatter.
- Required package files.
- The PNG asset.
- README image reference.
- No emojis in the README.
- No unsafe detector or imitation wording in active files.

## Maintainer Notes

The package is designed around four principles:

- Small runtime surface.
- One-level reference loading.
- Real examples over vague promises.
- Explicit integrity boundary.

The result should feel like a serious writing tool: concrete enough to test, disciplined enough to trust, and flexible enough to handle essays, testimony, research summaries, and spoken answers.
