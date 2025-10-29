from typing import *
import json
from openai import OpenAI
from openai.types.chat.chat_completion import Choice

import config

# 初始化 Moonshot AI 客户端，设置 API 的基础 URL 和 API 密钥
base_url = "https://api.moonshot.cn/v1"
api_key = config.get_config("Kimi_API_KEY")

kimi_client = OpenAI(
    base_url=base_url,
    api_key=api_key
)


class KimiClient:
    def __init__(self):
        self.client = kimi_client

    def chat(self, prompt, response_format="text",
             temperature=0.7, role_system="You are a helpful assistant"):
        try:
            completion = self.client.chat.completions.create(
                model="kimi-k2-0905-preview",
                messages=[
                    {"role": "system", "content": role_system},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                response_format={"type": response_format},
                max_tokens = 128000
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"调用Kimi API时出错: {e}")
            return None