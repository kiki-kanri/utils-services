### Dockerfile

FROM python:3.10.7-slim
LABEL org.opencontainers.image.authors="kiki-kanri"
LABEL version="1.0"

RUN apt-get update
RUN apt-get install -y git gcc

WORKDIR /app

COPY requirements.txt .
RUN python3.10 -m pip install --no-cache-dir -r ./requirements.txt --upgrade
RUN apt-get remove -y git gcc vim make cpp perl lsb-release --purge
RUN apt-get autoremove -y --purge
RUN apt-get autoclean -y
RUN apt-get clean -y
COPY ./ .
RUN chmod a+x ./docker_gunicorn.sh

CMD ["./docker_gunicorn.sh"]