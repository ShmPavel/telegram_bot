FROM python:3.11-slim

# PYTHONDONTWRITEBYTECODE: не создавать файлы .pyc (мусор в контейнере)
# PYTHONUNBUFFERED: выводить print() и логи сразу в терминал, а не буферизировать их
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /pgdata

COPY requirements.txt .


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]