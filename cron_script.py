from Sessions.db_session import DB
from Tables.funds import NavHistories
from datetime import datetime
from os import environ
import requests

db_user = environ.get('DB_USER')
db_password = environ.get('DB_PASSWORD')
db_host = environ.get('DB_HOST')
db_port = environ.get('DB_PORT')
db_database = environ.get('DB_DATABASE')
db_config = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
db_instance = DB(db_config)
db_session = db_instance.get_session()
mf_navs_url = environ.get('MF_NAVS_URL')

response = requests.get(mf_navs_url)
raw_response = response.text
current_navs = {}
objects = []
for idx, response in enumerate(raw_response.split("\n")):
    if idx == 0:
        continue
    row = response.split(";")
    if len(row) < 2 or row[-2] == "N.A.":
        continue
    fund_identifier = row[1]
    if row[1] == "-":
        fund_identifier = row[2]
    objects.append(
        NavHistories(
            fund_identifier=fund_identifier,
            fund_name=row[3],
            nav=float(row[-2]),
            date=datetime.now().date(),
            is_deleted=False,
            updated_at=datetime.now()
        )
    )
db_session.bulk_save_objects(objects)
db_session.commit()
db_session.close()
db_session.remove()
