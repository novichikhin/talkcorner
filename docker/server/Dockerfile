FROM python:3.10

WORKDIR .

COPY poetry.lock pyproject.toml ./

RUN python3.10 -m pip install poetry
RUN poetry install --no-dev

COPY . .

EXPOSE 8080

CMD poetry run alembic upgrade head && \
    poetry run python -m talkcorner.server