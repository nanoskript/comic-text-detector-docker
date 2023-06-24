import urllib.request

urllib.request.urlretrieve(
    "https://github.com/zyddnys/manga-image-translator/releases/download/beta-0.2.1/comictextdetector.pt.onnx",
    "./models/comictextdetector.pt.onnx"
)
