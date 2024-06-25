# -*- coding: utf-8 -*-
# Date       : 2023/11/5
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: LLM engine
import openai
from openai import OpenAI
from openai import AsyncClient
import time
import json
from functools import cache
from swarmagent.config.config import load_config

config = load_config()
api_key = config["OPENAI_API_KEY"]
base_url = config["BASE_URL"]

# gpt-4-0125-preview
# gpt-3.5-turbo
class OpenAILLM:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7, timeout=60):

        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.client = OpenAI(api_key=api_key,base_url=base_url)
        self.async_client = AsyncClient(api_key=api_key,base_url=api_key)

    def get_response(self, prompt: str, json_mode=False, system_prompt:str= "nothing" ,max_tokens=4000, retries=5):
        # print(f"current prompt :{prompt}")
        # print(f"current json mode: {json_mode}")
        """
        JSON_MODE开启之后直接返回JSON格式的结果，否则返回字符串
        """
        response_type = "text" if not json_mode else "json_object"
        messages = [{"role": "user", "content": prompt}] if system_prompt == "nothing" else [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        for i in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=self.temperature,
                    response_format={"type": response_type}
                )
                if json_mode:
                    result = response.choices[0].message.content
                    result = json.loads(response.choices[0].message.content)
                else:
                    result = response.choices[0].message.content
                return result
            except openai.RateLimitError:
                print("Occur RateLimitError, sleep 20s")
                time.sleep(20)
                print("Rate limit retry")

    @cache
    def get_embeddings(self, query):
        response = self.client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        embeddings = response.data[0].embedding
        return embeddings


if __name__ == "__main__":
    llm = OpenAILLM()
    llm.get_response("hello world")