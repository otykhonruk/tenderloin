import streamlit as st

from utils.db import QUERIES


# Initialize connection.
conn = st.connection("postgresql", type="sql")


df = conn.query(QUERIES.prozorro.list_tenders.sql)


st.title('Tenders')
# Print results.
for row in df.itertuples():
    st.page_link('tender.py', query_params={'doc_id': row.doc_id}, label=row.title)

