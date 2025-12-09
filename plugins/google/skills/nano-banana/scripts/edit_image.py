#!/usr/bin/env python3
"""
Edit images using Nano Banana (Gemini Image) API.

Usage:
    python edit_image.py input.jpg "Add a hat to the person" --output edited.png
    python edit_image.py photo.png "Change background to beach sunset" --model pro
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

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
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


def get_mime_type(file_path: Path) -> str:
    """Get MIME type from file extension."""
    ext = file_path.suffix.lower()
    if ext not in MIME_TYPES:
        print(f"Error: Unsupported file format '{ext}'")
        print(f"Supported formats: {', '.join(MIME_TYPES.keys())}")
        sys.exit(1)
    return MIME_TYPES[ext]


def edit_image(
    image_path: str,
    edit_prompt: str,
    model: str = "pro",
    aspect_ratio: str = None,
    resolution: str = None,
) -> tuple[bytes, str]:
    """
    Edit an image using a text prompt.
    
    Args:
        image_path: Path to the input image
        edit_prompt: Text description of the edit to make
        model: "flash" for Nano Banana or "pro" for Nano Banana Pro
        aspect_ratio: Output aspect ratio (e.g., "16:9")
        resolution: Output resolution ("1K", "2K", "4K")
    
    Returns:
        Tuple of (edited_image_bytes, description_text)
    """
    api_key = get_api_key()
    model_id = MODELS.get(model, MODELS["flash"])
    
    # Read and encode the input image
    image_file = Path(image_path)
    if not image_file.exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    # Check file size (max 5MB)
    file_size = image_file.stat().st_size
    if file_size > 5 * 1024 * 1024:
        print(f"Error: Image file too large ({file_size / 1024 / 1024:.1f}MB). Max size is 5MB.")
        sys.exit(1)
    
    mime_type = get_mime_type(image_file)
    image_data = base64.b64encode(image_file.read_bytes()).decode("utf-8")
    
    # Build request payload
    payload = {
        "contents": [{
            "parts": [
                {"text": edit_prompt},
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": image_data
                    }
                }
            ]
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
    result_image = None
    description = ""
    
    try:
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "text" in part:
                description = part["text"]
            elif "inlineData" in part:
                result_image = base64.b64decode(part["inlineData"]["data"])
    except (KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        print(json.dumps(data, indent=2))
        sys.exit(1)
    
    if not result_image:
        print("Error: No image data in response")
        print(json.dumps(data, indent=2))
        sys.exit(1)
    
    return result_image, description


def main():
    parser = argparse.ArgumentParser(
        description="Edit images using Nano Banana (Gemini) API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python edit_image.py photo.jpg "Add a wizard hat" --output wizard.png
    python edit_image.py room.png "Change the sofa to blue" --model pro
    python edit_image.py portrait.jpg "Apply oil painting style" --aspect 3:4
    
Edit prompt tips:
    - Adding elements: "Add a [element] to [location]"
    - Removing elements: "Remove the [element] from the image"
    - Style transfer: "Apply [style] to this image"
    - Color changes: "Change the [object] color to [color]"
    - Background: "Replace the background with [description]"
        """
    )
    parser.add_argument("image", help="Path to the input image")
    parser.add_argument("prompt", help="Text description of the edit to make")
    parser.add_argument(
        "--output", "-o",
        default="edited_image.png",
        help="Output filename (default: edited_image.png)"
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
    
    args = parser.parse_args()
    
    # Validate 4K resolution requires Pro model
    if args.resolution == "4K" and args.model != "pro":
        print("Warning: 4K resolution requires Pro model. Switching to Pro.")
        args.model = "pro"
    
    print(f"Editing image with {MODELS[args.model]}...")
    print(f"Input: {args.image}")
    print(f"Edit: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    
    image_data, description = edit_image(
        image_path=args.image,
        edit_prompt=args.prompt,
        model=args.model,
        aspect_ratio=args.aspect,
        resolution=args.resolution,
    )
    
    # Save image
    output_path = Path(args.output)
    output_path.write_bytes(image_data)
    
    print(f"\n✓ Edited image saved to: {output_path.absolute()}")
    if description:
        print(f"\nDescription: {description}")


if __name__ == "__main__":
    main()
