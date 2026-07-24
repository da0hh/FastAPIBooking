FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#  Открываем порт для FastAPI
EXPOSE 8100

#  Запускаем сервер uvicorn (файл router.py, объект app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"]
#python -m streamlit run router.py
#docker run -p 8501:8501 -d fastapi-docker