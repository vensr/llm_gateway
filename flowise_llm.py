from typing import Iterator, AsyncIterator
from litellm.types.utils import GenericStreamingChunk, ModelResponse
from litellm import CustomLLM, completion, acompletion
import requests

class FlowiseLLM(CustomLLM):

    def __init__(self, url):
        super().__init__()
        self.api_url = url

    def query(self, payload):
        response = requests.post(self.api_url, json=payload)
        return response.json()

    def completion(self, *args, **kwargs) -> ModelResponse:
        question = kwargs["messages"][0]["content"]
        response_json = self.query({"question": question})
        return completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello world"}],
            mock_response=response_json["text"],
        )  # type: ignore

    async def acompletion(self, *args, **kwargs) -> ModelResponse:
        question = kwargs["messages"][0]["content"]
        response_json = self.query({"question": question})
        return acompletion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello world"}],
            mock_response=response_json["text"],
        )  # type: ignore

    def streaming(self, *args, **kwargs) -> Iterator[GenericStreamingChunk]:
        index = len(kwargs["messages"]) - 1
        question = kwargs["messages"][index]["content"]
        print(question)
        response_json = self.query({"question": question})
        generic_streaming_chunk: GenericStreamingChunk = {
            "finish_reason": "stop",
            "index": 0,
            "is_finished": True,
            "text": response_json["text"],
            "tool_use": None,
            "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0},
        }
        return generic_streaming_chunk # type: ignore

    async def astreaming(self, *args, **kwargs) -> AsyncIterator[GenericStreamingChunk]:
        index = len(kwargs["messages"]) - 1
        question = kwargs["messages"][index]["content"]
        print(question)
        response_json = self.query({"question": question})
        generic_streaming_chunk: GenericStreamingChunk = {
            "finish_reason": "stop",
            "index": 0,
            "is_finished": True,
            "text": response_json["text"],
            "tool_use": None,
            "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0},
        }
        yield generic_streaming_chunk # type: ignore

