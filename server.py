from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
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
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"error": "No se recibió el código"}
        )

    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.mercadolibre.com/oauth/token", data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI
        })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=res.json()
        )
