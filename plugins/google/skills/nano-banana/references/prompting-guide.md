# Nano Banana Prompting Guide

Comprehensive guide for writing effective prompts to generate high-quality images.

## Fundamental Principle

> **Describe the scene, don't just list keywords.**

The model's strength is deep language understanding. Narrative paragraphs produce better results than keyword lists.

## Prompt Components

### 1. Subject (Who/What)

Be specific about the main subject.

| Vague | Specific |
|-------|----------|
| a robot | a stoic robot barista with glowing blue optics |
| a cat | a fluffy calico cat wearing a tiny wizard hat |
| a person | an elderly Japanese ceramicist with sun-etched wrinkles |

### 2. Action (What's Happening)

Describe the activity or state.

- "brewing a cup of coffee"
- "casting a magical spell"
- "carefully inspecting a freshly glazed tea bowl"
- "mid-stride running through a field"

### 3. Environment/Location

Set the scene and context.

- "in a rustic, sun-drenched workshop"
- "on a polished concrete surface in a modern studio"
- "in a fancy restaurant under the Gemini constellation"

### 4. Lighting

Photography-inspired lighting descriptions.

| Type | Description |
|------|-------------|
| Natural | "soft, golden hour light streaming through a window" |
| Studio | "three-point softbox setup with soft, diffused highlights" |
| Dramatic | "high-contrast lighting with deep shadows" |
| Ambient | "warm candlelight creating an intimate atmosphere" |

### 5. Style

Specify the visual style explicitly.

**Photography Styles:**
- Photorealistic, documentary, editorial, fashion, product photography

**Artistic Styles:**
- Watercolor, oil painting, digital art, anime, pixel art
- Kawaii-style, cel-shading, ink illustration
- Da Vinci anatomical sketch, noir art style

**Design Styles:**
- Minimalist, brutalist, art deco, cyberpunk, retro

### 6. Camera/Composition

Use photography terminology.

| Term | Effect |
|------|--------|
| Close-up / Macro | Detailed, intimate shots |
| Wide-angle shot | Expansive scenes, environment focus |
| 85mm portrait lens | Shallow depth of field, bokeh |
| Low-angle perspective | Dramatic, powerful subjects |
| Bird's eye view | Overview, patterns visible |
| Dutch angle | Dynamic, unsettling feeling |

### 7. Aspect Ratio

Specify the format for your output.

- **1:1** - Square (social media, profile pics)
- **16:9** - Widescreen (presentations, banners)
- **9:16** - Vertical (mobile, stories)
- **3:2** - Classic photo ratio
- **21:9** - Ultrawide cinematic

---

## Prompting Templates by Use Case

### Photorealistic Scenes

```
A photorealistic [shot type] of [subject], [action or expression], set in [environment]. 
The scene is illuminated by [lighting description], creating a [mood] atmosphere. 
Captured with a [camera/lens details], emphasizing [key textures and details]. 
The image should be in a [aspect ratio] format.
```

**Example:**
```
A photorealistic close-up portrait of an elderly Japanese ceramicist with deep, 
sun-etched wrinkles and a warm, knowing smile. He is carefully inspecting a freshly 
glazed tea bowl. The setting is his rustic, sun-drenched workshop. The scene is 
illuminated by soft, golden hour light streaming through a window, highlighting the 
fine texture of the clay. Captured with an 85mm portrait lens, resulting in a soft, 
blurred background (bokeh). The overall mood is serene and masterful.
```

### Stickers & Illustrations

```
A [style] sticker of a [subject], featuring [key characteristics] and a [color palette]. 
The design should have [line style] and [shading style]. The background must be [color/transparent].
```

**Example:**
```
A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat. It's munching 
on a green bamboo leaf. The design features bold, clean outlines, simple cel-shading, 
and a vibrant color palette. The background must be white.
```

### Logos & Text Graphics

```
Create a [style] logo for [brand/concept] with the text "[exact text]" in a [font style]. 
The design should be [style description], with a [color scheme]. [Additional design elements].
```

**Example:**
```
Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'. The text 
should be in a clean, bold, sans-serif font. The color scheme is black and white. 
Put the logo in a circle. Use a coffee bean in a clever way.
```

