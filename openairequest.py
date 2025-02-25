import json
import time
import uvicorn

from typing import List

import yaml
from fastapi import FastAPI, Depends, HTTPException
from starlette import status

from grok import GrokRequest
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import StreamingResponse


class Message(BaseModel):
    role: str
    content: str


class OpenAIRequest(BaseModel):
    model: str
    stream: bool
    max_tokens: int
    messages: List[Message]


class Model(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str


class ModelList(BaseModel):
    object: str = "list"
    data: List[Model]


models_data = ModelList(
    data=[
        Model(id="grok-latest", created=int(time.time()), owned_by="xai"),
        Model(id="grok-3", created=int(time.time()), owned_by="xai")
    ]
)

app = FastAPI()
grok_request = GrokRequest()
security = HTTPBearer()

with open('cookies.yaml', 'r') as file:
    config = yaml.safe_load(file)
valid_api_keys = config['password']


async def verify_api_key(authorization: HTTPAuthorizationCredentials = Depends(security)):
    if not valid_api_keys:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API keys not configured"
        )

    if authorization.credentials not in valid_api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Invalid API key",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": "invalid_api_key"
                }
            }
        )


async def generate_response(message: str, model: str):
    tokens = []
    async for token in grok_request.get_grok_request(str(message), model):
        tokens.append(token)
    return tokens


async def generate_stream_response(message: str, model: str):
    async for token in grok_request.get_grok_request(str(message), model):
        data = {
            "id": "grok-proxy",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "delta": {"content": token},
                    "index": 0,
                    "finish_reason": None
                }
            ]
        }
        yield f"data: {json.dumps(data)} \n\n "

    end_data = {
        "id": f"grok-proxy-end",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "delta": {},
                "index": 0,
                "finish_reason": "stop"
            }
        ]
    }
    yield f"data: {json.dumps(end_data)} \n\n "
    yield "data: [DONE] \n\n "  # OpenAI 官方接口的结束标志


@app.get("/v1/models", response_model=ModelList, dependencies=[Depends(verify_api_key)])
async def get_models():
    return models_data


@app.post("/v1/chat/completions", dependencies=[Depends(verify_api_key)])
async def handle_openai_request(request: OpenAIRequest):
    # print(str(request.messages))
    if request.stream:
        # 流式响应
        return StreamingResponse(
            generate_stream_response(str(request.messages), request.model),
            media_type="text/event-stream"
        )
    else:
        # 非流式响应
        tokens = ''.join(await generate_response(str(request.messages), request.model))
        return {
            "id": "grok_proxy",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": tokens
                    },
                    "finish_reason": "stop",
                    "index": 0
                }
            ]
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
