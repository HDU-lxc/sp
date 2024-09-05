import asyncio
import time
from fastapi import FastAPI, applications
from  router import api_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import fastapi_cdn_host
# api_router = APIRouter()

app = FastAPI()
app.include_router(api_router)
fastapi_cdn_host.patch_docs(app)
# # Press the green button in the gutter to run the script.
# loop = asyncio.get_event_loop()
# scheduler = AsyncIOScheduler(event_loop=loop)

if __name__ == '__main__':
    import uvicorn

    print(time.localtime())
    uvicorn.run("main:app", reload=True, lifespan="on", host='127.0.0.1', port=8088)