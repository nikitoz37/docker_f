FROM python:3.12-alpine
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["fastapi", "run", "./main.py"]
# CMD ["python3", "./main.py"]
