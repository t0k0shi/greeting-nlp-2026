import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
from nlp import (
    filter_by_groups,
    group_filter_widget,
    load_companies,
    load_cooccurrence,
)

st.set_page_config(page_title="共起分析", layout="wide")
st.title("共起ネットワーク")

companies = load_companies()
cooccurrence = load_cooccurrence()

selected_groups = group_filter_widget(companies)
min_count = st.sidebar.slider("最小共起回数", 1, 20, 5)
top_n = st.sidebar.slider("表示ペア数", 10, 100, 50)

filtered = filter_by_groups(cooccurrence, companies, selected_groups)
# 全社合算
agg = (
    filtered.groupby(["word1", "word2"])["count"]
    .sum()
    .reset_index()
    .sort_values("count", ascending=False)
)
agg = agg[agg["count"] >= min_count].head(top_n)

if agg.empty:
    st.warning("条件に合う共起ペアがありません。最小共起回数を下げてください。")
else:
    G = nx.Graph()
    for _, row in agg.iterrows():
        G.add_edge(row["word1"], row["word2"], weight=row["count"])

    fig, ax = plt.subplots(figsize=(12, 10))
    pos = nx.spring_layout(G, k=2, seed=42)
    weights = [G[u][v]["weight"] for u, v in G.edges()]
    max_w = max(weights) if weights else 1
    widths = [w / max_w * 5 for w in weights]

    nx.draw_networkx_nodes(G, pos, node_size=600, node_color="#4A90D9", alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.5, edge_color="#888", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif", ax=ax)
    ax.set_title(f"共起ネットワーク（上位 {len(agg)} ペア）")
    ax.axis("off")
    st.pyplot(fig)

    st.subheader("共起ペアテーブル")
    st.dataframe(
        agg.rename(columns={"word1": "単語1", "word2": "単語2", "count": "共起回数"}),
        use_container_width=True,
        hide_index=True,
    )
