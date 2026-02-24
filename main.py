import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 初期設定 ---
st.set_page_config(page_title="AI研修管理システム", layout="wide")

# 保存用CSVファイル名
CSV_FILE = "survey_results.csv"

# タイトル
st.title("🤖 AI研修・運営ポータル")

# サイドバーでメニュー切り替え
menu = st.sidebar.radio("メニューを選択", ["受講者：アンケート回答", "管理者：アジェンダ作成", "管理者：集計・分析"])

# --- 1. 受講者：アンケート回答 ---
if menu == "受講者：アンケート回答":
    st.header("📋 本日の研修アンケート")
    st.info("研修お疲れ様でした！以下の回答をお願いします。")
    
    with st.form("survey_form", clear_on_submit=True):
        q1 = st.radio(
            "① 本日の研修で自身のAIスキルは向上しましたか？",
            ["はい", "いいえ", "変わらない"],
            index=0
        )
        q2 = st.text_area("② AI研修で学びたい事は何ですか？（自由入力）")
        
        submitted = st.form_submit_button("回答を送信")
        
        if submitted:
            # データの作成
            new_data = pd.DataFrame({
                "日付": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                "スキル向上": [q1],
                "学びたい事": [q2]
            })
            
            # CSVへの保存処理（追記モード）
            try:
                # ファイルが存在しない場合はヘッダーあり、存在する場合はヘッダーなしで追記
                file_exists = os.path.isfile(CSV_FILE)
                new_data.to_csv(CSV_FILE, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
                st.success("✅ 回答ありがとうございました！データは正常に集計用ファイルへ保存されました。")
                st.balloons() # 演出用
            except Exception as e:
                st.error(f"❌ エラーが発生しました。管理者に連絡してください: {e}")

# --- 2. 管理者：アジェンダ作成 ---
elif menu == "管理者：アジェンダ作成":
    st.header("📅 研修アジェンダ設定")
    st.write("年間の研修計画をこちらで管理できます。")
    
    with st.expander("新規アジェンダの登録（入力例）"):
        month = st.selectbox("対象月", [f"{i}月" for i in range(1, 13)])
        topic = st.text_input("議題", placeholder="例：ChatGPTを使った業務自動化")
        goal = st.text_area("目的", placeholder="例：プロンプトの基本を理解し、日常業務の30分を削減する")
        
        if st.button("アジェンダを保存"):
            # ここではデモとして画面表示のみ（必要に応じて別途CSV保存も可能）
            st.success(f"【保存完了】 {month}のテーマは「{topic}」に設定されました。")

# --- 3. 管理者：集計・分析 ---
elif menu == "管理者：集計・分析":
    st.header("📊 アンケート集計結果")
    
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        
        # 集計データの表示
        st.subheader("現在の回答データ")
        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)
        
        with col1:
            # 円グラフの作成
            st.subheader("スキル向上度の割合")
            fig = px.pie(df, names='スキル向上', 
                         color='スキル向上',
                         color_discrete_map={'はい':'#00CC96', 'いいえ':'#EF553B', '変わらない':'#AB63FA'})
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # 自由記述のリスト化
            st.subheader("学びたい事（生の声）")
            for i, text in enumerate(df['学びたい事'].dropna()):
                if text.strip():
                    st.write(f"{i+1}. {text}")

        # CSVダウンロードボタン（Excelで開く用）
        st.divider()
        csv_data = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="集計データをCSVとしてダウンロード",
            data=csv_data,
            file_name=f"ai_survey_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.warning("まだ回答データがありません。受講者画面からテスト回答を行ってください。")