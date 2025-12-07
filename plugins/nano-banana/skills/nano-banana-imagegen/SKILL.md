---
name: nano-banana-imagegen
description: AI image generation and editing using Google's Nano Banana (Gemini 2.5 Flash Image) and Nano Banana Pro (Gemini 3 Pro Image) APIs. Use this skill when the user wants to generate, edit, or compose images using AI. Triggers include requests to create images from text descriptions, edit existing images, add/remove elements from photos, apply style transfers, maintain character consistency across images, generate images with text overlays (logos, posters, infographics), or create multi-image compositions. Also use when users mention "Nano Banana", "Gemini image", or want AI-generated visuals.
---

# Nano Banana Image Generation Skill

Generate and edit images using Google's Nano Banana (Gemini 2.5 Flash Image) and Nano Banana Pro (Gemini 3 Pro Image) APIs.

## Model Selection

| Model | ID | Best For | Resolution | Cost |
|-------|-----|----------|------------|------|
| **Nano Banana** | `gemini-2.5-flash-image` | Fast generation, iteration, basic edits | Up to 1024px | ~$0.039/image |
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | Professional assets, text rendering, complex compositions | Up to 4K | Higher cost |

**Selection Guide:**
- Use **Nano Banana** for: rapid prototyping, simple edits, high-volume generation
- Use **Nano Banana Pro** for: text in images, 4K output, up to 14 reference images, Google Search grounding

## Core Capabilities

1. **Text-to-Image**: Generate images from text descriptions
2. **Image Editing**: Add, remove, modify elements in existing images
3. **Multi-Image Composition**: Blend up to 14 images (Pro only)
4. **Character Consistency**: Maintain same character across multiple generations
5. **Text Rendering**: Generate legible text in images (Pro excels here)
6. **Style Transfer**: Apply artistic styles to images
7. **Iterative Refinement**: Conversational multi-turn editing

## Quick Start

### Generate an Image

```bash
python scripts/generate_image.py "A cozy coffee shop interior with warm lighting" --output coffee_shop.png
```

### Edit an Image

```bash
python scripts/edit_image.py input.jpg "Add a cat sitting on the chair" --output output.png
```

## Prompting Best Practices

**Core Principle: Describe the scene, don't just list keywords.**

The model understands natural language narratives better than comma-separated tags.

### Prompt Structure (for best results)

Include these elements in your prompts:

1. **Subject**: Who/what is in the image (be specific)
2. **Action**: What is happening
3. **Environment/Location**: Setting and context
4. **Lighting**: Natural, studio, golden hour, etc.
5. **Style**: Photorealistic, illustration, watercolor, etc.
6. **Composition**: Camera angle, framing, perspective
7. **Mood/Atmosphere**: Emotional tone

### Example - Good vs Bad Prompts

**Bad**: `cat, hat, wizard, cute`

**Good**: `A fluffy ginger cat wearing a tiny knitted wizard hat, sitting on a wooden floor in a cozy living room. Soft natural light streams through a nearby window, creating a warm, magical atmosphere. Photorealistic, shot with an 85mm portrait lens.`

For comprehensive prompting strategies, see: `references/prompting-guide.md`

## API Configuration

### Required Environment Variable

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key from: https://aistudio.google.com/apikey

### Response Modalities

Always set `responseModalities: ["TEXT", "IMAGE"]` to receive generated images.

### Image Configuration Options

```python
image_config = {
    "aspect_ratio": "16:9",  # Options: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
    "image_size": "2K"       # Options: 1K, 2K, 4K (Pro only for 4K)
}
```

For complete API reference, see: `references/api-reference.md`

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/generate_image.py` | Text-to-image generation |
| `scripts/edit_image.py` | Edit existing images with text prompts |
| `scripts/multi_image_compose.py` | Compose multiple images (Pro only) |

## Important Notes

- All generated images include invisible SynthID watermarks
- Pro model uses "thinking" mode for complex prompts (enabled by default)
- For multi-turn editing, maintain conversation history
- Supported input formats: JPEG, PNG, WebP (up to 5MB)
- For best performance use languages: EN, es-MX, ja-JP, zh-CN, hi-IN
