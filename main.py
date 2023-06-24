import io
import sys

import numpy as np
from fastapi import FastAPI, File
from pydantic.main import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, Response
from PIL import Image

sys.path.append("patch")
sys.path.append("comic-text-detector")

from inference import TextDetector

app = FastAPI(title="comic-text-detector-docker")
app.add_middleware(CORSMiddleware, allow_origins=["*"])
detector = TextDetector("./models/comictextdetector.pt.onnx")


class Block(BaseModel):
    xa: int
    ya: int
    xb: int
    yb: int


def send_image(image):
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    return Response(content=image_bytes.getvalue(), media_type="image/png")


@app.get("/", include_in_schema=False)
async def route_index():
    return RedirectResponse("/docs")


@app.post("/comic-text-detector-blocks", summary="Detect regions of text in an image.")
async def route_comic_text_detector_blocks(image: bytes = File()) -> list[Block]:
    image = Image.open(io.BytesIO(image))
    _mask, _mask_refined, blocks = detector(np.asarray(image))

    return [
        Block(
            xa=block.xyxy[0],
            ya=block.xyxy[1],
            xb=block.xyxy[2],
            yb=block.xyxy[3],
        )
        for block in blocks
    ]


@app.post("/comic-text-detector-mask", summary="Mask regions of text in an image.")
async def route_comic_text_detector_mask(image: bytes = File()):
    image = Image.open(io.BytesIO(image))
    _mask, mask_refined, _blocks = detector(np.asarray(image), keep_undetected_mask=True)
    return send_image(Image.fromarray(mask_refined))
