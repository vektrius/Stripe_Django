FROM python:slim
WORKDIR /PaymentApp
COPY poetry.lock pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
