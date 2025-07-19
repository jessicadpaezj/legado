# ─── BUILD ───────────────────────────────────────────────────
FROM python:3.11-slim AS build
WORKDIR /code
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# ─── RUNTIME ─────────────────────────────────────────────────
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /code
COPY --from=build /root/.local /root/.local
COPY app/ ./app/
CMD ["python", "-m", "app.main"]
