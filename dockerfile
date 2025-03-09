FROM python:3.11-slim
WORKDIR /app
COPY src/requirements.txt .
COPY src/train.py .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "train.py"]