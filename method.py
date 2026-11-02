from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


class Person(BaseModel):
    name: str
    age: int

item_list: List[Person] = [
    Person(name="Bob", age=18),
    Person(name="Alice", age=25),
    Person(name="Charlie", age=30),
]

def get_person_by_id(person_id: int) -> Person:
    if 0 <= person_id < len(item_list):
        return item_list[person_id]
    raise HTTPException(status_code=404, detail="Person not found")

@app.get("/people", response_model=List[Person])
def get_people():
    return item_list

@app.get("/people/{person_id}", response_model=Person)
def get_person(person_id: int):
    return get_person_by_id(person_id)

@app.put("/people/{person_id}", response_model=Person)
def update_person_full(person_id: int, person: Person):
    # Проверяем, что ID существует
    get_person_by_id(person_id)  # вызовет 404, если нет
    # Полностью заменяем объект
    item_list[person_id] = person
    return item_list[person_id]

@app.patch("/people/{person_id}", response_model=Person)
def update_person_partial(person_id: int, updates: dict):
    person = get_person_by_id(person_id)
    
  
    for key, value in updates.items():
        if hasattr(person, key):
            setattr(person, key, value)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid field: {key}"
            )
    return person

@app.delete("/people/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: int):
    get_person_by_id(person_id)  # проверка существования
    del item_list[person_id]
   
    return None
