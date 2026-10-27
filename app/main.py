import uvicorn
from fastapi import FastAPI

from core.config import settings

from api.router import router 


app = FastAPI()
app.include_router(
    router,
    prefix=settings.api.prefix
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port, 
        reload=True)