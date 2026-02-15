# 企業トップ年頭挨拶 NLP分析ダッシュボード（2026年版）

23社の企業トップによる2026年の年頭挨拶を [Ginza](https://megagonlabs.github.io/ginza/) で形態素解析し、[Streamlit](https://streamlit.io/) で可視化するダッシュボードです。

**デモ**: https://greeting-nlp-2026-nemvn3qgkewakxz5g4jcnb.streamlit.app/

## 分析ページ

| ページ | 内容 | ライブラリ |
|--------|------|-----------|
| 頻度分析 | 頻出単語の横棒グラフ | Plotly |
| 共起分析 | 共起ネットワークグラフ | NetworkX + matplotlib |
| ワードクラウド | WordCloud 画像 | wordcloud |
| TF-IDF | 企業別の特徴語ランキング | Plotly |
| 類似度 | 23社間コサイン類似度ヒートマップ | Plotly |

## 対象企業（23社）

| グループ | 企業 |
|---------|------|
| NTT系（8社） | NTT持株、ドコモ、ドコモビジネス、NTTデータ、NTTデータES、NTTデータ先端技術、NTT東日本、NTT西日本 |
| 商社（4社） | 三菱商事、丸紅、伊藤忠商事、住友商事 |
| 他業種（11社） | トヨタ自動車、ファミリーマート、セブン＆アイ、JFEスチール、積水化学、野村ホールディングス、三井E&S、IHI、日本マイクロソフト、日本郵船、三菱マテリアル |

## アーキテクチャ

Ginza（約700MB）は Streamlit Community Cloud のメモリ上限（約1GB）に収まらないため、**事前計算方式**を採用しています。

```
[ローカル]                         [Streamlit Community Cloud]

texts/*.txt → preprocess.py        data/*.csv → Streamlit（CSV読込のみ）
               Ginza v5.2.0                      Ginza不要 → メモリ ~100MB
               ↓
            data/*.csv → git push
```

## ローカルで動かす

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## 事前計算の再実行

形態素解析やストップワードを変更したい場合は、元リポジトリの `preprocess.py` を使用します。

```bash
pip install -r requirements-preprocess.txt
python preprocess.py
```

## 技術スタック

- **NLP**: Ginza v5.2.0 + SudachiDict（mode A）
- **フロントエンド**: Streamlit
- **可視化**: Plotly / NetworkX / matplotlib / wordcloud
- **デプロイ**: Streamlit Community Cloud
