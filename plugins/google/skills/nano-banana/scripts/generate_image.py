#!/usr/bin/env python3
"""
Generate images from text prompts using Nano Banana (Gemini Image) API.

Usage:
    python generate_image.py "Your prompt here" --output image.png
    python generate_image.py "Your prompt" --model pro --aspect 16:9 --resolution 2K
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests --break-system-packages -q")
    import requests


API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
RESOLUTIONS = ["1K", "2K", "4K"]


def get_api_key():
    """Get API key from environment variable."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Get your API key from: https://aistudio.google.com/apikey")
        print("Then run: export GEMINI_API_KEY='your-key-here'")
        sys.exit(1)
    return api_key


def generate_image(
    prompt: str,
    model: str = "flash",
    aspect_ratio: str = None,
    resolution: str = None,
    use_search: bool = False,
) -> tuple[bytes, str]:
    """
    Generate an image from a text prompt.
    
    Args:
        prompt: Text description of the image to generate
        model: "flash" for Nano Banana or "pro" for Nano Banana Pro
        aspect_ratio: Output aspect ratio (e.g., "16:9")
        resolution: Output resolution ("1K", "2K", "4K")
        use_search: Enable Google Search grounding (Pro only)
    
    Returns:
        Tuple of (image_bytes, description_text)
    """
    api_key = get_api_key()
    model_id = MODELS.get(model, MODELS["flash"])
    
    # Build request payload
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }
    
    # Add image config if specified
    if aspect_ratio or resolution:
        payload["generationConfig"]["imageConfig"] = {}
        if aspect_ratio:
            payload["generationConfig"]["imageConfig"]["aspectRatio"] = aspect_ratio
        if resolution:
            payload["generationConfig"]["imageConfig"]["imageSize"] = resolution
    
    # Add Google Search grounding (Pro only)
    if use_search and model == "pro":
        payload["tools"] = [{"google_search": {}}]
    
    # Make API request
    url = API_URL.format(model=model_id)
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    
    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    data = response.json()
    
    # Extract image and text from response
    image_data = None
    description = ""
    
    try:
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "text" in part:
                description = part["text"]
            elif "inlineData" in part:
                image_data = base64.b64decode(part["inlineData"]["data"])
    except (KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        print(json.dumps(data, indent=2))
        sys.exit(1)
    
    if not image_data:
        print("Error: No image data in response")
        print(json.dumps(data, indent=2))
        sys.exit(1)
    
    return image_data, description


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Nano Banana (Gemini) API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python generate_image.py "A cozy coffee shop" --output coffee.png
    python generate_image.py "Modern logo for TechCorp" --model pro --aspect 1:1
    python generate_image.py "Current weather in NYC as infographic" --model pro --search
        """
    )
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument(
        "--output", "-o",
        default="generated_image.png",
        help="Output filename (default: generated_image.png)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["flash", "pro"],
        default="flash",
        help="Model to use: flash (fast) or pro (high quality)"
    )
    parser.add_argument(
        "--aspect", "-a",
        choices=ASPECT_RATIOS,
        help="Aspect ratio (e.g., 16:9, 1:1)"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=RESOLUTIONS,
        help="Resolution: 1K, 2K, or 4K (4K requires pro model)"
    )
    parser.add_argument(
        "--search", "-s",
        action="store_true",
        help="Enable Google Search grounding (Pro model only)"
    )
    
    args = parser.parse_args()
    
    # Validate 4K resolution requires Pro model
    if args.resolution == "4K" and args.model != "pro":
        print("Warning: 4K resolution requires Pro model. Switching to Pro.")
        args.model = "pro"
    
    print(f"Generating image with {MODELS[args.model]}...")
    print(f"Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    
    image_data, description = generate_image(
        prompt=args.prompt,
        model=args.model,
        aspect_ratio=args.aspect,
        resolution=args.resolution,
        use_search=args.search,
    )
    
    # Save image
    output_path = Path(args.output)
    output_path.write_bytes(image_data)
    
    print(f"\n✓ Image saved to: {output_path.absolute()}")
    if description:
        print(f"\nDescription: {description}")


if __name__ == "__main__":
    main()
