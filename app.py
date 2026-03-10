import streamlit as st
import pandas as pd
import random
import datetime

# --- 1. 動画データの設定（ご提示のURLをすべて反映しました） ---
VIDEO_DATA = [
    {"name": "C001_002 沈黙①", "url": "https://youtu.be/-YLyHXWdpwA"},
    {"name": "C001_002 沈黙②", "url": "https://youtu.be/pODWvK-WDCw"},
    {"name": "K001_004 沈黙①", "url": "https://youtu.be/5GvTP5ZsHGc"},
    {"name": "K001_004 沈黙②", "url": "https://youtu.be/T7VrMyrQTcg"},
    {"name": "K002_016 沈黙①", "url": "https://youtu.be/goiuyPzMLBM"},
    {"name": "K002_016 沈黙②", "url": "https://youtu.be/5mM-5vMFpEQ"},
    {"name": "K006_023 沈黙①", "url": "https://youtu.be/UXCatH2-HVo"},
    {"name": "K006_023 沈黙②", "url": "https://youtu.be/oRl-oxeKtsc"},
    {"name": "K009_007 沈黙①", "url": "https://youtu.be/is5AvUX9xI8"},
    {"name": "K009_007 沈黙②", "url": "https://youtu.be/sL2FLEmvJGU"},
    {"name": "K010_006 沈黙①", "url": "https://youtu.be/ceeu3npo9Hs"},
    {"name": "K010_006 沈黙②", "url": "https://youtu.be/VWKiuUMlM6Q"},
    {"name": "K010_013b 沈黙①", "url": "https://youtu.be/J_PbqYE4uos"},
    {"name": "K010_013b 沈黙②", "url": "https://youtu.be/QKX8KcGVmq0"},
    {"name": "K012_001 沈黙①", "url": "https://youtu.be/J9M5A6TYC5k"},
    {"name": "K012_001 沈黙②", "url": "https://youtu.be/bDryDIcuXto"},
    {"name": "K012_002d 沈黙①", "url": "https://youtu.be/B_WtYFZMvss"},
    {"name": "K012_002d 沈黙②", "url": "https://youtu.be/uBgkTO9qu1A"},
    {"name": "T008_022c 沈黙①", "url": "https://youtu.be/2jl8mRNE3uA"},
    {"name": "T008_022c 沈黙②", "url": "https://youtu.be/1nVxZ_tN5Fw"},
    {"name": "T010_013 沈黙①", "url": "https://youtu.be/j_RtuDmBv9A"},
    {"name": "T010_013 沈黙②", "url": "https://youtu.be/fLPhBTsm5tA"},
    {"name": "T022_005 沈黙①", "url": "https://youtu.be/NbFnWbbByMk"},
    {"name": "T022_005 沈黙②", "url": "https://youtu.be/TT4UPh-Xbk0"},
    {"name": "T022_012 沈黙①", "url": "https://youtu.be/XrwElJHHACI"},
    {"name": "T022_012 沈黙②", "url": "https://youtu.be/A0jLMrK99ZU"},
    {"name": "T023_007 沈黙①", "url": "https://youtu.be/tXXRX1aKg_U"},
    {"name": "T023_007 沈黙②", "url": "https://youtu.be/XmmipswjZPE"},
]

# --- 2. セッション管理（回答データや順番の保持） ---
if 'results' not in st.session_state:
    st.session_state.results = []

if 'initialized' not in st.session_state:
    # 28本をランダムにシャッフル
    st.session_state.video_order = random.sample(VIDEO_DATA, len(VIDEO_DATA))
    st.session_state.current_idx = 0
    st.session_state.user_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.initialized = True

# 画面設定
st.set_page_config(page_title="動画評価調査", layout="centered")

# 全ての動画が終わったか判定
if st.session_state.current_idx >= len(st.session_state.video_order):
    st.title("調査終了")
    st.write("全ての回答が完了しました。ご協力ありがとうございました。")
    
    # データの集計
    df = pd.DataFrame(st.session_state.results)
    # 日本語の文字化けを防ぐ設定
    csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    
    st.success("【重要】最後に、以下のボタンを押して回答データをダウンロードしてください。")
    st.download_button(
        label="結果をCSVでダウンロード",
        data=csv,
        file_name=f"survey_result_{st.session_state.user_id}.csv",
        mime="text/csv"
    )
    st.info("ダウンロードしたファイルを、調査担当者へ提出してください。")

else:
    # 現在の動画情報を取得
    current_item = st.session_state.video_order[st.session_state.current_idx]
    progress = st.session_state.current_idx + 1
    total = len(st.session_state.video_order)

    st.title(f"動画評価 ({progress} / {total})")
    st.write("以下の動画を視聴し、評価を選択してください。")

    # --- 3. YouTubeの表示 ---
    st.video(current_item["url"])

    st.divider()

    # --- 4. 評価フォーム ---
    # ラジオボタンの選択肢（keyを動画ごとに変えることでリセットされる）
    score = st.radio(
        "この動画の評価を6段階で選択してください（1=全くあてはまらない、6=非常にあてはまる）",
        options=[1, 2, 3, 4, 5, 6],
        horizontal=True,
        index=None,
        key=f"radio_{st.session_state.current_idx}"
    )

    # 次へボタン
    if st.button("回答して次の動画へ"):
        if score is not None:
            # データの追加
            st.session_state.results.append({
                "user_id": st.session_state.user_id,
                "video_name": current_item["name"],
                "video_url": current_item["url"],
                "presentation_order": progress,
                "rating": score,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            # インデックスを進める
            st.session_state.current_idx += 1
            st.rerun()
        else:
            st.warning("評価を選択してください。")
