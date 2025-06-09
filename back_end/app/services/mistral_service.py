from mistralai import Mistral, SDKError
from dotenv import load_dotenv

import time 
import os 
from typing import Any, Dict, List, Tuple
import asyncio

class MistralService:
    def __init__(
        self,
        model_name: str | None = None,
        api_key: str | None = None,
        api_base: str | None = None,
    ):
        load_dotenv()
        self.model_name = (
            model_name
            or ("mistral-medium")
        )

        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        self.client = Mistral(api_key=self.api_key)


    async def chat_complete_async(
            self,
            messages: List[Dict[str, str]],
            temperature: float = 0.1,
            max_tokens: int | None = 4000,
            retries: int = 5,
            backoff: float = 2.0
            ):
        
        for attempt in range(retries):
            try:
                resp = await self.client.chat.complete_async(
                    model       = self.model_name,
                    messages    = messages,
                    temperature = temperature,
                    max_tokens  = max_tokens,
                )

                return resp

            except SDKError as e:
                await asyncio.sleep(backoff)

        raise RuntimeError("Rate-limit retry failed")
    
    async def generate_response(
            self, 
            messages: List[Dict[str, str]],
            temperature: float = 0.7,
            max_tokens: int = 2000
        ):
        """
        Generate a response to a user prompt using the Mistral API asynchronously.
        
        Args:
            prompt: The user's question or input
            system_prompt: Instructions for the model
            temperature: Controls randomness (0-1)
            max_tokens: Maximum length of response
            
        Returns:
            The generated response text
        """
        
        try:
            response = await self.chat_complete_async(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"


