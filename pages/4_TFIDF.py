import plotly.express as px
import streamlit as st
from nlp import load_companies, load_tfidf

st.set_page_config(page_title="TF-IDF", layout="wide")
st.title("TF-IDF 分析")

companies = load_companies()
tfidf = load_tfidf()

# 企業名のマッピング
id_to_name = dict(zip(companies["id"], companies["name"]))

company_names = [id_to_name.get(cid, cid) for cid in sorted(tfidf["company_id"].unique())]
selected_name = st.sidebar.selectbox("企業を選択", company_names)
top_n = st.sidebar.slider("表示件数", 10, 50, 20)

# 選択された企業名 → id
name_to_id = {v: k for k, v in id_to_name.items()}
selected_id = name_to_id.get(selected_name, selected_name)

company_tfidf = (
    tfidf[tfidf["company_id"] == selected_id]
    .sort_values("score", ascending=False)
    .head(top_n)
)

fig = px.bar(
    company_tfidf,
    x="score",
    y="word",
    orientation="h",
    title=f"{selected_name} の TF-IDF 上位 {top_n} 語",
    labels={"score": "TF-IDF スコア", "word": "単語"},
)
fig.update_layout(yaxis=dict(autorange="reversed"), height=max(400, top_n * 20))
st.plotly_chart(fig, use_container_width=True)

st.subheader("データテーブル")
st.dataframe(
    company_tfidf[["word", "score"]].rename(
        columns={"word": "単語", "score": "スコア"}
    ),
    use_container_width=True,
    hide_index=True,
)
