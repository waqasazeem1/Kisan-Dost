# from pathlib import Path

# from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel, Field

# from main import ask_kisan

# FRONTEND_DIR = Path(__file__).parent / "frontend"

# app = FastAPI(title="Kisan Dost")
# app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# class ChatRequest(BaseModel):
#     message: str = Field(..., min_length=1)


# class ChatResponse(BaseModel):
#     reply: str


# @app.get("/")
# async def home():
#     return FileResponse(
#         FRONTEND_DIR / "index.html",
#         headers={"Cache-Control": "no-store"},
#     )


# @app.post("/api/chat", response_model=ChatResponse)
# async def chat(req: ChatRequest):
#     text = req.message.strip()
#     if not text:
#         raise HTTPException(status_code=400, detail="Sawal khali nahi ho sakta")
#     try:
#         reply = await ask_kisan(text)
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=str(exc)) from exc
#     return ChatResponse(reply=reply)



from pathlib import Path
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from main import ask_kisan

FRONTEND_DIR = Path(__file__).parent / "frontend"

app = FastAPI(title="Kisan Dost")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
async def home():
    return FileResponse(
        FRONTEND_DIR / "index.html",
        headers={"Cache-Control": "no-store"},
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    text = req.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Sawal khali nahi ho sakta")
    try:
        reply = await ask_kisan(text)
    except Exception as exc:
        traceback.print_exc()  # terminal mein poora error dikhega
        error_message = str(exc) or f"{type(exc).__name__} (koi message nahi mila)"
        raise HTTPException(status_code=500, detail=error_message) from exc
    return ChatResponse(reply=reply)

