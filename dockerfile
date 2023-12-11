FROM python:3.10-slim
RUN adduser --disabled-password dbmaker
WORKDIR /home/dbmaker/app
RUN apt update && apt install -y nano unixodbc

COPY requirements.txt /home/dbmaker
COPY ../app/sj_backup.sh /home/dbmaker/app/

RUN chmod +x /home/dbmaker/app/sj_backup.sh
RUN pip3 install -r /home/dbmaker/requirements.txt

COPY config/odbcinst.ini /etc/odbcinst.ini
COPY config/odbc.ini /etc/odbc.ini
COPY config/ /config/

ENV 	DB_SETTINGS=/config/db-settings.env \
		DB_CREDENTIALS=/config/db-credentials.env \
		JSONPATH=/config/sanjorge_secrets.json \
		JWT=/config/jwt_params.env \
		LOG_PATH=/home/dbmaker/logs \
		DEBUG=False
