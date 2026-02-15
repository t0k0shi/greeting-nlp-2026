import streamlit as st
from nlp import load_companies

st.set_page_config(page_title="企業トップ年頭挨拶 NLP分析", layout="wide")

st.title("2026年度 企業トップ年頭挨拶 NLP分析")
st.markdown(
    """
    23社の企業トップによる2026年の年頭挨拶を自然言語処理（NLP）で分析し、
    可視化するダッシュボードです。

    **分析手法**: 頻度分析 / 共起分析 / ワードクラウド / TF-IDF / 類似度ヒートマップ

    左のサイドバーから各分析ページに移動できます。
    """
)

st.subheader("対象企業一覧")
companies = load_companies()
st.dataframe(
    companies[["name", "group", "industry"]].rename(
        columns={"name": "企業名", "group": "グループ", "industry": "業種"}
    ),
    use_container_width=True,
    hide_index=True,
)

st.caption("データ出典: 各社公式サイトの2026年年頭挨拶より")
