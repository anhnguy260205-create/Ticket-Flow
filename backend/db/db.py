import os
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def get_connection():
    db_user = os.environ.get("MYSQL_USER", "ticketflow")
    db_password = os.environ.get("MYSQL_PASSWORD", "ticketflow_pass")
    db_host = os.environ.get("MYSQL_HOST", "localhost")
    db_port = os.environ.get("MYSQL_PORT", "3306")
    db_name = os.environ.get("MYSQL_DATABASE", "ticketflow_db")

    connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return connection_string
