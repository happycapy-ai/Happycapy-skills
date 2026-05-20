#!/usr/bin/env python3
"""Batch generate images from a list of prompts."""

import argparse
import json
import os
import sys
import time
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


def generate_image(prompt, model, output_path):
    """Generate a single image."""
    api_key = check_api_key()
    api_base = os.environ.get('AI_GATEWAY_BASE_URL', 'https://ai-gateway.happycapy.ai') + '/api/v1'

    payload = {
        'model': model,
        'prompt': prompt,
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
            result = json.loads(response.read().decode('utf-8'))

        if 'data' not in result or not result['data']:
            return None, 'No image data in response'

        image_url = result['data'][0].get('url')
        if not image_url:
            return None, 'No URL in response'

        # Download image
        download_req = request.Request(
            image_url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)'}
        )
        with request.urlopen(download_req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())

        return output_path, None

    except HTTPError as e:
        error_body = e.read().decode('utf-8')
        return None, f'HTTP Error {e.code}: {error_body}'
    except URLError as e:
        return None, f'Network Error: {e.reason}'
    except Exception as e:
        return None, str(e)


def read_prompts(file_path):
    """Read prompts from file, one per line."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prompts = [line.strip() for line in f if line.strip()]
        return prompts
    except Exception as e:
        print(f'Error reading prompts file: {str(e)}', file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Batch generate images from a list of prompts'
    )
    parser.add_argument(
        'prompts_file',
        help='Text file with one prompt per line'
    )
    parser.add_argument(
        '--model',
        default='google/gemini-3.1-flash-image-preview',
        help='Model to use (default: google/gemini-3.1-flash-image-preview)'
    )
    parser.add_argument(
        '--output-dir',
        default='batch_output',
        help='Output directory (default: batch_output)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )

    args = parser.parse_args()

    # Read prompts
    prompts = read_prompts(args.prompts_file)
    if not prompts:
        print('Error: No prompts found in file', file=sys.stderr)
        sys.exit(1)

    print(f'Found {len(prompts)} prompt(s)')
    print(f'Model: {args.model}')
    print(f'Output directory: {args.output_dir}')
    print()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate images for each prompt
    results = []

    for i, prompt in enumerate(prompts, 1):
        print(f'[{i}/{len(prompts)}] Processing: {prompt[:60]}...')

        output_path = output_dir / f'image_{i:03d}.png'

        result_path, error = generate_image(prompt, args.model, output_path)

        if error:
            print(f'  ✗ Failed: {error}')
            results.append({'prompt': prompt, 'status': 'failed', 'error': error})
        else:
            print(f'  ✓ Saved to: {result_path}')
            results.append({'prompt': prompt, 'status': 'success', 'path': str(result_path)})

        # Delay between requests
        if i < len(prompts):
            time.sleep(args.delay)

    # Summary
    print()
    print('=' * 60)
    print('BATCH GENERATION SUMMARY')
    print('=' * 60)

    successful = sum(1 for r in results if r['status'] == 'success')
    failed = len(results) - successful

    print(f'Total: {len(results)}')
    print(f'Successful: {successful}')
    print(f'Failed: {failed}')

    if failed > 0:
        print()
        print('Failed prompts:')
        for result in results:
            if result['status'] == 'failed':
                print(f"  - {result['prompt'][:60]}...")
                print(f"    Error: {result['error']}")

    # Save results log
    log_path = output_dir / 'batch_results.json'
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print()
    print(f'Results log saved to: {log_path}')


if __name__ == '__main__':
    main()
