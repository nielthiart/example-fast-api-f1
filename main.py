from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(servers=[{"url": "http://localhost:8000"}])

# Fake data of F1 race winners
f1_race_winners = {
    2021: [
        {"race": "bahrain", "winner": "Lewis Hamilton"},
        {"race": "emilia_romagna", "winner": "Max Verstappen"},
        {"race": "portuguese", "winner": "Lewis Hamilton"},
    ],
    2022: [
        {"race": "bahrain", "winner": "Charles Leclerc"},
        {"race": "saudi_arabia", "winner": "Max Verstappen"},
        {"race": "australian", "winner": "Charles Leclerc"},
    ],
    2023: [
        {"race": "bahrain", "winner": "Max Verstappen"},
        {"race": "saudi_arabia", "winner": "Max Verstappen"},
        {"race": "australian", "winner": "Max Verstappen"},
    ],
    2024: [
        {"race": "bahrain", "winner": "Max Verstappen"},
        {"race": "australian", "winner": "Carlos Sainz"},
        {"race": "saudi_arabia", "winner": "Max Verstappen"},
        {"race": "monaco", "winner": "Charles Leclerc"},
        {"race": "cape_town", "winner": "Abdul Davids"},
    ],
}


# Models
class RaceWinner(BaseModel):
    race: str
    winner: str

    class Config:
        schema_extra = {
            "example": {"race": "bahrain", "winner": "Lewis Hamilton"},
        }

class YearWinnersResponse(BaseModel):
    year: int
    winners: List[RaceWinner]

    class Config:
        schema_extra = {
            "example": {
                "year": 2021,
                "winners": [
                    {"race": "bahrain", "winner": "Lewis Hamilton"},
                    {"race": "emilia_romagna", "winner": "Max Verstappen"},
                ]
            }
        }

class RaceWinnerResponse(BaseModel):
    year: int
    race: str
    winner: str

    class Config:
        schema_extra = {
            "example": {"race": "bahrain", "winner": "Lewis Hamilton"}
        }

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the F1 Race Winners API!"}

# Endpoint to get winners for a specific year
@app.get("/winners/{year}", response_model=YearWinnersResponse)
def get_year_winners(year: int):
    if year in f1_race_winners:
        return {"year": year, "winners": f1_race_winners[year]}
    return {"error": "Data not available for the requested year."}

# Endpoint to get winners for a specific year and race
@app.get("/winners/{year}/{race}", response_model=RaceWinnerResponse)
def get_race_winner(year: int, race : str):
    if year in f1_race_winners:
        for race_info in f1_race_winners[year]:
            if race_info["race"].strip().lower() == race.strip().lower():
                return {"year": year, "race": race, "winner": race_info["winner"]}
        return {"error": "Race not found for the requested year."}
    return {"error": "Data not available for the requested year."}