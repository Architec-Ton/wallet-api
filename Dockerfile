FROM python:3.12

RUN apt update && apt -y upgrade

RUN pip install pipenv

WORKDIR /walletapi

COPY ./Pipfile ./Pipfile.lock ./

RUN pipenv requirements > requirements.txt
RUN pip install --user -r requirements.txt

COPY ./ ./

CMD python -m uvicorn wallet.app:app --host 0.0.0.0 --port 8000