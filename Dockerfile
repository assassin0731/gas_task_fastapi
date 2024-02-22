FROM python:3.11

WORKDIR /app


COPY ./requirements.txt /requirements.txt


RUN pip install --no-cache-dir --upgrade -r /requirements.txt


COPY . .

CMD ["alembic", "init", "migrations"]
CMD ["alembic", "revision", "--autogenerate"]
CMD ["alembic", "upgrade", "head"]
CMD ["pip", "show", "fastapi"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
