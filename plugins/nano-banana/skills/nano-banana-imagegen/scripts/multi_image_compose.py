#!/usr/bin/env python3
"""
Compose multiple images using Nano Banana Pro (Gemini 3 Pro Image) API.

This script uses the Pro model which supports up to 14 reference images:
- Up to 6 object images (high-fidelity)
- Up to 5 human images (character consistency)

Usage:
    python multi_image_compose.py "Create a group photo" img1.jpg img2.jpg img3.jpg --output composed.png
    python multi_image_compose.py "Show person A in location B with style C" personA.jpg locationB.jpg styleC.jpg
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


API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

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


def load_image(image_path: str) -> tuple[str, str]:
    """
    Load an image and return base64 data and MIME type.
    
    Returns:
        Tuple of (base64_data, mime_type)
    """
    image_file = Path(image_path)
    if not image_file.exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    # Check file size (max 5MB)
    file_size = image_file.stat().st_size
    if file_size > 5 * 1024 * 1024:
        print(f"Error: Image file too large ({file_size / 1024 / 1024:.1f}MB): {image_path}")
        print("Max size is 5MB per image.")
        sys.exit(1)
    
    mime_type = get_mime_type(image_file)
    image_data = base64.b64encode(image_file.read_bytes()).decode("utf-8")
    
    return image_data, mime_type


def compose_images(
    prompt: str,
    image_paths: list[str],
    aspect_ratio: str = None,
    resolution: str = None,
    use_search: bool = False,
) -> tuple[bytes, str]:
    """
    Compose multiple images into a new image.
    
    Args:
        prompt: Text description of how to compose the images
        image_paths: List of paths to input images (max 14)
        aspect_ratio: Output aspect ratio (e.g., "16:9")
        resolution: Output resolution ("1K", "2K", "4K")
        use_search: Enable Google Search grounding
    
    Returns:
        Tuple of (composed_image_bytes, description_text)
    """
    api_key = get_api_key()
    
    # Validate image count
    if len(image_paths) > 14:
        print(f"Warning: Maximum 14 images supported. Using first 14 of {len(image_paths)} images.")
        image_paths = image_paths[:14]
    
    if len(image_paths) < 1:
        print("Error: At least one image is required.")
        sys.exit(1)
    
    # Build parts list with prompt and images
    parts = [{"text": prompt}]
    
    for i, img_path in enumerate(image_paths, 1):
        print(f"  Loading image {i}/{len(image_paths)}: {img_path}")
        img_data, mime_type = load_image(img_path)
        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": img_data
            }
        })
    
    # Build request payload
    payload = {
        "contents": [{
            "parts": parts
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
    
    # Add Google Search grounding if requested
    if use_search:
        payload["tools"] = [{"google_search": {}}]
    
    # Make API request
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    print("\nSending request to Nano Banana Pro API...")
    response = requests.post(API_URL, headers=headers, json=payload, timeout=180)
    
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
            # Skip thought parts
            if part.get("thought"):
                continue
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
        description="Compose multiple images using Nano Banana Pro API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script uses Nano Banana Pro which supports up to 14 reference images:
- Up to 6 object images (high-fidelity preservation)
- Up to 5 human images (character consistency)

Examples:
    # Group photo with character consistency
    python multi_image_compose.py "An office group photo, everyone making funny faces" \\
        person1.jpg person2.jpg person3.jpg --output team.png

    # Style transfer with multiple references
    python multi_image_compose.py "Use Image 1 for the character's pose, Image 2 for the art style" \\
        pose_ref.jpg style_ref.jpg --output styled.png

    # Product composition
    python multi_image_compose.py "Place the product on this background with this lighting" \\
        product.png background.jpg lighting_ref.jpg --aspect 16:9

Prompt tips for multi-image:
    - Reference images by order: "Image 1 for pose, Image 2 for style"
    - Be explicit about each image's role
    - Describe the desired composition clearly
        """
    )
    parser.add_argument("prompt", help="Text description of how to compose the images")
    parser.add_argument("images", nargs="+", help="Paths to input images (2-14 images)")
    parser.add_argument(
        "--output", "-o",
        default="composed_image.png",
        help="Output filename (default: composed_image.png)"
    )
    parser.add_argument(
        "--aspect", "-a",
        choices=ASPECT_RATIOS,
        help="Aspect ratio (e.g., 16:9, 1:1)"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=RESOLUTIONS,
        default="2K",
        help="Resolution: 1K, 2K, or 4K (default: 2K)"
    )
    parser.add_argument(
        "--search", "-s",
        action="store_true",
        help="Enable Google Search grounding for real-time info"
    )
    
    args = parser.parse_args()
    
    print(f"Composing {len(args.images)} images with Nano Banana Pro...")
    print(f"Prompt: {args.prompt[:100]}{'...' if len(args.prompt) > 100 else ''}")
    print(f"Resolution: {args.resolution}")
    if args.aspect:
        print(f"Aspect ratio: {args.aspect}")
    
    image_data, description = compose_images(
        prompt=args.prompt,
        image_paths=args.images,
        aspect_ratio=args.aspect,
        resolution=args.resolution,
        use_search=args.search,
    )
    
    # Save image
    output_path = Path(args.output)
    output_path.write_bytes(image_data)
    
    print(f"\n✓ Composed image saved to: {output_path.absolute()}")
    if description:
        print(f"\nDescription: {description}")


if __name__ == "__main__":
    main()
