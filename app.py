import streamlit as st
import pandas as pd
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# ==========================================
# 1. 環境設定 & APIキー読み込み
# ==========================================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error(".envファイルに GEMINI_API_KEY を設定してください！")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ==========================================
# 2. 究極デザイン (視覚特化・白文字強調・ゴールドアクセント)
# ==========================================
st.set_page_config(page_title="HealthyAI ⚡", layout="wide", page_icon="🏋️‍♂️")

st.markdown("""
    <style>
    /* 全体の背景：高級感のあるダークグレー */
    .stApp {
        background: radial-gradient(circle, #1e1e1e 0%, #000000 100%);
        color: #FFFFFF !important;
    }

    /* 基本文字はすべて白 */
    p, li, label, div, span, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* AIのチャットバブル：ゴールドの枠線で差別化 */
    [data-testid="stChatMessage"] {
        background-color: #121212 !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
    }
    /* AI(Assistant)の吹き出しだけ左側をゴールドに光らせる */
    [data-testid="stChatMessage"]:has(path[d*="M12 21.35"]) { 
        border-left: 5px solid #FFD700 !important;
    }

    /* サイドバー：黒地に金の境界線 */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 2px solid #FFD700 !important;
    }

    /* チャット入力欄：操作性を考慮した白背景 */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border-radius: 30px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
    }

    /* 見出しをゴールドに強調 */
    h1, h2, h3 {
        color: #FFD700 !important;
        text-shadow: 0px 0px 12px rgba(255, 215, 0, 0.6);
    }

    /* ボタンのデザイン */
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px #FFD700;
    }

    /* 表（データフレーム）の背景調整 */
    .stDataFrame {
        background-color: #111 !important;
        border: 1px solid #444 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. 起動演出 (Healthy Go! 3秒Ver.)
# ==========================================
if 'initialized' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
            @keyframes thunder_flash {
                0%, 15% { background-color: #ffffff; }
                5%, 20% { background-color: transparent; }
            }
            .stApp { animation: thunder_flash 1.2s ease-out; }
            </style>
            """, unsafe_allow_html=True)
        st.markdown("<br><br><br><br><h1 style='text-align: center; color: #FFD700; font-size: 120px; text-shadow: 0 0 60px #FFA500;'>⚡ Healthy Go! ⚡</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px; letter-spacing: 5px;'>BY GEMINI AI 1.5 FLASH</p>", unsafe_allow_html=True)
        st.snow()
        time.sleep(3.0)
    placeholder.empty()
    st.session_state['initialized'] = True
# ==========================================
# 4. サイドバー (メニュー & BGM)
# ==========================================
st.sidebar.title("🔥 HealthyAI ⚡")
app_mode = st.sidebar.radio("メニュー選択：", ["AIトレーナー", "筋トレメニュー", "タイマー", "メトロノーム", "食品カロリー表"])

st.sidebar.markdown("---")
st.sidebar.subheader("🎵 Training BGM")

# 音楽フォルダの自動チェックと作成
music_folder = "music"
if not os.path.exists(music_folder):
    os.makedirs(music_folder)

# フォルダ内の音声ファイルを取得
music_files = [f for f in os.listdir(music_folder) if f.endswith((".mp3", ".wav", ".m4a"))]

if music_files:
    # 好きな曲を選べる
    selected_bgm = st.sidebar.selectbox("テンションを上げろ：", music_files)
    
    # ループ再生のオンオフ（筋トレ中ずっと流すため）
    is_loop = st.sidebar.checkbox("ループ再生", value=True)
    
    # 再生プレイヤー
    st.sidebar.audio(os.path.join(music_folder, selected_bgm), loop=is_loop)
    st.sidebar.caption(f"Playing: {selected_bgm}")
else:
    # 曲がない場合のガイドと、発表用サンプル
    st.sidebar.info("musicフォルダにmp3を入れると自分の曲を流せるぜ！")
    st.sidebar.caption("サンプルBGM（Energy Boost）")
    # 著作権フリーの筋トレに合うサンプル音源（Bensoundなど）
    st.sidebar.audio("https://www.bensound.com/bensound-music/bensound-energy.mp3", loop=True)

