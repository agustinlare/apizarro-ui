FROM python:3.8

RUN mkdir /apizarro-ui

ENV PORT=8080 \
    FLASK_APP="app.py" \
    FLASK_RUN_HOST="0.0.0.0" \
    FLASK_RUN_PORT=8080 \
    CLUSTER_CONFIG_FILE="./conf/ocpconfig.conf"

COPY . /apizarro-ui

WORKDIR /apizarro-ui

RUN pip install -r requirements.txt

EXPOSE 8080:8080

CMD [ "app.py" ]
ENTRYPOINT [ "python3" ]
