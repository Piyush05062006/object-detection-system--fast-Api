from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from pydantic import BaseModel
from model.detector import detect_from_image
from database.db import detections_collection, users_collection
from database.models import detection_schema
from auth.auth import (
    hash_password, verify_password,
    create_access_token, verify_token
)
import shutil
import os

app = FastAPI()

class UserLogin(BaseModel):
    username: str
    password: str

@app.get("/")
def home():
    return {"message": "Object Detection API is running"}

@app.post("/register")
def register(user: UserLogin):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    users_collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password)
    })
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"token": token}

@app.post("/detect")
async def detect(
    file: UploadFile = File(...),
    authorization: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    raw_token = authorization.split(" ")[1]
    current_user = verify_token(raw_token)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    os.makedirs("uploads", exist_ok=True)
    image_path = f"uploads/{file.filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = detect_from_image(image_path)

    record = detection_schema(file.filename, results)
    record["username"] = current_user
    detections_collection.insert_one(record)

    os.remove(image_path)

    return {
        "filename": file.filename,
        "total_objects": len(results),
        "detections": results
    }

@app.get("/history")
async def get_history(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    raw_token = authorization.split(" ")[1]
    current_user = verify_token(raw_token)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    records = list(detections_collection.find(
        {"username": current_user},
        {"_id": 0}
    ))
    return {"history": records}