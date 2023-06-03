FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app
COPY . /usr/src/app

# install poetry
RUN pip install poetry

# install dependencies
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
ENV MODULE_NAME=main
ENV APP_NAME=app
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]