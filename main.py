from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://adiincode-ai.github.io",
        "https://adiincode-ai.github.io/",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
API_KEY=os.getenv("OPENWEATHER_API_KEY")



@app.get("/")
def home():
    return {"message":"Weather API running"}

@app.get("/weather/{city_name}")
def get_weather(city_name:str):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return{
            "error": data.get("message", "Something went wrong")
        }

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
    }

