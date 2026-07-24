FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

#  Открываем порт для FastAPI
EXPOSE 8501

#  Запускаем сервер uvicorn (файл router.py, объект app)
CMD ["streamlit", "run", "main.py"]
#python -m streamlit run router.py
#docker build -t {name} .
#docker run -p 8501:8501 -d {name}
#docker ps