#!/usr/bin/env python3
"""
AI Gateway Client for HappyCapy

Unified interface for calling LLM via AI Gateway
"""

import os
import json
import requests
from typing import List, Dict, Optional


class AIGatewayClient:
    """Client for HappyCapy AI Gateway"""

    def __init__(self):
        self.api_key = os.environ.get("AI_GATEWAY_API_KEY")
        if not self.api_key:
            raise ValueError("AI_GATEWAY_API_KEY not found in environment")

        self.base_url = "https://ai-gateway.happycapy.ai/api/v1"
        self.default_model = "gpt-4"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Origin": "https://trickle.so",
            "User-Agent": "Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)"
        }

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        stream: bool = False,
        timeout: int = 90
    ) -> Dict:
        """
        Send a chat completion request

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (default: gpt-4)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stream: Enable streaming
            timeout: Request timeout in seconds (default: 90s, increased for complex operations)

        Returns:
            Response dict with choices and usage info

        Raises:
            requests.exceptions.RequestException: On API errors
        """

        model = model or self.default_model

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=timeout,
                stream=stream
            )
            response.raise_for_status()

            if stream:
                return response  # Return response object for streaming
            else:
                return response.json()

        except requests.exceptions.Timeout:
            raise Exception(f"Request timeout after {timeout}s")
        except requests.exceptions.HTTPError as e:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('error', {}).get('message', str(e))
            raise Exception(f"API Error: {error_msg}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    def simple_prompt(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """
        Simple prompt-response interface

        Args:
            prompt: User prompt
            system: Optional system message
            model: Model name
            max_tokens: Maximum tokens
            temperature: Sampling temperature

        Returns:
            Generated text content
        """

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.chat_completion(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response['choices'][0]['message']['content']

    def stream_prompt(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 1024
    ):
        """
        Stream a prompt response

        Args:
            prompt: User prompt
            system: Optional system message
            model: Model name
            max_tokens: Maximum tokens

        Yields:
            Content chunks as they arrive
        """

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.chat_completion(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            stream=True
        )

        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                if line_text.startswith('data: '):
                    data = line_text[6:]
                    if data.strip() == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data)
                        content = chunk['choices'][0]['delta'].get('content', '')
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue


def create_client() -> AIGatewayClient:
    """Create and return an AI Gateway client"""
    return AIGatewayClient()


if __name__ == "__main__":
    # Test the client
    print("Testing AI Gateway Client...")
    print("=" * 60)

    try:
        client = create_client()

        # Test simple prompt
        print("\n1. Testing simple prompt:")
        response = client.simple_prompt("Say 'Hello, HappyCapy!'")
        print(f"   Response: {response}")

        # Test streaming
        print("\n2. Testing streaming:")
        print("   Response: ", end="", flush=True)
        for chunk in client.stream_prompt("Count from 1 to 5"):
            print(chunk, end="", flush=True)
        print()

        # Test with system message
        print("\n3. Testing with system message:")
        response = client.simple_prompt(
            "What's 2+2?",
            system="You are a math tutor. Answer concisely."
        )
        print(f"   Response: {response}")

        print("\n" + "=" * 60)
        print("✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
