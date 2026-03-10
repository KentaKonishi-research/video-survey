import streamlit as st
import pandas as pd
import random
import os
import datetime

# --- 設定 ---
# ※オンライン版ではデータ保存に工夫が必要なため、画面にダウンロードボタンを表示させます
if 'results' not in st.session_state:
    st.session_state.results = []

VIDEO_DIR = "videos"
VIDEO_FILES = [
    "C001_002 沈黙①.mov", "C001_002 沈黙②.mov", "K001_004 沈黙①.mov", "K001_004 沈黙②.mov",
    "K002_016 沈黙①.mov", "K002_016 沈黙②.mov", "K006_023 沈黙①.mov", "K006_023 沈黙②.mov",
    "K009_007 沈黙①.mov", "K009_007 沈黙②.mov", "K010_006 沈黙①.mov", "K010_006 沈黙②.mov",
    "K010_013b 沈黙①.mov", "K010_013b 沈黙②.mov", "K012_001 沈黙①.mov", "K012_001 沈黙②.mov",
    "K012_002d 沈黙①.mov", "K012_002d 沈黙②.mov", "T008_022c 沈黙①.mov", "T008_022c 沈黙②.mov",
    "T010_013 沈黙①.mov", "T010_013 沈黙②.mov", "T022_005 沈黙①.mov", "T022_005 沈黙②.mov",
    "T022_012 沈黙①.mov", "T022_012 沈黙②.mov", "T023_007 沈黙①.mov", "T023_007 沈黙②.mov"
]

if 'initialized' not in st.session_state:
    st.session_state.video_order = random.sample(VIDEO_FILES, len(VIDEO_FILES))
    st.session_state.current_idx = 0
    st.session_state.user_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.initialized = True

st.title("動画評価アンケート")

if st.session_state.current_idx >= len(st.session_state.video_order):
    st.header("調査終了")
    st.write("ご協力ありがとうございました。")
    
    # 最後に回答データをCSVとしてダウンロードさせる（オンライン保存の代わり）
    df = pd.DataFrame(st.session_state.results)
    csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("結果をダウンロードしてください", data=csv, file_name=f"result_{st.session_state.user_id}.csv")
else:
    current_video = st.session_state.video_order[st.session_state.current_idx]
    st.write(f"進捗: {st.session_state.current_idx + 1} / {len(VIDEO_FILES)}")
    
    # 動画表示（GitHub上のパスを指定）
    video_path = f"{VIDEO_DIR}/{current_video}"
    st.video(video_path, format="video/quicktime")

    score = st.radio("評価を選択してください（1=低、6=高）", [1,2,3,4,5,6], horizontal=True, index=None, key=current_video)

    if st.button("次へ"):
        if score:
            st.session_state.results.append({
                "video": current_video,
                "score": score,
                "order": st.session_state.current_idx + 1
            })
            st.session_state.current_idx += 1
            st.rerun()
