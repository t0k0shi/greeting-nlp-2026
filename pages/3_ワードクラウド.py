import pathlib
from collections import Counter

import streamlit as st
from wordcloud import WordCloud
from nlp import (
    filter_by_groups,
    group_filter_widget,
    load_companies,
    load_tokens,
)

st.set_page_config(page_title="ワードクラウド", layout="wide")
st.title("ワードクラウド")

companies = load_companies()
tokens = load_tokens()

selected_groups = group_filter_widget(companies)
filtered = filter_by_groups(tokens, companies, selected_groups)

freq = Counter(filtered["lemma"])

# 日本語フォント検索
font_path = None
candidates = [
    pathlib.Path(__file__).parent.parent / "fonts" / "NotoSansJP-Regular.ttf",
    pathlib.Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    pathlib.Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
    pathlib.Path("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"),
    pathlib.Path("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"),
]
for c in candidates:
    if c.exists():
        font_path = str(c)
        break

if not freq:
    st.warning("表示するデータがありません。")
else:
    wc = WordCloud(
        font_path=font_path,
        width=1200,
        height=600,
        background_color="white",
        max_words=200,
        colormap="viridis",
    ).generate_from_frequencies(freq)

    st.image(wc.to_array(), use_container_width=True)
