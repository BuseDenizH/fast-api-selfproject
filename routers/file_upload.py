from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
import pandas as pd
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.post("/uploadfile/")
async def upload_file(file:UploadFile = File(...)):
    file_content = await file.read()

    with open("temp_file.csv", "wb") as temp_file:
        temp_file.write(file_content)

    try:
        df = pd.read_csv("temp_file.csv")

        return JSONResponse(content=df.to_json(), media_type="application/json")
    except Exception as e:
        return JSONResponse(content={"error":str(e)}, status_code=400)
    finally:
        os.remove("temp_file.csv")

@router.get("/getfile/{filepath}")
async def get_file(file_path: str):
    file = f"uploads/{file_path}"
    if os.path.exists(file):
        return FileResponse(file)
    else:
        return {"error": "Dosya bulunamadı."}