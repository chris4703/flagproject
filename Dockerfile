FROM python:3.13-slim-bookworm@sha256:a5a7017efc5969e00ae2b91c8eb0631049a569652aa4ffc4501769049ae45c72
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 NAV_BIND=0.0.0.0 NAV_PORT=8080 NAV_DB=/state/navigator.sqlite3
RUN mkdir /state && chown 10001:10001 /state
COPY navigator navigator
COPY inputs inputs
COPY web web
COPY server.py .
USER 10001:10001
EXPOSE 8080
CMD ["python", "server.py"]
