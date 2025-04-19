import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"
BENTOML_URL = "http://localhost:3000"

st.set_page_config(page_title="🎵 歌曲推薦系統", layout="wide")
st.title("🎧 歌曲推薦系統")

st.markdown("---")

# ========== 搜尋推薦功能 ==========
st.header("🔍 顯示歌曲")
st.markdown("在下方按鈕中搜尋推薦歌曲，系統將顯示前 10 首推薦歌曲。")

if st.button("開始搜尋", use_container_width=True):
    with st.spinner("查詢中..."):
        try:
            response = requests.get(f"{FASTAPI_URL}/songs", params={"skip": 0, "limit": 10})
            if response.status_code != 200:
                st.error("無法連接到後端 API")
                st.stop()
                
            results = response.json()
            if results:
                st.success("推薦結果：")
                for idx, song in enumerate(results, 1):
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <strong>{idx}. {song['song_title']}</strong> <br>
                            <em>演出者: {song['artist_id']}</em> <br>
                            <span>熱門度: {song['song_hotness']:.2f}</span> <br>
                            <span>年份: {song['year']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.warning("找不到推薦結果")
        except Exception as e:
            st.error(f"查詢失敗：{e}")

st.markdown("---")

# ========== 新歌輸入與預測功能 ==========
st.header("📈 新歌上架與熱門度預測")
st.markdown("填寫以下表單，系統將預測歌曲的熱門程度並儲存至資料庫。")

with st.form("new_song_form"):
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("🎵 歌曲名稱", placeholder="例如：Shape of You")
        artist = st.text_input("🎤 演出者", placeholder="例如：Ed Sheeran")
    with col2:
        tempo = st.slider("🎚️ Tempo (BPM)", 60, 200, 120)
        danceability = st.slider("💃 Danceability", 0.0, 1.0, 0.5)
        energy = st.slider("⚡ Energy", 0.0, 1.0, 0.6)
        acousticness = st.slider("🎸 Acousticness", 0.0, 1.0, 0.2)

    submitted = st.form_submit_button("預測熱門度並儲存")

if submitted:
    features = {
        "title": title,
        "artist": artist,
        "tempo": tempo,
        "danceability": danceability,
        "energy": energy,
        "acousticness": acousticness
    }

    with st.spinner("呼叫模型預測中..."):
        try:
            pred = requests.post(f"{BENTOML_URL}/predict", json=features).json()
            popularity = pred.get("popularity")
            if popularity is not None:
                st.success(f"✅ 預測熱門程度：{popularity:.2f}")
                st.info("正在將新歌資料儲存至資料庫...")
                save_payload = {**features, "popularity": popularity}
                save_res = requests.post(f"{FASTAPI_URL}/songs/add", json=save_payload)
                if save_res.status_code == 200:
                    st.success("歌曲成功儲存！")
                else:
                    st.error("儲存失敗，請檢查後端 API")
            else:
                st.warning("模型預測失敗")
        except Exception as e:
            st.error(f"預測或儲存錯誤：{e}")