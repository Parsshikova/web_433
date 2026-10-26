from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Demo Endpoints",
    description="API с двумя эндпоинтами: эхо имени и сумма двух чисел."
)

class NameRequest(BaseModel):
    name: str

class SumRequest(BaseModel):
    a: float
    b: float

@app.post("/echo-name", response_model=NameRequest)
def echo_name(request: NameRequest):
    """
    Принимает имя пользователя и возвращает его в JSON.
    Пример тела запроса: {"name": "Алексей"}
    """
    return {"name": request.name}

@app.post("/sum")
def calculate_sum(request: SumRequest):
    """
    Принимает два числа и возвращает их сумму.
    Пример тела запроса: {"a": 3.5, "b": 2.5}
    Ответ: {"a": 3.5, "b": 2.5, "sum": 6.0}
    """
    total = request.a + request.b
    return {
        "a": request.a,
        "b": request.b,
        "sum": total
    }

if __name__ == "__main__":
    import uvicorn
   
    uvicorn.run(app, host="0.0.0.0", port=8000)
