from Tables.funds import MutualFunds, InvestmentRecords
from Utils.utils import db_commit, serialize
from scipy import optimize
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import asc
from time import sleep
from datetime import datetime
import pandas as pd
import requests


def input_funds(st, **kwargs):
    mf_title = st.sidebar.title("Add New Mututal Funds")
    mf_name = st.sidebar.text_input("Mutual Fund Name", "IDFC Banking & PSU Fund - Direct Growth")
    mf_code = st.sidebar.text_input("Fund Code", "INF194K015G8")
    button = st.sidebar.button("Add Mutual Fund")
    st.text("")
    if button:
        add_funds(mf_name, mf_code, **kwargs)
        success = st.sidebar.success("Funds Added Successfully!")
        sleep(5)
        success.empty()


def add_funds(mf_name, mf_code, **kwargs):
    db_session = kwargs.get("db_session")
    updated_at = datetime.utcnow()
    insert_instance = insert(MutualFunds).values(
        name=mf_name,
        identifier=mf_code,
        is_deleted=False,
        updated_at=updated_at,
    )
    db_commit(db_session, insert_instance)


def add_investment(name, date, nav, units, **kwargs):
    db_session = kwargs.get("db_session")
    updated_at = datetime.utcnow()
    reqd_cols = [MutualFunds.identifier]
    query = db_session.query(*reqd_cols)\
        .filter(MutualFunds.name == name)\
        .filter(MutualFunds.is_deleted == False)\
        .limit(1)\
        .all()
    results = [serialize(result_instance=result_instance, reqd_cols=reqd_cols) for result_instance in query]
    fund_identifier = ""
    for result in results:
        fund_identifier = result.get(MutualFunds.identifier.name)
    insert_instance = insert(InvestmentRecords).values(
        fund_identifier=fund_identifier,
        nav=nav,
        units=units,
        execution_date=date,
        is_deleted=False,
        updated_at=updated_at
    )
    db_commit(db_session, insert_instance)


def get_funds(**kwargs):
    db_session = kwargs.get('db_session')
    remove_session = kwargs.get('remove_session', True)
    reqd_cols = [MutualFunds.name]
    query = db_session.query(*reqd_cols)\
        .filter(MutualFunds.is_deleted == False)\
        .all()
    results = [serialize(result_instance=result_instance, reqd_cols=reqd_cols) for result_instance in query]
    funds = []
    for result in results:
        funds.append(result.get(MutualFunds.name.name))
    if remove_session:
        db_session.remove()
    return funds


def get_current_navs(**kwargs):
    identifiers = kwargs.get("identifiers")
    mf_navs_url = kwargs.get("mf_navs_url")
    response = requests.get(mf_navs_url)
    raw_response = response.text
    current_navs = {}
    for idx, response in enumerate(raw_response.split("\n")):
        if idx == 0:
            continue
        row = response.split(";")
        if len(row) < 2:
            continue
        if row[1] in identifiers:
            current_navs[row[1]] = float(row[-2])
        elif row[2] in identifiers:
            current_navs[row[2]] = float(row[-2])
    return current_navs


def get_reports(**kwargs):
    db_session = kwargs.get('db_session')
    selection_values = kwargs.get('selection_values')
    reqd_cols = [InvestmentRecords.execution_date, InvestmentRecords.nav,
                 InvestmentRecords.units, MutualFunds.name, InvestmentRecords.fund_identifier]
    query = db_session.query(*reqd_cols)\
        .join(MutualFunds, MutualFunds.identifier == InvestmentRecords.fund_identifier)\
        .filter(MutualFunds.name.in_(selection_values))\
        .filter(InvestmentRecords.is_deleted == False)\
        .filter(MutualFunds.is_deleted == False)\
        .order_by(asc(InvestmentRecords.execution_date))\
        .all()
    results = [serialize(result_instance=result_instance, reqd_cols=reqd_cols) for result_instance in query]
    df = pd.DataFrame(columns=["Fund Name", "Fund Identifier", "Date of Execution", "NAV",
                               "Units", "Value", "Current Nav", "Current Value", "Profit/Loss"])
    fund_identifiers = set()
    for idx, result in enumerate(results):
        name = result.get(MutualFunds.name.name)
        execution_date = result.get(InvestmentRecords.execution_date.name)
        nav = result.get(InvestmentRecords.nav.name)
        units = result.get(InvestmentRecords.units.name)
        fund_identifier = result.get(InvestmentRecords.fund_identifier.name)
        fund_identifiers.add(fund_identifier)
        df.loc[idx] = [
            name,
            fund_identifier,
            execution_date.date(),
            nav,
            units,
            nav * units,
            0,
            0,
            0
        ]
    current_navs = get_current_navs(identifiers=fund_identifiers, **kwargs)
    df["Current Nav"] = df.apply(lambda x: current_navs[x["Fund Identifier"]], axis=1)
    df["Current Value"] = df.apply(lambda x: x["Units"] * x["Current Nav"], axis=1)
    df["Profit/Loss"] = df.apply(lambda x: x["Current Value"] - x["Value"], axis=1)
    return df


