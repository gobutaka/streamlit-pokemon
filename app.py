import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="ポケモン図鑑", layout="wide")

# サイドバーの設定
st.sidebar.title("検索フィルター")
name = st.sidebar.text_input("ポケモン名")
types = st.sidebar.multiselect("タイプ", ("ノーマル", "ほのお", "みず", "でんき", "くさ", "こおり", "かくとう", "どく", "じめん", "ひこう", "エスパー", "むし", "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"), max_selections=2, placeholder="タイプを選択")
ability = st.sidebar.text_input("特性")
with st.sidebar.expander("種族値"):
  min_hp, max_hp = st.select_slider("HP", range(256), value=(0, 255))
  min_atk, max_atk = st.select_slider("攻撃", range(256), value=(0, 255))
  min_def, max_def = st.select_slider("防御", range(256), value=(0, 255))
  min_sp_atk, max_sp_atk = st.select_slider("特攻", range(256), value=(0, 255))
  min_sp_def, max_sp_def = st.select_slider("特防", range(256), value=(0, 255))
  min_speed, max_speed = st.select_slider("素早さ", range(256), value=(0, 255))

# CSVからポケモンのデータを取得する関数
def pokemons():
  return pd.read_csv("pokemons.csv", usecols=["図鑑No.", "名前", "フォルム", "タイプ1", "タイプ2", "HP", "攻撃", "防御", "特攻", "特防", "素早さ", "特性1", "特性2", "夢特性"], index_col=0, keep_default_na=False).sort_values(["図鑑No."])

# フィルタリング
df = pokemons()
df = df[df["名前"].str.contains(name)]
if len(types) == 1:
  df = df[df["タイプ1"].isin(types) | df["タイプ2"].isin(types)]
if len(types) == 2:
  df = df[df["タイプ1"].isin(types) & df["タイプ2"].isin(types)]
df = df[df["特性1"].str.contains(ability) | df["特性2"].str.contains(ability) | df["夢特性"].str.contains(ability)]
df = df[(df["HP"] >= min_hp) & (df["HP"] <= max_hp)]
df = df[(df["攻撃"] >= min_atk) & (df["攻撃"] <= max_atk)]
df = df[(df["防御"] >= min_def) & (df["防御"] <= max_def)]
df = df[(df["特攻"] >= min_sp_atk) & (df["特攻"] <= max_sp_atk)]
df = df[(df["特防"] >= min_sp_def) & (df["特防"] <= max_sp_def)]
df = df[(df["素早さ"] >= min_speed) & (df["素早さ"] <= max_speed)]

# 描画
st.dataframe(df, use_container_width=True)
st.scatter_chart(df, x="素早さ", y="攻撃")
st.scatter_chart(df, x="素早さ", y="特攻")