### Product Mockups

```
A high-resolution, studio-lit product photograph of a [product description] on a 
[background surface]. The lighting is a [lighting setup] to [lighting purpose]. 
The camera angle is a [angle type] to showcase [specific feature]. Ultra-realistic, 
with sharp focus on [key detail].
```

**Example:**
```
A high-resolution, studio-lit product photograph of a minimalist ceramic coffee mug 
in matte black, presented on a polished concrete surface. The lighting is a three-point 
softbox setup designed to create soft, diffused highlights and eliminate harsh shadows. 
The camera angle is a slightly elevated 45-degree shot to showcase its clean lines. 
Ultra-realistic, with sharp focus on the steam rising from the coffee. Square image.
```

### Minimalist/Negative Space

```
A minimalist composition featuring a single [subject] positioned in the [position] 
of the frame. The background is a vast, empty [color] canvas, creating significant 
negative space. [Lighting description].
```

**Example:**
```
A minimalist composition featuring a single, delicate red maple leaf positioned in 
the bottom-right of the frame. The background is a vast, empty off-white canvas, 
creating significant negative space for text. Soft, diffused lighting from the top left.
```

### Infographics & Diagrams

```
Create a vibrant infographic that explains [topic] as if it were [analogy]. 
Show the [components] and the [result]. The style should be [visual style], 
suitable for [audience].
```

**Example:**
```
Create a vibrant infographic that explains photosynthesis as if it were a recipe for 
a plant's favorite food. Show the "ingredients" (sunlight, water, CO2) and the 
"finished dish" (sugar/energy). The style should be like a page from a colorful 
kids' cookbook, suitable for a 4th grader.
```

### Sequential Art / Comics

```
Make a [number] panel comic in a [art style]. Put the character in a [scene type]. 
[Additional style details].
```

**Example:**
```
Make a 3 panel comic in a gritty, noir art style with high-contrast black and white inks. 
Put the character in a humorous scene.
```

---

## Editing Prompts

### Adding Elements

```
Using the provided image, please add [element] to [location]. 
Make it look [quality description] and match the [lighting/style] of the original.
```

### Removing Elements

```
Remove the [element] from this image while maintaining the background seamlessly.
```

### Style Transfer

```
Apply the style of [artistic reference] to this image while keeping the original 
subject intact.
```

### Local Edits

```
In this image, change only the [specific element] to [new state/color/style]. 
Do not modify any other elements.
```

---

## Multi-Image Composition (Pro Only)

When using multiple reference images:

```
Using Image A for [purpose], Image B for [purpose], and Image C for [purpose], 
create [final composition description].
```

**Example:**
```
Using Image A for the character's pose, Image B for the art style, and Image C for 
the background environment, create a fantasy scene of a warrior standing in a mystical forest.
```

### Character Consistency

For maintaining the same character across images:

```
An office group photo of these people [upload reference images], they are [action]. 
Maintain the exact appearance and features of each person.
```

---

## Advanced Tips

### Positive Framing

Instead of saying what you don't want, describe what you do want:

| Negative (Avoid) | Positive (Better) |
|------------------|-------------------|
| "no cars in the street" | "an empty, deserted street with no signs of traffic" |
| "don't make it blurry" | "sharp focus with crisp details" |
| "not too bright" | "soft, subdued lighting with gentle shadows" |

### Iterative Refinement

Use multi-turn conversation to refine:

1. Generate initial image
2. "Make the lighting warmer"
3. "Add more detail to the background"
4. "Change the aspect ratio to 16:9"

### Google Search Grounding (Pro Only)

For real-time information:

```
Visualize the current weather forecast for the next 5 days in [location] as a 
clean, modern weather chart.
```

```
Create a graphic showing last night's [sports team] game score in [competition].
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Text is garbled | Use Nano Banana Pro, spell out the text clearly in quotes |
| Character changes between images | Upload reference images, describe features explicitly |
| Wrong style applied | Be more specific about the style, use reference terms |
| Image too generic | Add more specific details about lighting, mood, textures |
| Composition is off | Specify camera angle, subject placement, aspect ratio |