st.sidebar.markdown("---")
st.sidebar.write("⚡ **Tips:**")
st.sidebar.caption("音楽はドーパミンを出し、疲労感を感じにくくさせる。自分の『勝負曲』をセットしよう！")
# ==========================================
# 5. メイン機能
# ==========================================

# --- AIトレーナー ---
if app_mode == "AIトレーナー":
    st.header("🤖 Healthy AI")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "よぉ！準備はいいか？お前の限界をぶち破りに来たぜ！💪"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("お前の悩みをぶつけろ！"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                res = model.generate_content(f"あなたは超熱血トレーナーです。ポジティブに答えて：{prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
            except Exception as e:
                st.error(f"エラー発生：{e}")
# --- 筋トレメニュー (AIカスタム＆動画連携版) ---
elif app_mode == "筋トレメニュー":
    st.header("🏋️ インテリジェント・ワークアウト")
    
    # ユーザーへのヒアリング
    st.subheader("今日のプランをAIと作る")
    col_a, col_b = st.columns(2)
    target = col_a.selectbox("鍛えたい部位は？", ["全身", "お腹周り", "足・お尻", "腕・胸", "背中"])
    intensity = col_b.select_slider("追い込み度", options=["ゆったり", "普通", "限界まで"])

    if st.button("✨ AIに専用メニューを作らせる", use_container_width=True):
        with st.spinner("AIトレーナーがメニューを考案中..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"部位：{target}、強度：{intensity}。この条件で、自宅で道具なしでできる筋トレメニューを3種目提案して。種目名、回数、コツを熱く、短く教えて。"
                res = model.generate_content(prompt)
                
                # 結果表示エリアをカード風に
                st.markdown(f"""
                <div style="background-color: #1A1A1A; padding: 20px; border-radius: 15px; border-left: 5px solid #FFD700;">
                    <h3 style="color: #FFD700;">🔥 本日の特製メニュー：{target}</h3>
                    <p style="color: white; white-space: pre-wrap;">{res.text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 部位に合わせた参考動画を自動表示
                st.subheader("📹 正しいフォームを確認しよう")
                video_urls = {
                    "全身": "https://www.youtube.com/watch?v=Xz2idpL-yis",
                    "お腹周り": "https://www.youtube.com/watch?v=p79q148y_20",
                    "足・お尻": "https://www.youtube.com/watch?v=3nIdK7I17eA",
                    "腕・胸": "https://www.youtube.com/watch?v=vV_X8-mDkEw",
                    "背中": "https://www.youtube.com/watch?v=mY255hI3b0I"
                }
                st.video(video_urls[target])
                
            except Exception as e:
                st.error(f"AIがサボっています: {e}")

    st.markdown("---")
    st.subheader("🏆 殿堂入り定番メニュー")
    # ここに以前の固定メニューも残しておくと親切！
    with st.expander("もっと見る"):
        st.write("- バーピージャンプ (20回)")
        st.write("- ワイドスクワット (30回)")
# --- タイマー (停止・自動リセット機能付き) ---
elif app_mode == "タイマー":
    st.header("⏱️ インターバル・タイマー")
    
    # 状態管理（タイマーが動いているかどうか）
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False

    c1, c2 = st.columns(2)
    m = c1.number_input("分", 0, 60, 0, key="timer_m")
    s = c2.number_input("秒", 0, 59, 30, key="timer_s")
    
    # ボタン配置
    col_start, col_stop = st.columns(2)
    start_btn = col_start.button("🚀 START", use_container_width=True)
    stop_btn = col_stop.button("🛑 STOP", use_container_width=True)

    # 表示エリア
    timer_display = st.empty()

    if start_btn:
        st.session_state.timer_running = True
        total_seconds = m * 60 + s
        
        while total_seconds >= 0 and st.session_state.timer_running:
            # 停止ボタンが押されたかチェック（Streamlitの仕様上、再描画で判定）
            if stop_btn:
                st.session_state.timer_running = False
                break
                
            # 残り時間を表示
            mins, secs = divmod(total_seconds, 60)
            timer_display.markdown(f"<h1 style='text-align: center; font-size: 250px; color: #FFD700;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            
            if total_seconds == 0:
                st.balloons()
                time.sleep(2) # 0秒を少し見せてからリセット
                st.session_state.timer_running = False
                st.rerun() # 画面をリセットして初期状態に戻す
                
            time.sleep(1)
            total_seconds -= 1

    elif stop_btn:
        st.session_state.timer_running = False
        timer_display.markdown("<h1 style='text-align: center; color: #FF4B4B;'>STOPPED</h1>", unsafe_allow_html=True)
        time.sleep(1)
        st.rerun()

    else:
        # 待機画面
        timer_display.markdown(f"<h1 style='text-align: center; font-size: 250px; color: #333333;'>{m:02d}:{s:02d}</h1>", unsafe_allow_html=True)
# --- メトロノーム (視認性改善・究極版) ---
elif app_mode == "メトロノーム":
    st.header("🥁 筋トレ・リズムメトロノーム")
    st.write("リズムが乱れれば、筋肉への負荷も逃げる。一定を保て！")

    col1, col2 = st.columns(2)
    bpm = col1.slider("BPM (テンポ)", 30, 120, 60)
    total_beats = col2.number_input("合計カウント数", 4, 100, 32)
    
    rhythm_type = st.selectbox("トレーニングリズムを選択：", [
        "等間隔 (1-2-3-4)", 
        "ネガティブ重視 (1秒で上げ、3秒で下げる)", 
        "スロートレーニング (4秒かけて上げ下げ)"
    ])

    if st.button("🚀 リズムに合わせてスタート！", use_container_width=True):
        t_display = st.empty()
        
        # 音声読み上げJS
        st.components.v1.html("""
        <script>
        function speak(text) {
            window.speechSynthesis.cancel(); // 前の音声を止める
            const uttr = new SpeechSynthesisUtterance(text);
            uttr.lang = 'en-US';
            uttr.rate = 1.2; // 少し早口でキレを出す
            window.speechSynthesis.speak(uttr);
        }
        </script>
        """, height=0)

        for i in range(total_beats):
            count = (i % 4) + 1
            
            # デザイン設定
            if rhythm_type == "ネガティブ重視 (1秒で上げ、3秒で下げる)":
                if count == 1:
                    bg_color = "#FFD700" # ゴールド（一番目立つ）
                    text_color = "#000000" # 文字を黒にして視認性確保！
                    label = "UP!! (上げる)"
                    voice = "Up"
                else:
                    bg_color = "#1E90FF" # 青（耐える時）
                    text_color = "#FFFFFF" # 青背景には白文字
                    label = f"DOWN... ({count-1})"
                    voice = str(count-1)
            else:
                # デフォルト
                bg_color = "#FFD700" if count == 1 else "#333333"
                text_color = "#000000" if count == 1 else "#FFFFFF"
                label = "BEAT!" if count == 1 else "HOLD"
                voice = str(count)

            # 視覚的表示（文字色をtext_colorで動的に変更）
            t_display.markdown(f"""
                <div style='
                    text-align: center; 
                    background-color: {bg_color}; 
                    padding: 60px; 
                    border-radius: 30px; 
                    border: 5px solid {bg_color};
                    box-shadow: 0px 0px 20px {bg_color if count==1 else "transparent"};
                    transition: 0.1s;
                '>
                    <h1 style='font-size: 180px; color: {text_color} !important; margin: 0; line-height: 1;'>{count}</h1>
                    <h2 style='color: {text_color} !important; font-weight: bold; margin-top: 10px;'>{label}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # 音声
            st.components.v1.html(f"<script>speak('{voice}');</script>", height=0)
            
            time.sleep(60/bpm)
        
        st.success("セット完了！ナイス追い込み！")
# --- 食品カロリー表 (全95行対応・検索機能付き) ---
elif app_mode == "食品カロリー表":
    st.header("🍎 食品栄養データベース")
    if os.path.exists('food_data.csv'):
        df = pd.read_csv('food_data.csv')
        
        # 🔍 検索バー
        search_query = st.text_input("🔍 料理名で検索（例：ハンバーグ、納豆）", "")
        
        if search_query:
            filtered_df = df[df['料理名'].str.contains(search_query, na=False)]
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("food_data.csv を作成して保存してください。")