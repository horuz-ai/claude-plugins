# Nano Banana API Reference

Technical reference for the Gemini Image Generation API.

## Authentication

### API Key Setup

Get your API key from: https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Billing

API access requires billing setup on your Google Cloud project. Enable billing at: https://aistudio.google.com

**Pricing (approximate):**
- Nano Banana: ~$0.039 per image (~1,290 tokens per 1024x1024 image)
- Nano Banana Pro: Higher cost, varies by resolution

## Models

| Model Name | Model ID | Max Resolution | Features |
|------------|----------|----------------|----------|
| Nano Banana | `gemini-2.5-flash-image` | 1024px | Fast, efficient, basic editing |
| Nano Banana Pro | `gemini-3-pro-image-preview` | 4096px (4K) | Text rendering, 14 images, Search grounding, Thinking mode |

## API Endpoints

### REST Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
```

### Headers

```
x-goog-api-key: {GEMINI_API_KEY}
Content-Type: application/json
```

## Request Format

### Basic Text-to-Image

```json
{
  "contents": [{
    "parts": [
      {"text": "Your image description here"}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

### Image Editing (with input image)

```json
{
  "contents": [{
    "parts": [
      {"text": "Edit instructions here"},
      {
        "inline_data": {
          "mime_type": "image/jpeg",
          "data": "{base64_encoded_image}"
        }
      }
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

### With Image Configuration

```json
{
  "contents": [{
    "parts": [
      {"text": "Your prompt"}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "2K"
    }
  }
}
```

## Configuration Options

### Response Modalities

**Required for image generation:**
```json
"responseModalities": ["TEXT", "IMAGE"]
```

### Image Configuration

| Parameter | Values | Description |
|-----------|--------|-------------|
| `aspectRatio` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` | Output aspect ratio |
| `imageSize` | `1K`, `2K`, `4K` | Output resolution (4K only for Pro) |

**Note:** Use uppercase 'K' (e.g., `1K`, not `1k`).

### Tools (Pro Only)

#### Google Search Grounding

```json
{
  "tools": [{"google_search": {}}]
}
```

Enables real-time information for generating images based on current events, weather, etc.

## Response Format

### Successful Response

```json
{
  "candidates": [{
    "content": {
      "parts": [
        {
          "text": "Description of generated image"
        },
        {
          "inlineData": {
            "mimeType": "image/png",
            "data": "{base64_encoded_image}"
          }
        }
      ]
    }
  }]
}
```

### Extracting Image Data

The image is returned as base64-encoded data in `candidates[0].content.parts[].inlineData.data`.

**Bash extraction:**
```bash
jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' response.json | base64 --decode > output.png
```

## Multi-Turn Conversations

For iterative editing, maintain conversation history:

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "Create a sunset beach scene"}]
    },
    {
      "role": "model",
      "parts": [
        {"text": "Here's a beautiful sunset beach scene"},
        {"inlineData": {"mimeType": "image/png", "data": "..."}}
      ]
    },
    {
      "role": "user",
      "parts": [{"text": "Add a sailboat on the horizon"}]
    }
  ]
}
```

## Thought Signatures (Pro Only)

Nano Banana Pro uses "thinking" mode. Responses may include `thought_signature` fields.

**Important:** When using multi-turn conversations with Pro, pass thought signatures back exactly as received.

If using official SDKs with chat features, thought signatures are handled automatically.

## Multi-Image Input (Pro Only)

Supports up to 14 reference images:
- Up to 6 object images (high-fidelity)
- Up to 5 human images (character consistency)

```json
{
  "contents": [{
    "parts": [
      {"text": "Create a group photo of these people"},
      {"inline_data": {"mime_type": "image/png", "data": "{image1_base64}"}},
      {"inline_data": {"mime_type": "image/png", "data": "{image2_base64}"}},
      {"inline_data": {"mime_type": "image/png", "data": "{image3_base64}"}}
    ]
  }]
}
```

## Supported Input Formats

| Format | MIME Type |
|--------|-----------|
| JPEG | `image/jpeg` |
| PNG | `image/png` |
| WebP | `image/webp` |

**Max file size:** 5MB per image

## Rate Limits

Rate limits vary by account tier and region. Check official documentation for current limits.

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 400 Bad Request | Invalid parameters | Check request format |
| 401 Unauthorized | Invalid API key | Verify GEMINI_API_KEY |
| 429 Too Many Requests | Rate limit exceeded | Implement backoff, check limits |
| 500 Server Error | API issue | Retry with exponential backoff |

## Python SDK Usage

### Installation

```bash
pip install google-genai --break-system-packages
```

### Basic Generation

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Your prompt here"],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("output.png")
```

### With Configuration

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["Your prompt"],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K"
        ),
    )
)
```

### Image Editing

```python
from PIL import Image

image_input = Image.open('input.jpg')

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Add a hat to the person", image_input],
)
```

### Multi-Turn Chat

```python
chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    )
)

response1 = chat.send_message("Create a mountain landscape")
response2 = chat.send_message("Add a cabin in the foreground")
response3 = chat.send_message("Change to winter scene with snow")
```

## cURL Examples

### Text-to-Image

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "A serene mountain lake at sunset"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 --decode > output.png
```

### With Aspect Ratio

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Your prompt"}]}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {"aspectRatio": "16:9"}
    }
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 --decode > output.png
```

## Best Languages for Performance

For optimal results, use:
- English (EN)
- Spanish Mexico (es-MX)
- Japanese (ja-JP)
- Chinese Simplified (zh-CN)
- Hindi (hi-IN)

## SynthID Watermarking

All generated images include invisible SynthID digital watermarks identifying them as AI-generated. This cannot be disabled.
