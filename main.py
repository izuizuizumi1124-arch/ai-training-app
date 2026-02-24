import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 初期設定 ---
st.set_page_config(page_title="AI研修ポータル", layout="wide")

# ファイルパスの設定
SURVEY_FILE = "survey_results.csv"
AGENDA_FILE = "agenda.csv"

st.title("🤖 AI研修・運営ポータル")

# サイドバーメニュー
menu = st.sidebar.radio("メニューを選択", ["受講者：アンケート回答", "受講者：年間研修スケジュール", "管理者：アジェンダ作成", "管理者：集計・分析"])

# --- 1. 受講者：アンケート回答 ---
if menu == "受講者：アンケート回答":
    st.header("📋 本日の研修アンケート")
    with st.form("survey_form", clear_on_submit=True):
        q1 = st.radio("① 本日の研修で自身のAIスキルは向上しましたか？", ["はい", "いいえ", "変わらない"])
        q2 = st.text_area("② AI研修で学びたい事は何ですか？（自由入力）")
        submitted = st.form_submit_button("回答を送信")
        if submitted:
            new_data = pd.DataFrame({"日付": [datetime.now().strftime("%Y-%m-%d %H:%M")], "スキル向上": [q1], "学びたい事": [q2]})
            new_data.to_csv(SURVEY_FILE, mode='a', index=False, header=not os.path.exists(SURVEY_FILE), encoding='utf-8-sig')
            st.success("回答ありがとうございました！")
            st.balloons()

# --- 2. 受講者：年間研修スケジュール ---
elif menu == "受講者：年間研修スケジュール":
    st.header("📅 年間研修スケジュール")
    if os.path.exists(AGENDA_FILE):
        df_agenda = pd.read_csv(AGENDA_FILE)
        # 月順にソートして表示
        df_agenda['月_数値'] = df_agenda['月'].str.replace('月','').astype(int)
        df_agenda = df_agenda.sort_values('月_数値').drop(columns=['月_数値'])
        st.table(df_agenda)
    else:
        st.info("現在、研修計画を策定中です。公開をお待ちください。")

# --- 3. 管理者：アジェンダ作成 ---
elif menu == "管理者：アジェンダ作成":
    st.header("⚙️ 管理者用：アジェンダ登録・編集")
    
    # 入力フォーム
    with st.expander("新しい月のアジェンダを追加する"):
        month = st.selectbox("対象月", [f"{i}月" for i in range(1, 13)])
        topic = st.text_input("議題（例：画像生成AIの活用）")
        goal = st.text_area("目的（例：バナー作成の効率化）")
        
        if st.button("アジェンダを保存"):
            new_agenda = pd.DataFrame({"月": [month], "議題": [topic], "目的": [goal]})
            new_agenda.to_csv(AGENDA_FILE, mode='a', index=False, header=not os.path.exists(AGENDA_FILE), encoding='utf-8-sig')
            st.success(f"{month}の計画を保存しました。")
            st.rerun() # 画面を更新して一覧に反映

    # 一覧表示・管理
    st.divider()
    st.subheader("🗓️ 現在登録済みの計画一覧")
    if os.path.exists(AGENDA_FILE):
        df_display = pd.read_csv(AGENDA_FILE)
        st.dataframe(df_display, use_container_width=True)
        
        if st.button("全計画をリセット（削除）"):
            if os.path.exists(AGENDA_FILE):
                os.remove(AGENDA_FILE)
                st.warning("すべての計画を削除しました。")
                st.rerun()
    else:
        st.write("登録されたデータはありません。")

# --- 4. 管理者：集計・分析 ---
elif menu == "管理者：集計・分析":
    st.header("📊 アンケート集計結果")
    if os.path.exists(SURVEY_FILE):
        df = pd.read_csv(SURVEY_FILE)
        st.subheader("スキル向上度の推移")
        fig = px.pie(df, names='スキル向上', color='スキル向上',
                     color_discrete_map={'はい':'#00CC96', 'いいえ':'#EF553B', '変わらない':'#AB63FA'})
        st.plotly_chart(fig)
        st.subheader("自由記述：学びたい事")
        st.write(df['学びたい事'].dropna().tolist())
    else:
        st.warning("まだ回答データがありません。")
