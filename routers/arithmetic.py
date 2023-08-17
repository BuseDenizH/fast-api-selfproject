from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/arithmetic",
    tags=["arithmetic"]
)

class TwoInt(BaseModel):
    num1:int
    num2:int

@router.post("/add")
def add(twoint:TwoInt):
    result=twoint.num1+twoint.num2
    return {"result":result}

@router.post("/mul")
def mul(number1:int,number2:int):
    result=number1*number2
    return {"result":result}

@router.get("/sub")
def sub(number1:int,number2:int):
    result=number1-number2
    return {"result":result}

@router.get("/div")
def div(twoint:TwoInt):
    result=twoint.num1/twoint.num2
    return {"result":result}