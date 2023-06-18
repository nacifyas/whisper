import logging
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def logging_setup():
    logger = logging.getLogger("uvicorn.access")
    console_formatter = uvicorn.logging.ColourizedFormatter(
        "{levelprefix} {asctime} {message}",
        style="{", use_colors=True)
    logger.handlers[0].setFormatter(console_formatter)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9900, reload=True) # remove reload on production
