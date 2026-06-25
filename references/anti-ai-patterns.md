# Anti-AI Pattern Pass

Source field guide: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

Use this reference as a humanizer quality gate. The goal is not detector evasion. The goal is to remove formulaic chatbot residue so the final prose reads like a writer made real choices: specific, uneven where useful, accountable to evidence, and free of machine-default polish.

## Core Principle

Do not make the text merely less detectable. Make it less generic.

AI-sounding prose often fails because it smooths strange facts into broad importance. It adds significance instead of evidence, structure instead of thought, and decorative polish instead of a reason for the sentence to exist.

## Remove These Patterns

### 1. Generic importance without evidence

Watch for language that inflates the subject before proving anything:

- "stands as"
- "serves as"
- "testament"
- "lasting legacy"
- "broader trend"
- "key turning point"
- "marks a shift"
- "important reminder"

Replacement rule: name the actual mechanism, measurement, consequence, or dispute. If there is no evidence for importance, cut the importance claim.

### 2. Superficial analysis

Watch for sentences that add a vague interpretive tail:

- "highlighting the importance of..."
- "underscoring the role of..."
- "reflecting a broader..."
- "contributing to..."
- "fostering..."
- "offering valuable insights..."

Replacement rule: ask what changed, who changed it, how it was measured, and what follows from it. If the sentence only gestures, remove it.

### 3. Promotional diction

Cut sales-copy language unless the source itself is being quoted:

- "boasts"
- "vibrant"
- "rich tapestry"
- "groundbreaking"
- "renowned"
- "showcasing"
- "diverse array"
- "in the heart of"
- "natural beauty"

Replacement rule: replace praise with concrete nouns, dates, actions, limits, and observed effects.

### 4. Elegant variation

Do not synonym-cycle just to avoid repetition. Human technical prose often repeats the correct term. If "planet", "policy", "model", or "cell" is the right word, reuse it.

Replacement rule: vary rhythm, sentence length, and paragraph pressure instead of swapping in ornate synonyms.

### 5. Mechanical contrast

Avoid reflexive constructions:

- "not only X, but also Y"
- "not just X, it is Y"
- "no X, no Y, just Z"
- "rather than..."

Replacement rule: state the stronger claim directly. Use contrast only when the source argument genuinely turns on a distinction.

### 6. Rule-of-three packaging

Do not default to three nouns, three adjectives, or three parallel examples. Use the number of examples the idea earns. Two can be enough. Four can be more honest.

Replacement rule: let the material determine the count.

### 7. Chatbot stage directions

Remove any residue of a chatbot conversation:

- "Of course"
- "Certainly"
- "I hope this helps"
- "Would you like"
- "let me know"
- "here is a"
- "based on available information"
- "as of my last knowledge update"
- placeholders like `[insert source]`, `PASTE_URL_HERE`, or `2025-XX-XX`

Replacement rule: final output should be the writing itself, not a message about the writing.

### 8. Formatting tells

Avoid AI-default formatting unless the user asked for that exact format:

- Decorative emoji.
- Over-bolded list headers.
- Title-case mini-headings inside ordinary prose.
- Unnecessary tables.
- Thematic breaks before headings.
- Em dash reflexes.
- Curly quotation marks in plain Markdown docs.

Replacement rule: use prose by default. Use lists and tables only when they make comparison easier.

### 9. Citation and markup residue

Remove tool artifacts and verify every reference marker before returning:

- `contentReference`
- `oaicite`
- `oai_citation`
- `turn0search`
- `[cite: 1]`
- `[attached_file:1]`
- `utm_source=chatgpt.com`
- `utm_source=openai`
- `grok_card`
- `grok_render_citation_card_json`
- `attributableIndex`
- `writing{variant=`

Replacement rule: either provide a real citation the user supplied, preserve an existing real citation, or omit the marker.

### 10. Defensive AI-use prose

Do not include long assurances of quality, neutrality, policy compliance, good faith, or willingness to accept feedback unless the user specifically asked for a response letter and the context requires it.

Replacement rule: demonstrate quality through the rewrite. Do not narrate virtue.

## Final Humanizer Questions

Before returning a substantial rewrite, ask:

1. Did I add importance where the source gave only a fact?
2. Did I use a stock transition when a plain conjunction would do?
3. Did I over-organize the answer into neat sections, bullets, or three-part rhythm?
4. Did I repeat any phrase because it sounds polished rather than because it is true?
5. Did I leave any chatbot residue, placeholder, hidden marker, or citation artifact?
6. Would a careful reader know what changed in the world after reading each paragraph?

If the answer to any of these is yes, revise once more.
