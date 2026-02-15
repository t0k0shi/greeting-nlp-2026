import plotly.express as px
import streamlit as st
from nlp import (
    filter_by_groups,
    group_filter_widget,
    load_companies,
    load_tokens,
)

st.set_page_config(page_title="頻度分析", layout="wide")
st.title("頻度分析")

companies = load_companies()
tokens = load_tokens()

selected_groups = group_filter_widget(companies)
top_n = st.sidebar.slider("表示件数", 10, 50, 30)

filtered = filter_by_groups(tokens, companies, selected_groups)
freq = filtered["lemma"].value_counts().head(top_n).reset_index()
freq.columns = ["単語", "出現回数"]

fig = px.bar(
    freq,
    x="出現回数",
    y="単語",
    orientation="h",
    title=f"頻出単語 Top {top_n}",
)
fig.update_layout(yaxis=dict(autorange="reversed"), height=max(400, top_n * 20))
st.plotly_chart(fig, use_container_width=True)

st.subheader("データテーブル")
st.dataframe(freq, use_container_width=True, hide_index=True)
