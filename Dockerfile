# docker build -t fastapi .
# docker image tag fastapi_api dineshaponso/fastapi
# docker image ls 
# docker login

FROM python:3.10.2

WORKDIR /usr/scr/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","app.main_sqlalchemy:app","--host","0.0.0.0","--port","8000"]