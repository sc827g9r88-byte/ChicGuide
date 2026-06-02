# -*- coding: utf-8 -*-
"""
Unified AI API Client
Supports OpenAI, Qwen (Tongyi), Kimi (Moonshot), and other LLM providers
"""

import json
import requests
from typing import Optional, Dict, List, Generator
from dataclasses import dataclass, asdict


@dataclass
class AIConfig:
    """AI API Configuration"""
    provider: str = "openai"  # openai, qwen, kimi, custom
    api_key: str = ""
    api_base: str = ""
    model: str = ""
    temperature: float = 0.8
    max_tokens: int = 2048

    def to_dict(self):
        return asdict(self)


class AIClient:
    """Unified AI Client for multiple providers"""

    # Provider configurations
    PROVIDER_DEFAULTS = {
        "openai": {
            "api_base": "https://api.openai.com/v1",
            "models": [
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4-turbo",
                "gpt-3.5-turbo",
            ],
            "default_model": "gpt-4o-mini",
        },
        "qwen": {
            "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "models": [
                "qwen-turbo",
                "qwen-plus",
                "qwen-max",
                "qwen2.5-72b-instruct",
                "qwen2.5-14b-instruct",
                "qwen2.5-7b-instruct",
            ],
            "default_model": "qwen-turbo",
        },
        "kimi": {
            "api_base": "https://api.moonshot.cn/v1",
            "models": [
                "moonshot-v1-128k",
                "moonshot-v1-32k",
                "moonshot-v1-8k",
                "moonshot-v1-auto",
            ],
            "default_model": "moonshot-v1-8k",
        },
        "deepseek": {
            "api_base": "https://api.deepseek.com/v1",
            "models": [
                "deepseek-chat",
                "deepseek-reasoner",
            ],
            "default_model": "deepseek-chat",
        },
        "custom": {
            "api_base": "",
            "models": [],
            "default_model": "",
        },
    }

    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        self._validate_config()

    def _validate_config(self):
        """Validate and set defaults"""
        if not self.config.api_base:
            defaults = self.PROVIDER_DEFAULTS.get(self.config.provider, {})
            self.config.api_base = defaults.get("api_base", "")
        if not self.config.model:
            defaults = self.PROVIDER_DEFAULTS.get(self.config.provider, {})
            self.config.model = defaults.get("default_model", "")

    @classmethod
    def get_provider_list(cls) -> List[str]:
        """Get list of supported providers"""
        return list(cls.PROVIDER_DEFAULTS.keys())

    @classmethod
    def get_models_for_provider(cls, provider: str) -> List[str]:
        """Get available models for a provider"""
        return cls.PROVIDER_DEFAULTS.get(provider, {}).get("models", [])

    @classmethod
    def get_default_model(cls, provider: str) -> str:
        """Get default model for a provider"""
        return cls.PROVIDER_DEFAULTS.get(provider, {}).get("default_model", "")

    def chat(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        """
        Send chat completion request

        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response

        Returns:
            Response text
        """
        if not self.config.api_key:
            raise ValueError("API Key not configured. Please set up API settings first.")

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        # Add provider-specific headers
        if self.config.provider == "qwen":
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "stream": stream,
        }

        try:
            response = requests.post(
                f"{self.config.api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return f"Error: Unexpected response format - {json.dumps(data, ensure_ascii=False)}"

        except requests.exceptions.Timeout:
            return "Error: Request timeout. Please check your network connection."
        except requests.exceptions.ConnectionError:
            return "Error: Connection failed. Please check the API base URL."
        except requests.exceptions.HTTPError as e:
            error_msg = f"Error: HTTP {e.response.status_code}"
            try:
                error_detail = e.response.json()
                if "error" in error_detail:
                    error_msg += f" - {error_detail['error'].get('message', '')}"
            except:
                error_msg += f" - {e.response.text[:200]}"
            return error_msg
        except Exception as e:
            return f"Error: {str(e)}"

    def chat_stream(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """
        Stream chat completion

        Yields:
            Chunks of response text
        """
        if not self.config.api_key:
            yield "Error: API Key not configured."
            return

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "stream": True,
        }

        try:
            response = requests.post(
                f"{self.config.api_base}/chat/completions",
                headers=headers,
                json=payload,
                stream=True,
                timeout=60,
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            yield f"Error: {str(e)}"

    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            messages = [{"role": "user", "content": "Hello"}]
            result = self.chat(messages)
            return not result.startswith("Error:")
        except:
            return False

    def get_outfit_advice(self, scene: str, season: str = "", style_preference: str = "") -> str:
        """Get outfit advice for a specific scene"""
        system_prompt = """你是一位专业的时尚穿搭顾问，擅长为女性用户提供场合穿搭建议。
请根据用户描述的场景，提供1-2套完整的搭配方案。

每套方案需要包含：
1. 整体搭配概述
2. 上装、下装、鞋履、配饰的具体推荐
3. 从以下四个维度分析为什么这样搭配：
   - 色彩：选择的色系如何适合该场合
   - 款式：单品款式如何符合场合需求
   - 风格：整体风格如何匹配场景氛围
   - 场合逻辑：为什么这样的穿搭在该场合得体且实用

请用中文回答，语言亲切友好，像闺蜜在分享穿搭建议一样。
格式清晰，使用emoji让内容更生动。"""

        user_prompt = f"场景：{scene}"
        if season:
            user_prompt += f"\n当前季节：{season}"
        if style_preference:
            user_prompt += f"\n风格偏好：{style_preference}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        return self.chat(messages)

    def get_brand_feedback(self, question: str, context: Dict) -> str:
        """Get AI feedback for brand recommendation questions"""
        system_prompt = """你是一位专业的时尚购物顾问。用户对你的品牌推荐有疑问或需要调整，请根据用户的需求友好地调整推荐。
请保持专业、亲切的态度，像闺蜜在聊天一样给出建议。"""

        context_str = f"\n用户背景：\n职业：{context.get('occupation', '')}\n收入：{context.get('income', '')}\n风格：{', '.join(context.get('styles', []))}\n"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{context_str}\n用户问题：{question}"},
        ]

        return self.chat(messages)
