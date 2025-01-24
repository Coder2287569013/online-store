FROM python:3.12.0-slim

FROM python:3.12.0-slim

WORKDIR /online-store

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8080

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]