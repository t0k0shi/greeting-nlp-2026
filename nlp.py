"""Streamlit 側の共通データ読込・フィルタ処理"""
import pathlib

import pandas as pd
import streamlit as st

DATA_DIR = pathlib.Path(__file__).parent / "data"


@st.cache_data
def load_companies() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "companies.csv")


@st.cache_data
def load_tokens() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "tokens.csv")
    df = df[df["lemma"].str.strip().astype(bool)]  # 空白・改行のみのトークンを除外
    return df


@st.cache_data
def load_tfidf() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "tfidf.csv")


@st.cache_data
def load_cooccurrence() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "cooccurrence.csv")


@st.cache_data
def load_similarity() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "similarity.csv", index_col=0)


def filter_by_groups(
    df: pd.DataFrame, companies: pd.DataFrame, selected_groups: list[str]
) -> pd.DataFrame:
    """企業グループでフィルタリング"""
    target_ids = companies[companies["group"].isin(selected_groups)]["id"].tolist()
    return df[df["company_id"].isin(target_ids)]


def group_filter_widget(companies: pd.DataFrame) -> list[str]:
    """サイドバーに企業グループフィルタを表示（共通）"""
    groups = companies["group"].unique().tolist()
    return st.sidebar.multiselect("企業グループ", groups, default=groups)
