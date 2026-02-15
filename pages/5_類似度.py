import plotly.express as px
import streamlit as st
from nlp import load_companies, load_similarity

st.set_page_config(page_title="類似度ヒートマップ", layout="wide")
st.title("企業間類似度ヒートマップ")

companies = load_companies()
similarity = load_similarity()

# グループフィルタ
groups = companies["group"].unique().tolist()
selected_groups = st.sidebar.multiselect("企業グループ", groups, default=groups)
target_ids = companies[companies["group"].isin(selected_groups)]["id"].tolist()

# フィルタ適用
sim_filtered = similarity.loc[
    similarity.index.isin(target_ids),
    similarity.columns.isin(target_ids),
]

# id → 企業名に変換
id_to_name = dict(zip(companies["id"], companies["name"]))
sim_display = sim_filtered.rename(index=id_to_name, columns=id_to_name)

fig = px.imshow(
    sim_display,
    color_continuous_scale="Blues",
    aspect="auto",
    title="コサイン類似度（TF-IDFベース）",
    labels=dict(color="類似度"),
)
fig.update_layout(height=700)
st.plotly_chart(fig, use_container_width=True)

# 類似度上位ペア
st.subheader("類似度 上位ペア")
pairs = []
ids = sim_filtered.index.tolist()
for i, id1 in enumerate(ids):
    for j, id2 in enumerate(ids):
        if i < j:
            pairs.append({
                "企業1": id_to_name.get(id1, id1),
                "企業2": id_to_name.get(id2, id2),
                "類似度": round(sim_filtered.loc[id1, id2], 4),
            })

import pandas as pd

pairs_df = pd.DataFrame(pairs).sort_values("類似度", ascending=False).head(20)
st.dataframe(pairs_df, use_container_width=True, hide_index=True)
