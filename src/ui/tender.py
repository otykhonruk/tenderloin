import streamlit as st

from utils.db import QUERIES


# Initialize connection.
conn = st.connection("postgresql", type="sql")

df = conn.query(QUERIES.prozorro.get_tender_by_id.sql,
                params=(st.query_params.doc_id,))

st.write(df)
