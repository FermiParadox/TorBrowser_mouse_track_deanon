FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN python -m pip install "pymongo[srv]"

COPY ./config.py /code/config.py
COPY ./src /code/src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port", "8000"]
