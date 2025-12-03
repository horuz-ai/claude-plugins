---
description: Translate and organize Spanish voice-to-text into clear English prompts
argument-hint: "[your Spanish voice input]"
---

# Voice Prompt Translator

You are receiving raw Spanish speech-to-text input that needs to be translated to English and organized for clarity.

## Input
$ARGUMENTS

## Your Task

Translate the above Spanish text to English and organize it for readability. Follow these rules strictly:

### What you MUST do:
1. Translate from Spanish to English accurately
2. Remove filler words and verbal hesitations (um, uh, like, you know, etc.)
3. Remove personal reactions and opinions that don't affect the actual request (e.g., "I love this", "I think we're good", "that's great", "perfect")
4. Organize the content logically with clear paragraph breaks
5. Use bullet points ONLY when listing multiple distinct items or requirements
6. Keep the natural, conversational tone — this should sound like the person speaking, just cleaner and more direct

### What you MUST NOT do:
- Do NOT remove any technical details, requirements, context, or constraints
- Do NOT remove reasoning or explanations that clarify WHY something should be done
- Do NOT add information that wasn't in the original
- Do NOT make it sound robotic or overly formal
- Do NOT add explanations, summaries, or meta-commentary
- Do NOT use headers, titles, or excessive formatting

### Key distinction:
- REMOVE: Personal reactions, pleasantries, self-reassurances ("me encanta", "estamos bien", "perfecto", "gracias")
- KEEP: All details about WHAT to do, HOW to do it, WHY to do it, and any CONSTRAINTS or CONTEXT

## Output Format

Output ONLY the translated and organized English text. Nothing else — no preamble, no "Here's the translation:", no explanations. Just the clean prompt ready to be used.