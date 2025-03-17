from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stations")
async def get_stations():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=json&limit=55"
            )
            data = response.json()

            transformed_data = {
                "velos": [
                    {
                        "nom": station["nom"],
                        "adresse": station["adresse"],
                        "etat": station["etat"],
                        "nb_velos_dispo": station["nb_velos_dispo"],
                        "nb_places_dispo": station["nb_places_dispo"],
                        "x": station["x"],
                        "y": station["y"],
                        "date_modification": station["date_modification"]
                    }
                    for station in data["records"]
                ]
            }
            return transformed_data

    except Exception as e:
        return {"error": str(e)}