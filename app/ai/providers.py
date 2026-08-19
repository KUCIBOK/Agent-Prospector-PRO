"""
AI Provider abstraction — support for Ollama and future providers.

All AI decisions go through this abstraction so we can:
- Swap providers easily
- Log all AI interactions
- Enforce guardrails consistently
- Test with mock providers
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import json
import logging

import requests

from app.config import settings

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def analyze(self, payload: dict) -> dict:
        """Analyze data and return structured result."""
        pass

    @abstractmethod
    def extract(self, text: str, schema: dict) -> dict:
        """Extract structured data from text using schema."""
        pass

    @abstractmethod
    def classify(self, payload: dict) -> str:
        """Classify data into a category."""
        pass

    @abstractmethod
    def summarize(self, text: str, max_length: int = 200) -> str:
        """Summarize text."""
        pass


class OllamaProvider(AIProvider):
    """Local LLM provider using Ollama."""

    def __init__(self, model_name: str = settings.model_name, host: str = settings.ollama_host):
        self.model = model_name
        self.host = host
        self.endpoint = f"{host}/api/generate"
        logger.info(f"✅ Ollama provider initialized: {model_name} @ {host}")

    def _call_ollama(self, prompt: str, json_mode: bool = False) -> str:
        """Call Ollama API and return response."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": settings.model_temperature,
                "num_predict": settings.model_max_tokens,
            }

            response = requests.post(self.endpoint, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except Exception as e:
            logger.error(f"❌ Ollama API error: {str(e)}")
            raise

    def analyze(self, payload: dict) -> dict:
        """
        Analyze prospect data and return structured analysis.

        Guardrails:
        - Always use UNKNOWN for missing data
        - Never invent: emails, websites, exhibitions, relationships
        - All scores must be justified
        - Return valid JSON
        """
        analysis_type = payload.get("type", "general")
        data_summary = json.dumps(payload.get("data", {}), indent=2)

        prompt = f"""Analyze this prospect data and return a JSON response.

CRITICAL GUARDRAILS:
1. Use "UNKNOWN" for any missing or unconfirmed information
2. NEVER invent: emails, websites, exhibitions, past activities
3. NEVER claim relationships or activities not explicitly mentioned
4. All scores must be justified
5. Return ONLY valid JSON, no markdown or extra text

Data to analyze:
{data_summary}

For {analysis_type} analysis, return this JSON structure:
{{
  "classification": "...",
  "score": 0-100,
  "confidence": "LOW/MEDIUM/HIGH",
  "reasoning": "...",
  "missing_data": ["field1", "field2"],
  "warnings": []
}}

Remember: accuracy > speculation. UNKNOWN is better than wrong data."""

        response_text = self._call_ollama(prompt)

        # Parse JSON response
        try:
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text

            result = json.loads(json_str)
            return result

        except json.JSONDecodeError:
            logger.error(f"Failed to parse Ollama response as JSON: {response_text}")
            return {
                "classification": "UNKNOWN",
                "score": 0,
                "confidence": "LOW",
                "reasoning": "Failed to analyze",
                "missing_data": [],
                "warnings": ["JSON parsing failed"],
            }

    def extract(self, text: str, schema: dict) -> dict:
        """Extract structured data from text using schema."""
        prompt = f"""Extract data from the following text according to this schema.

GUARDRAILS:
- Use "UNKNOWN" for missing fields
- Do NOT invent information
- Only extract what is explicitly stated

Text:
{text}

Schema (required fields):
{json.dumps(schema, indent=2)}

Return ONLY valid JSON matching the schema:"""

        response_text = self._call_ollama(prompt)

        try:
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text

            return json.loads(json_str)

        except json.JSONDecodeError:
            logger.error(f"Failed to parse extraction response as JSON")
            return {field: "UNKNOWN" for field in schema.keys()}

    def classify(self, payload: dict) -> str:
        """Classify data into a category."""
        data_str = json.dumps(payload.get("data", {}))
        categories = payload.get("categories", [])

        prompt = f"""Classify this data into ONE of these categories: {', '.join(categories)}

Data:
{data_str}

Respond with ONLY the category name, nothing else."""

        response = self._call_ollama(prompt)
        return response.strip()

    def summarize(self, text: str, max_length: int = 200) -> str:
        """Summarize text to max_length."""
        prompt = f"""Summarize this text in {max_length} characters or less.

Text:
{text}

Summary (max {max_length} chars):"""

        response = self._call_ollama(prompt)
        return response.strip()[:max_length]


class MockProvider(AIProvider):
    """Mock provider for testing."""

    def analyze(self, payload: dict) -> dict:
        return {
            "classification": "TEST",
            "score": 75,
            "confidence": "MEDIUM",
            "reasoning": "Mock analysis",
            "missing_data": [],
            "warnings": [],
        }

    def extract(self, text: str, schema: dict) -> dict:
        return {field: "MOCK" for field in schema.keys()}

    def classify(self, payload: dict) -> str:
        return "UNKNOWN"

    def summarize(self, text: str, max_length: int = 200) -> str:
        return text[:max_length]


# Factory function
def get_ai_provider() -> AIProvider:
    """Get configured AI provider."""
    if settings.debug:
        # Use mock provider in debug mode for testing
        return MockProvider()
    else:
        return OllamaProvider(settings.model_name, settings.ollama_host)
