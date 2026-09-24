# FROM python:3.9

# Stage 1: Build
FROM python:3.11-alpine AS build

WORKDIR /app

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Stage 2: Production
FROM python:3.11-alpine

WORKDIR /app

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=build /app /app

EXPOSE 5002

CMD ["python", "app.py"]