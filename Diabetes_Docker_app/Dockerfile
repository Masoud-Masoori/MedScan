FROM python:3.12

WORKDIR /src

COPY model.pkl /src/model.pkl
COPY server.py /src/server.py
COPY requirements.txt /src/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
