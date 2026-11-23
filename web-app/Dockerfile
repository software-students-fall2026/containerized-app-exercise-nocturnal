ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --dev

ADD . .

CMD ["python3", "-m", "flask", "--app", "run", "--host=0.0.0.0", "--port=5000"]
