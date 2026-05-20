#!/usr/bin/env python3
"""Transform existing images using AI Gateway API."""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError


def check_api_key():
    """Check if API key is set in environment."""
    api_key = os.environ.get('AI_GATEWAY_API_KEY')
    if not api_key:
        print('Error: AI_GATEWAY_API_KEY environment variable is required.', file=sys.stderr)
        print('Please set it with your AI Gateway API key:', file=sys.stderr)
        print('  export AI_GATEWAY_API_KEY="your-api-key-here"', file=sys.stderr)
        sys.exit(1)
    return api_key


def transform_image(prompt, image_urls, model='google/gemini-3.1-flash-image-preview'):
    """
    Transform images using AI Gateway API.

    Args:
        prompt: Text instructions for image transformation
        image_urls: List of reference image URLs
        model: AI model to use for transformation

    Returns:
        dict: API response containing transformed image data
    """
    api_key = check_api_key()
    api_base = os.environ.get('AI_GATEWAY_BASE_URL', 'https://ai-gateway.happycapy.ai') + '/api/v1'

    payload = {
        'model': model,
        'prompt': prompt,
        'images': image_urls if isinstance(image_urls, list) else [image_urls],
        'response_format': 'url',
        'n': 1
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'Origin': 'https://trickle.so',
        'User-Agent': 'Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)'
    }

    try:
        req = request.Request(
            f'{api_base}/images/generations',
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))

    except HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f'HTTP Error {e.code}: {error_body}', file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f'Network Error: {e.reason}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        sys.exit(1)


def download_image(url, output_path):
    """Download image from URL to local file."""
    try:
        req = request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)'}
        )
        with request.urlopen(req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f'Error downloading image: {str(e)}', file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Transform images using AI Gateway image-to-image API'
    )
    parser.add_argument(
        'prompt',
        help='Text instructions for how to transform the image'
    )
    parser.add_argument(
        'image_urls',
        nargs='+',
        help='One or more reference image URLs to transform'
    )
    parser.add_argument(
        '--model',
        default='google/gemini-3.1-flash-image-preview',
        help='Model to use (default: google/gemini-3.1-flash-image-preview)'
    )
    parser.add_argument(
        '--output',
        default='transformed_image.png',
        help='Output file path (default: transformed_image.png)'
    )

    args = parser.parse_args()

    print(f'Transforming image(s) with model: {args.model}')
    print(f'Prompt: {args.prompt}')
    print(f'Reference image(s): {", ".join(args.image_urls)}')
    print('Please wait...')

    result = transform_image(args.prompt, args.image_urls, args.model)

    if 'data' not in result or not result['data']:
        print('Error: No image data in response', file=sys.stderr)
        sys.exit(1)

    image_data = result['data'][0]
    image_url = image_data.get('url')

    if not image_url:
        print('Error: No URL in response', file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)

    print(f'Downloading to: {output_path}')

    if download_image(image_url, output_path):
        print(f'✓ Transformed image saved successfully to {output_path.absolute()}')
    else:
        print(f'✗ Failed to download image')
        sys.exit(1)


if __name__ == '__main__':
    main()
