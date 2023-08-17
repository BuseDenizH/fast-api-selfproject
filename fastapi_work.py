import asyncio
import json
import time
from typing import Optional, List, Dict
from urllib.request import Request

from typing import Union

from fastapi import FastAPI, Header, Body
from pydantic import BaseModel
import uvicorn

from routers import arithmetic, file_upload


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])


app.include_router(arithmetic.router)
app.include_router(file_upload.router)


class Person(BaseModel):
    name:str
    age:int

class Cars(BaseModel):
    brand:str
    model:str
    year:int
    price:float
    tax:Union[float, None] = None

@app.post("/about_cars/")
async def about_cars(cars: Cars):
    cars_dict = cars.dict()
    if cars.tax:
        price_with_tax = cars.price + cars.tax
        cars_dict.update({"price_with_tax": price_with_tax})
    return cars_dict

@app.put("/cars/{car_id}")
async def create_car(car_id: int, cars:Cars, q: Union[str, None] = None):
    result = {"car_id": car_id, **cars.dict()}
    if q:
        result.update({"q":q})
    return result


@app.get("/name/{name}")
async def read_items(name:str):
    return {"name":name}

@app.get("/get_with_body")
async def get_with_body(name:str=Body(...,embed=True),age:int=Body(...,embed=True)):
    return {"name":name,"age":age}


@app.post("/post_with_body")
async def post_with_body(name:str=Body(...,embed=True)):
    return {"name":name}


@app.post("/create_person")
async def create_person(person:Person):
    return {"Person":person}

async def simulate_network_request():
    print("Ağ isteği başlıyor...")
    await asyncio.sleep(5)
    print("Ağ isteği tamamlandı!")

@app.get("/async_example")
async def async_example():
    asyncio.create_task(simulate_network_request())
    print("Asenkron işlem devam ediyor...")
    return {"message":"Asenkron işlem sırasında diğer işlemler yapılıyor."}