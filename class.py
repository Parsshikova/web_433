from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    age: int
items_list= [
    {
        "id": 1,
        "name": "John",
        "age":18,
    },
    {
        "id":2,
        "name":"Vika",
        "age":20,
    },
    {
       "id":3,
       "name":"Denis",
       "age":22,  
    }
]

@app.get("/")
async def root():
    return {
        "message": "Hello world!"
    }

@app.get("/items")
async def items() -> list[dict]:
    return items_list


@app.get("/items/{item_id}")
async def detail_item(item_id:int) -> dict:
    for item in items_list:
        if item["id"]==item_id:
            return item


    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Страница не найдена"
    )




@app.post("/items")
async def create_item(item:Item) -> dict:
    idx = len(items_list) + 1 
    item = {
        "id":idx,
        "name":item.name,
        "age":item.age,
    }
    items_list.append(item)
    return item



if __name__== "__main__":
    import uvicorn

    uvicorn.run("main:app", host ="0.0.0.0", port=8000, reload=True)    
