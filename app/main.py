from typing import Optional
# from . import schemas, models
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import RedirectResponse, Response, JSONResponse
# from .database import SessionLocal, engine
from sqlalchemy.orm import Session
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from .utils import *
from datetime import datetime
import pytz
import requests
from .config import settings
import motor.motor_asyncio
from pydantic import BaseModel, Field
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.register

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class RegistrationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    location: str = Field(...)
    date: str = Field(...)
    time: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "location": "TQ",
                "date": datetime.now,
                "time": "AM",
            }
        }






@app.get("/")
async def index():
    return {"Hello": "World"}


@app.post("/", response_description="Add new student", response_model=RegistrationModel)
async def register(registration: RegistrationModel = Body(...)):
    existing_registration = await db["registration"].find_one(
        {
            "name": registration.name,
            "location": registration.location,
            "date": registration.date,
            "time": registration.time
        }
    )
    registration = jsonable_encoder(registration)
    if (existing_registration):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content="Already exists")
    else:
        new_registration = await db["registration"].insert_one(registration)
        created_registration = await db["registration"].find_one({"_id": new_registration.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_registration)




@app.on_event("startup")
# @repeat_every(seconds=10) 
def update_schedule() -> None:
    print("-------------------")
    print(f"Updating Telegram schedule text: {settings.SCHEDULE_TEXT_TIMESTAMP}")
    send_telegram_text_update()