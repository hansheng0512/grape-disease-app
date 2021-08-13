from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import logging
from PIL import Image
import io

from api_server.utils import base64_str_to_PILImage
from api_server.classifier import SqueezeNet
from api_server.models import Base64str, ResponseDataModel


app = FastAPI()
image_classifer = SqueezeNet()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return "Hello!"


@app.post("/predict")
def predict(payload: Base64str):
    try:
        image = base64_str_to_PILImage(payload.base64str)
        predicted_class = image_classifer.predict(image)
        logging.info(f"Predicted Class: {predicted_class}")

        return {"likely_class": predicted_class}

    except Exception as error:
        logging.exception(error)
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict-img", response_model=ResponseDataModel)
async def predict(file: UploadFile = File(...)):
    if file.content_type.startswith("image/") is False:
        raise HTTPException(
            status_code=400, detail=f"File '{file.filename}' is not an image."
        )

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        predicted_class = image_classifer.predict(image)

        logging.info(f"Predicted Class: {predicted_class}")
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "likely_class": predicted_class,
        }

    except Exception as error:
        logging.exception(error)
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "api_server.main:app", reload=True, host="0.0.0.0", port=8000, log_level="info"
    )
