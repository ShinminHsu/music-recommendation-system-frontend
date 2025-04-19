import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.set_page_config(page_title="音樂推薦系統", layout="wide")
st.title("🎵 音樂推薦系統")

# 建立兩個 tab
tab1, tab2 = st.tabs(["使用者查詢", "推薦與歌曲清單"])

# Tab 1: 查詢使用者 ID
with tab1:
    st.header("🔍 查詢使用者列表")
    if st.button("取得前 10 位使用者"):
        try:
            response = requests.get(f"{FASTAPI_URL}/users")
            if response.status_code == 200:
                users = response.json()
                st.write("使用者 ID 清單：")
                st.table(users[:10])
            else:
                st.error(f"取得失敗：{response.status_code}")
        except Exception as e:
            st.error(f"錯誤：{e}")

# Tab 2: 推薦與歌曲清單
with tab2:
    st.header("🎧 使用者推薦")

    # 先抓前 10 位 user id 作為選單選項
    try:
        user_list_resp = requests.get(f"{FASTAPI_URL}/users/")
        user_ids = user_list_resp.json()[:10] if user_list_resp.status_code == 200 else []
    except:
        user_ids = []

    selected_user = st.selectbox("選擇一位使用者", user_ids)

    if st.button("取得推薦歌曲") and selected_user:
        try:
            rec_response = requests.get(f"{FASTAPI_URL}/users/{selected_user}/recommendations")
            if rec_response.status_code == 200:
                data = rec_response.json()
                st.subheader("✨ 推薦歌曲")
                
                for item in data:
                    song = item["song"]
                    artist_name = item["artist_name"]

                    with st.container():
                        st.markdown(f"""
                        <div style='border: 1px solid #ddd; padding: 16px; border-radius: 12px; margin-bottom: 12px; background-color: #f9f9f9;'>
                            <h4 style='margin-bottom: 4px; font-size: 20px;'>🎵 {song['song_title']} </h4>
                            <p style='margin: 0; font-size: 16px;'><b>{artist_name}</b></p>
                        </div>
                        """, unsafe_allow_html=True)

            else:
                st.error(f"取得推薦失敗：{rec_response.status_code}")
        except Exception as e:
            st.error(f"錯誤：{e}")

    st.divider()

    # 下半部：所有歌曲清單
    st.subheader("🎼 歌曲清單")
    if st.button("取得 10 首歌曲"):
        try:
            songs_response = requests.get(f"{FASTAPI_URL}/songs", params={"skip": 0, "limit": 10})
            if songs_response.status_code == 200:
                data = songs_response.json()

                cols = st.columns(5)  # 5 columns for a 5x2 grid
                for idx, item in enumerate(data):
                    song = item["song"]
                    artist_name = item["artist_name"]
                    col = cols[idx % 5]  # Cycle through the 5 columns
                    with col:
                        st.markdown(f"""
                        <div style='border: 1px solid #ddd; padding: 16px; border-radius: 12px; margin-bottom: 12px; background-color: #f9f9f9; height: 200px; display: flex; flex-direction: column; justify-content: space-between;'>
                            <h4 style='margin-bottom: 4px; font-size: 20px;'>🎵 {song['song_title']} </h4>
                            <p style='margin: 0; font-size: 16px;'><b>{artist_name}</b></p>
                        </div>
                        """, unsafe_allow_html=True)

            else:
                st.error(f"取得失敗：{songs_response.status_code}")
        except Exception as e:
            st.error(f"錯誤：{e}")
