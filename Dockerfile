FROM python:3.10-slim-buster

ADD ./models ./models
ADD ./download_model.py ./
RUN python3 download_model.py

RUN pip install --no-cache-dir pdm
ADD ./pyproject.toml ./pdm.lock ./
RUN pdm sync && pdm cache clear

ADD ./comic-text-detector ./comic-text-detector
ADD ./patch ./patch
ADD ./main.py ./

CMD ["pdm", "run", "uvicorn", \
	"--host", "0.0.0.0", "--port", "$PORT", \
	"main:app"]