def calculate_xirr(df):
    cashflows = df["Value"].tolist()
    st.write(cashflows)
    dates = df["Date of Execution"].tolist()
    t0 = dates[0]
    current_date = datetime.now().date()
    dates.append(current_date)
    current_value = -sum(df["Current Value"])
    cashflows.append(current_value)
    xirr = optimize.newton(lambda r: sum([cf / (1 + r) ** ((dates[idx] - t0).days / 365) for idx, cf in enumerate(cashflows)]), 0.1)
    xirr = round(100 * xirr, 2)
    return xirr


def select_funds(st, **kwargs):
    st.sidebar.title("View Investment Report")
    funds = get_funds(remove_session=False, **kwargs)
    selection_values = st.sidebar.multiselect("Select Mutual Fund", funds)
    button = st.sidebar.button("View Report")
    st.text("")
    if button and len(selection_values) > 0:
        df = get_reports(selection_values=selection_values, **kwargs)
        for selection_value in selection_values:
            st.write(f"**{selection_value}**")
            _df = df[df["Fund Name"] == selection_value]
            _df = _df.drop(columns=["Fund Name", "Fund Identifier"])
            xirr = calculate_xirr(_df)
            _df.loc["Total"] = ["", "", sum(_df["Units"]), sum(_df["Value"]), "", sum(_df["Current Value"]), sum(_df["Profit/Loss"])]
            _df["Profit/Loss"] = _df.apply(lambda x: round(x["Profit/Loss"], 3), axis=1)
            _df_styled = _df.style\
                .applymap(
                    lambda x: "color: green" if x > 0 else "color: red",
                    subset=pd.IndexSlice[_df.index[:-1], ["Value"]]
                ).applymap(
                    lambda x: "background: #d2f8d2" if x > 0 else "background: #ffcccb",
                    subset=pd.IndexSlice[_df.index[:-1], ["Value"]]
                ).applymap(
                    lambda x: "color: green" if x > 0 else "color: red",
                    subset=pd.IndexSlice[:, ["Profit/Loss"]]
                ).applymap(
                    lambda x: "background: #d2f8d2" if x > 0 else "background: #ffcccb",
                    subset=pd.IndexSlice[:, ["Profit/Loss"]]
                )

            st.table(_df_styled)
            absolute_rr = round(100 * (_df["Current Value"]["Total"] / _df["Value"]["Total"] - 1), 2)
            st.write(f"**XIRR (Internal Rate of Return):** {xirr}%")
            st.write(f"**Absolute Rate of Return:** {absolute_rr}%")
        sorted_df = df.sort_values("Date of Execution")
        xirr = calculate_xirr(sorted_df)
        total_current_value = sum(df["Current Value"])
        total_value = sum(df["Value"])
        absolute_rr = round(100 * (total_current_value / total_value - 1), 2)
        st.write(f"**Total Investment Value:** Rs. {round(total_value, 2)}")
        st.write(f"**Total Current Value:** Rs. {round(total_current_value, 2)}")
        st.write(f"**Overall XIRR (Internal Rate of Return):** {xirr}%")
        st.write(f"**Overall Absolute Rate of Return:** {absolute_rr}%")


def input_investment(st, **kwargs):
    st.sidebar.title("Add Investment")
    funds = get_funds(**kwargs)
    selection_value = st.sidebar.selectbox("Select Mutual Fund", funds)
    date = st.sidebar.date_input("Enter Date of investment")
    nav = st.sidebar.number_input("Enter NAV as on investment date", format="%f")
    units = st.sidebar.number_input("Enter Units allocated", format="%f")
    button = st.sidebar.button("Add Investment")
    st.text("")
    if button:
        add_investment(selection_value, date, nav, units, **kwargs)
        success = st.sidebar.success("Investment Added Successfully!")
        sleep(5)
        success.empty()
