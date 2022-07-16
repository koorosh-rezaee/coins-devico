FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim
RUN mv /start.sh /app

RUN apt update && apt -y install gcc libgmp3-dev git libpq-dev
RUN useradd -m -d /home/app app && chown -R app:app /home/app && chown -R app:app /app

ENV PATH="/home/app/.local/bin:${PATH}"
ENV MODULE_NAME=coins.web_app
ENV MAX_WORKERS=4

COPY requirements.txt /app
USER app
RUN pip install -r requirements.txt
RUN pip install pydantic[dotenv]

COPY . /app

USER root
RUN chown -R app:app /app
USER app

RUN pip install -e .

CMD ["./start.sh"]