# -*- coding: utf-8 -*-
# Date       : 2023/11/5
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: LLM engine
import openai
import asyncio
from openai import OpenAI
from openai import AsyncClient
import time
import json
import os


# TODO OPENAI 修改Client 需要做出同步修改

class OpenAILLM:
    def __init__(self, model="gpt-3.5-turbo-1106", temperature=0.7, timeout=60):

        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),
                             base_url=os.environ.get("BASE_URL"))
        self.async_client = AsyncClient(api_key=os.environ.get("OPENAI_API_KEY"),
                                        base_url=os.environ.get("BASE_URL"))

    def get_response(self, prompt: str, json_mode=False, max_tokens=1500, retries=5):
        print(f"current prompt :{prompt}")
        print(f"current json mode: {json_mode}")
        """
        JSON_MODE开启之后直接返回JSON格式的结果，否则返回字符串
        """
        response_type = "text" if not json_mode else "json_object"
        for i in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=self.temperature,
                    response_format={"type": response_type}
                )
                if json_mode:
                    result = response.choices[0].message.content
                    print(f"Json mode result: {result}")
                    result = json.loads(response.choices[0].message.content)
                else:
                    result = response.choices[0].message.content
                return result
            except openai.RateLimitError:
                print("Occur RateLimitError, sleep 20s")
                time.sleep(20)
                print("Rate limit retry")
            except Exception as e:
                print(f"{__name__} occurs: {e}")

    async def async_get_response(self, prompt: str, json_mode=False, max_tokens=1500, retries=5):
        print(f"current prompt :{prompt}")
        print(f"current json mode: {json_mode}")
        """
        JSON_MODE开启之后直接返回JSON格式的结果，否则返回字符串
        """
        async_response_type = "text" if not json_mode else "json_object"
        for i in range(retries):
            try:
                async_response = await self.async_client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=self.temperature,
                    response_format={"type": async_response_type}
                )
                if json_mode:
                    async_result = async_response.choices[0].message.content
                    print(f"Json mode result: {async_result}")
                    async_result = json.loads(async_response.choices[0].message.content)
                else:
                    async_result = async_response.choices[0].message.content
                return async_result
            except openai.RateLimitError:
                print("Occur RateLimitError, sleep 20s")
                await asyncio.sleep(20)
                print("Rate limit retry")
            except Exception as e:
                print(f"{__name__} occurs: {e}")

def prompt_load(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        content = "File not found at the specified path."

    return content
