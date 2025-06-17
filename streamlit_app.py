import streamlit as st
import requests

st.set_page_config(page_title="🧠 RAG Demo", layout="wide")
st.title("🧠 Local RAG 查詢助手")

query = st.text_input("輸入你的問題：", placeholder="例如：Who created Python?")

if st.button("送出查詢") and query:
    with st.spinner("⏳ 查詢中..."):
        try:
            res = requests.post("http://backend:8000/query", json={"query": query})
            if res.ok:
                data = res.json()
                st.markdown("### 💬 回答：")
                st.success(data["response"])

                st.markdown("### 📚 參考內容：")
                st.info(data["context"])
            else:
                st.error(f"❌ 錯誤：{res.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ 連線失敗：{e}")
