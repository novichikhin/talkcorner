FROM python:3.10

WORKDIR .

COPY pyproject.toml ./

RUN python3.10 -m pip install poetry
RUN poetry install --no-dev

COPY . .

CMD poetry run alembic upgrade head && \
    poetry run python -m talkcorner.server.api