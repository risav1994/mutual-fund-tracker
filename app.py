from Funds import funds
from Sessions.db_session import DB
import streamlit as st
from os import environ

db_user = environ.get('DB_USER')
db_password = environ.get('DB_PASSWORD')
db_host = environ.get('DB_HOST')
db_port = environ.get('DB_PORT')
db_database = environ.get('DB_DATABASE')
db_config = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
db_instance = DB(db_config)
db_session = db_instance.get_session()
mf_navs_url = environ.get('MF_NAVS_URL')

st.set_page_config(page_title="Investment Tracker")

funds.select_funds(st, db_session=db_session, mf_navs_url=mf_navs_url)
funds.input_funds(st, db_session=db_session)
funds.input_investment(st, db_session=db_session)
