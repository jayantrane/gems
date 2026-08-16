FROM python:3.12-slim

WORKDIR /app/admin
COPY admin/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "app.py"]
