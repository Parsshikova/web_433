from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx

app = FastAPI(title="Chat с локальной моделью через LM Studio")

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen2.5-0.5b-instruct"  


class ChatRequest(BaseModel):
    message: str = Field(..., description="Сообщение пользователя")
    system_prompt: str | None = Field(
        default="Ты полезный ассистент. Отвечай кратко и по делу.",
        description="Системный промпт",
    )
    max_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    reply: str
    model: str
    usage: dict


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": req.system_prompt},
            {"role": "user", "content": req.message},
        ],
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(LM_STUDIO_URL, json=payload)
            resp.raise_for_status()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="LM Studio недоступен. Убедитесь, что сервер запущен на localhost:1234",
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Ошибка LM Studio: {e.response.text}",
        )

    data = resp.json()
    return ChatResponse(
        reply=data["choices"][0]["message"]["content"],
        model=data.get("model", MODEL_NAME),
        usage=data.get("usage", {}),
    )


@app.get("/health")
async def health():
    """Проверка доступности LM Studio."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get("http://localhost:1234/v1/models")
            models = [m["id"] for m in resp.json()["data"]]
            return {"status": "ok", "models": models}
    except Exception:
        raise HTTPException(status_code=503, detail="LM Studio не отвечает")
