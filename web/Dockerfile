FROM python:3.14-slim

WORKDIR /app

COPY web/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY web/ ./web/
COPY utils/ ./utils/
COPY worker/ ./worker/
COPY database/ ./database/

CMD ["uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8000"]
