"""
Intent Extractor - Uses LLM to extract structured infrastructure intent
Supports any tech stack, database, and architecture pattern
"""

import os
import json
from typing import Dict, Any
from openai import OpenAI


class IntentExtractor:
    """Extracts structured infrastructure intent from natural language"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.mock_mode = True
            self.client = None
        else:
            self.mock_mode = False
            # Keep client lazy/simple for PoC
            self.client = OpenAI(api_key=api_key)

    def extract_intent(self, description: str) -> Dict[str, Any]:
        """Extract structured intent. Uses mock if no API key available."""
        if self.mock_mode:
            intent = self._mock_extract(description)
        else:
            # Attempt a lightweight LLM call, fallback to mock on any error
            try:
                resp = self.client.responses.create(
                    model="gpt-4o-mini",
                    input=f"Extract a JSON intent describing infrastructure from: {description}",
                    max_output_tokens=512
                )
                text = getattr(resp, "output_text", None) or str(resp)
                intent = json.loads(text)
            except Exception:
                intent = self._mock_extract(description)

        return self._validate_and_defaults(intent)

    def _mock_extract(self, description: str) -> Dict[str, Any]:
        """Mock extraction heuristics (no external API required)."""
        d = (description or "").lower()
        app = "other"
        if "node" in d or "nodejs" in d:
            app = "nodejs"
        elif "go" in d or "golang" in d:
            app = "golang"
        elif "python" in d:
            app = "python"
        elif "java" in d:
            app = "java"

        database = "none"
        if "mongo" in d or "mongodb" in d:
            database = "mongodb"
        elif "mysql" in d:
            database = "mysql"
        elif "postgres" in d or "postgresql" in d:
            database = "postgresql"

        load_balancer = any(x in d for x in ["load balancer", "alb", "loadbalancer", "high availability", "ha"])
        availability = "high" if "high" in d or "redund" in d or "availability" in d else "standard"
        app_count = 2 if load_balancer or availability == "high" else 1

        intent = {
            "cloud": "aws",
            "app": app,
            "database": database,
            "architecture": "3-tier" if load_balancer and database != "none" else ("2-tier" if database != "none" else "serverless"),
            "availability": availability,
            "load_balancer": load_balancer,
            "security": ["private_vpc", "security_groups"],
            "region": "us-east-1",
            "instance_type": "t2.micro",
            "app_count": app_count,
            "database_type": "rds" if "rds" in d or "managed" in d else "ec2"
        }
        return intent

    def _validate_and_defaults(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure all fields exist and have sane defaults."""
        defaults = {
            "cloud": "aws",
            "app": "other",
            "database": "none",
            "architecture": "2-tier",
            "availability": "standard",
            "load_balancer": False,
            "security": ["private_vpc", "security_groups"],
            "region": "us-east-1",
            "instance_type": "t2.micro",
            "app_count": 1,
            "database_type": "ec2"
        }
        out = {}
        for k, v in defaults.items():
            out[k] = intent.get(k, v)
        # Type safety
        out["load_balancer"] = bool(out["load_balancer"])
        out["app_count"] = int(out.get("app_count", 1) or 1)
        return out
