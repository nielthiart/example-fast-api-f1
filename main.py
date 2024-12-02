from typing import List

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local server",
        }
    ],
    openapi_tags=[
        {
            "name": "F1",
            "description": "Endpoints related to F1 races and winners.",
            "externalDocs": {
                "description": "F1 official website",
                "url": "http://localhost:8000/docs",
            },
        },
    ],
)

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
    """The winner of a race."""

    race: str = Field(description="The name of the F1 race.", examples=["bahrain"])
    winner: str = Field(
        description="The name of the F1 race.", examples=["Lewis Hamilton"]
    )

    model_config = ConfigDict(
        title="Race winner",
        json_schema_extra={
            "examples": [
                {
                    "race": "bahrain",
                    "winner": "Lewis Hamilton",
                },
            ],
        },
    )


class YearWinnersResponse(BaseModel):
    """Year winners response."""

    year: int = Field(description="The year of the F1 race.", examples=[2021])
    winners: List[RaceWinner] = Field(
        description="The winners",
        examples=[
            {
                "race": "bahrain",
                "winner": "Lewis Hamilton",
            },
        ],
    )

    model_config = ConfigDict(
        title="Year winners",
        json_schema_extra={
            "examples": [
                {
                    "year": 2021,
                    "winners": [
                        {
                            "race": "bahrain",
                            "winner": "Lewis Hamilton",
                        },
                        {
                            "race": "emilia_romagna",
                            "winner": "Max Verstappen",
                        },
                    ],
                },
            ],
        },
    )


class RaceWinnerResponse(BaseModel):
    """Race winner response."""

    year: int
    race: str
    winner: str

    model_config = ConfigDict(
        title="Race winner response",
        json_schema_extra={
            "examples": [
                {
                    "year": 2021,
                    "race": "bahrain",
                    "winner": "Lewis Hamilton",
                },
                {
                    "year": 2024,
                    "race": "cape_town",
                    "winner": "Abdul Davids",
                },
            ],
        },
    )


class ResponseMessage(BaseModel):
    """A response message"""

    message: str = Field(description="The response message")


OPENAPI_RESPONSE_OBJECT_NOT_FOUND = {
    "model": ResponseMessage,
    "description": "Object not found",
}


@app.get(
    "/",
    response_model=ResponseMessage,
    operation_id="root",
)
def read_root():
    """
    Welcome message.
    """
    return {"message": "Welcome to the F1 Race Winners API! Docs at /docs."}


@app.get(
    "/winners/{year}",
    response_model=YearWinnersResponse,
    tags=["F1"],
    operation_id="getYearWinners",
    responses={
        404: OPENAPI_RESPONSE_OBJECT_NOT_FOUND,
    },
    summary="Get the winners of all Formula 1 races in a given year.",
)
def get_year_winners(year: int):
    """
    Get the winners of all Formula 1 races in a given year.
    """
    if year in f1_race_winners:
        return {"year": year, "winners": f1_race_winners[year]}
    return JSONResponse(
        status_code=404,
        content={
            "message": "Data not available for the requested year.",
        },
    )


@app.get(
    "/winners/{year}/{race}",
    response_model=RaceWinnerResponse,
    tags=["F1"],
    operation_id="getRaceWinner",
    responses={
        404: OPENAPI_RESPONSE_OBJECT_NOT_FOUND,
    },
    summary="Get the winner of a specific Formula 1",
)
def get_race_winner(year: int, race: str):
    """
    Get the winner of a specific Formula 1 race in a given year.
    """
    if year in f1_race_winners:
        for race_info in f1_race_winners[year]:
            if race_info["race"].strip().lower() == race.strip().lower():
                return {
                    "year": year,
                    "race": race,
                    "winner": race_info["winner"],
                }
        return JSONResponse(
            status_code=404,
            content={
                "message": "Data not available for the requested race.",
            },
        )
    return JSONResponse(
        status_code=404,
        content={
            "message": "Data not available for the requested year.",
        },
    )
