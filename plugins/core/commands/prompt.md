---
description: Organize messy speech-to-text into a clean, structured prompt
argument-hint: "[your speech-to-text input]"
allowed-tools: Bash(echo:*)
---

## Your task

Transform the following raw speech-to-text input into a clean, well-organized prompt in English.

**Raw input:** $ARGUMENTS

## Rules

1. **Translate** to English if the input is in Spanish or mixed
2. **Remove** filler words (um, uh, este, eee, verdad, like, you know, pues, nada, etc.)
3. **Remove** false starts, repetitions, and thinking-out-loud artifacts
4. **Reorganize** ideas by grouping related concepts together, even if they were scattered throughout the input
5. **Preserve** the user's original intent and meaning exactly — do NOT add suggestions, constraints, context, or ideas that weren't explicitly stated
6. **Do NOT** embellish, expand, or "improve" the content — only clean and reorganize what was said

## Output structure

Organize the prompt using this format when applicable:

1. **Title**: A clear, descriptive header for the task
2. **Sections with headers**: Group related ideas under descriptive headers (e.g., "Context", "Requirements", "UI Design", "Process")
3. **Numbered lists**: For sequential steps or ordered processes
4. **Bullet points**: For features, characteristics, or non-sequential items
5. **Logical flow**: Context/setup first, then specifications, then process/steps

Keep sections minimal — only create headers when there are genuinely distinct topics to separate.

## Output format

Return ONLY the cleaned prompt. No explanations, no preamble, no "Here's your prompt:", no markdown code blocks wrapping the entire output. Just output the organized prompt directly.

After outputting the prompt, silently copy it to clipboard using:
```bash
echo "THE_CLEAN_PROMPT" | pbcopy
```

## Important

- This is a stateless operation — treat each invocation as completely independent
- Your only job is to be a translator/organizer, not a prompt engineer
- If something is ambiguous in the input, keep it ambiguous in the output — do not assume or clarify