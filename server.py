from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

CLIENT_ID = os.getenv("ML_CLIENT_ID")
CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET")
REDIRECT_URI = os.getenv("ML_REDIRECT_URI")

@app.get("/callback")
async def handle_callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return {"error": "No se recibió el código"}

    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.mercadolibre.com/oauth/token", data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI
        })

        return res.json()