FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir . \
    && addgroup --system worker \
    && adduser --system --ingroup worker worker
USER worker
CMD ["celery", "-A", "app.celery_app:celery_app", "worker", "--loglevel=INFO"]
