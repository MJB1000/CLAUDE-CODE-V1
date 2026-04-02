# Token Optimizer — Marketing Team Skill

Load this skill first, before any other file, at every session start.

---

## Five Rules

Apply these before every tool call and every response:

1. **Trust context.** If information is already in a skill, memory, or this session's context — do not re-read the source file.
2. **Kill speculation.** Do not generate content, options, or variations unless the brief explicitly asks for them. One version, done right.
3. **Parallelize.** If two file reads or tool calls are independent, run them in parallel.
4. **Route verbosity.** If a tool call will return more than 20 lines you will not directly use, route it to a subagent that returns a summary.
5. **Never restate.** Do not begin a response by summarizing what the user said, what the brief contains, or what the last agent wrote. Start with the work.

## File Access Rules

- Grep before Read. Never read a whole file to find one thing.
- Do not re-read files already in context this session.
- Use offset and limit when reading — never load a 500-line brand guide to find the CTA guidelines.

## Response Rules

- Lead with the deliverable, decision, or action — not the reasoning.
- If you can say it in one sentence, do not use three.
- Do not add preamble, transitions, or filler between sections.
- Do not echo back instructions, brief contents, or feedback before acting on them.
