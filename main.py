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


class Line(BaseModel):
    xa: int
    ya: int
    xb: int
    yb: int


class Block(BaseModel):
    xa: int
    ya: int
    xb: int
    yb: int
    lines: list[Line]


def send_image(image):
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    return Response(content=image_bytes.getvalue(), media_type="image/png")


@app.get("/", include_in_schema=False)
async def route_index():
    return RedirectResponse("/docs")


@app.post("/comic-text-detector-blocks", summary="Detect regions of text in an image.")
async def route_comic_text_detector_blocks(image: bytes = File()) -> list[Block]:
    image = Image.open(io.BytesIO(image)).convert("RGBA")
    _mask, _mask_refined, blocks = detector(np.asarray(image))

    return [
        Block(
            xa=block.xyxy[0],
            ya=block.xyxy[1],
            xb=block.xyxy[2],
            yb=block.xyxy[3],
            lines=[
                Line(
                    xa=min([line[0][0], line[1][0], line[2][0], line[3][0]]),
                    ya=min([line[0][1], line[1][1], line[2][1], line[3][1]]),
                    xb=max([line[0][0], line[1][0], line[2][0], line[3][0]]),
                    yb=max([line[0][1], line[1][1], line[2][1], line[3][1]]),
                )
                for line in block.lines
            ],
        )
        for block in blocks
    ]


@app.post("/comic-text-detector-mask", summary="Mask regions of text in an image.")
async def route_comic_text_detector_mask(image: bytes = File(), keep_undetected_mask: bool = True):
    image = Image.open(io.BytesIO(image)).convert("RGBA")
    _mask, mask_refined, _blocks = detector(np.asarray(image), keep_undetected_mask=keep_undetected_mask)
    return send_image(Image.fromarray(mask_refined))
