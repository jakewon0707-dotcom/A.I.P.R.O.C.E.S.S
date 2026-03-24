import streamlit as st
import speech_recognition as sr
import difflib
import os
import csv
from datetime import datetime
import pandas as pd
import streamlit.components.v1 as components

# Basic Setup
st.set_page_config(
    page_title="A.I. P.R.O.C.E.S.S. Tutor", 
    page_icon="🌟", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CSS / Aesthetics ---
st.markdown("""
<style>
    /* Google Fonts - Jua for cute thick style, Nunito as fallback */
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Nunito:wght@400;700;900&display=swap');
    
    html, body, [class*="css"], p, div, span, label {
        font-family: 'Jua', 'Nunito', sans-serif !important;
        font-size: 18px;
    }
    
    /* 1. Pastel Background for the whole app */
    .stApp {
        background: linear-gradient(135deg, #FFF0F5 0%, #E0F7FA 100%);
    }

    /* 2. Game-style Buttons */
    .stButton > button {
        background-color: #FF6F61 !important;
        color: white !important;
        font-family: 'Jua', sans-serif !important;
        font-size: 22px !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 24px !important;
        box-shadow: 0 6px 0 #D85A4E, 0 10px 15px rgba(0,0,0,0.1) !important;
        transition: all 0.1s ease !important;
        height: auto !important;
        margin-top: 10px;
    }
    .stButton > button:active {
        box-shadow: 0 2px 0 #D85A4E, 0 4px 6px rgba(0,0,0,0.1) !important;
        transform: translateY(4px) !important;
    }

    /* 3. Input fields rounded */
    .stTextInput > div > div > input {
        border-radius: 20px !important;
        border: 3px solid #7DD3FC !important;
        padding: 10px 15px !important;
        font-size: 18px !important;
        font-family: 'Jua', sans-serif !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 20px !important;
        border: 3px solid #7DD3FC !important;
        font-family: 'Jua', sans-serif !important;
    }

    .big-font {
        font-family: 'Jua', sans-serif !important;
        font-size: 38px !important;
        font-weight: 800;
        color: #0284C7; /* Sky Blue */
        text-align: center;
        background-color: #FFFFFF;
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 20px;
        border: 4px dashed #7DD3FC;
        box-shadow: 0 8px 15px rgba(0,0,0,0.05);
    }
    
    .perfect-score {
        font-family: 'Jua', sans-serif !important;
        font-size: 42px;
        font-weight: 900;
        color: #10B981; /* Mint Green */
        text-align: center;
        margin-top: 15px;
        text-shadow: 2px 2px 0px #A7F3D0;
        animation: bounce 1s infinite alternate;
    }
    
    @keyframes bounce {
        from { transform: translateY(0); }
        to { transform: translateY(-15px); }
    }
    
    .main-title {
        font-family: 'Jua', sans-serif !important;
        color: #0284C7;
        font-weight: 900;
        font-size: 55px;
        margin-bottom: 5px;
        text-align: center;
        text-shadow: 2px 2px 0px #BAE6FD;
    }
    
    .sub-title {
        font-family: 'Jua', sans-serif !important;
        color: #FF6F61; /* Coral Pink */
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 40px;
        text-align: center;
    }
    
    .col-header {
        font-family: 'Jua', sans-serif !important;
        color: #1E3A8A;
        font-weight: 800;
        font-size: 28px;
        margin-bottom: 15px;
        text-align: center;
        background-color: #E0F2FE;
        padding: 10px;
        border-radius: 20px;
        border: 3px solid #BAE6FD;
    }
    
    .highlight-good {
        color: #10B981;
        font-weight: 800;
        background-color: #D1FAE5;
        padding: 4px 10px;
        border-radius: 12px;
        border: 2px solid #34D399;
    }
    
    .highlight-bad {
        color: #EF4444;
        font-weight: 800;
        background-color: #FEE2E2;
        padding: 4px 10px;
        border-radius: 12px;
        text-decoration: line-through;
        border: 2px solid #F87171;
    }
    
    .spoken-text-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        font-size: 22px;
        margin-top: 15px;
        border: 3px solid #0284C7;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        font-family: 'Jua', sans-serif !important;
    }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F9FF 100%);
        border-right: 3px solid #E2E8F0;
    }
    
    .sidebar-title {
        font-family: 'Jua', sans-serif !important;
        font-size: 26px;
        font-weight: 900;
        color: #0284C7;
        text-align: center;
        margin-bottom: 15px;
        background-color: #E0F2FE;
        padding: 15px;
        border-radius: 20px;
        border: 3px solid #7DD3FC;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'teacher_target_sentence' not in st.session_state:
    st.session_state.teacher_target_sentence = ""

# --- Constants ---
LESSON_1_COUNTRIES = ["the USA", "the UK", "Korea", "Canada", "Australia", "Vietnam"]
RESULTS_FILE = "results.csv"

# --- Helper Functions ---
def clean_text(text):
    import string
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator).lower().strip()

def calculate_similarity(target, spoken):
    target_clean = clean_text(target)
    spoken_clean = clean_text(spoken)
    
    if not target_clean or not spoken_clean:
        return 0
        
    matcher = difflib.SequenceMatcher(None, target_clean, spoken_clean)
    score = int(matcher.ratio() * 100)
    return score

def highlight_words(target, spoken):
    target_words = clean_text(target).split()
    spoken_words = clean_text(spoken).split()
    
    html_out = []
    spoken_set = set(spoken_words)
    
    for word in target_words:
        if word in spoken_set:
            html_out.append(f"<span class='highlight-good'>{word}</span>")
        else:
            html_out.append(f"<span class='highlight-bad'>{word}</span>")
            
    return " ".join(html_out)

def stt_from_audio(audio_data):
    recognizer = sr.Recognizer()
    try:
        temp_wav = "temp_student_audio.wav"
        with open(temp_wav, "wb") as f:
            f.write(audio_data.getbuffer())
        
        with sr.AudioFile(temp_wav) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="en-US")
            return text
    except sr.UnknownValueError:
        return "⚠️ 음성을 인식할 수 없어요! 다시 크게 말해주세요."
    except sr.RequestError as e:
        return f"⚠️ 구글 STT 서버 연결 오류: {e}"
    except Exception as e:
        return f"⚠️ 시스템 오류: {e}"

def save_result(student_name, target_sentence, spoken_text, score):
    file_exists = os.path.isfile(RESULTS_FILE)
    with open(RESULTS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Student Name", "Target Sentence", "Spoken Text", "Score"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), student_name, target_sentence, spoken_text, score])

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">👩‍🏫 VS 👧👦<br>Beat the Teacher!</div>', unsafe_allow_html=True)
    menu = st.radio(
        "메뉴를 선택하세요! 👇",
        ["🏠 Home", "🎤 Beat the Teacher!", "📊 My Data", "👩‍🏫 Teacher's Room"]
    )
    
    st.markdown("---")
    st.info("💡 **A.I. P.R.O.C.E.S.S. English Tutor**\n\n5학년 맞춤형 원어민 발음 정복 프로젝트! 선생님을 이겨라!")

# --- Main App Logic ---
if menu == "🏠 Home":
    st.markdown('<div class="main-title">🌟 A.I. P.R.O.C.E.S.S. English Tutor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">"선생님의 발음을 완벽하게 따라잡고 풍선을 터뜨려봐!"</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: center; font-size: 80px; margin: 10px 0; letter-spacing: 20px;">🎮🎙️🏆</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #E0F2FE; padding: 20px; border-radius: 15px; border-left: 5px solid #0284C7; margin-top: 20px;'>
        <h3 style='color: #0284C7; margin-top: 0;'>🚀 게임 규칙 (How to Play)</h3>
        <ul style='font-size: 18px; line-height: 1.8;'>
            <li>왼쪽 메뉴에서 <b>🎤 Beat the Teacher!</b> 를 선택하세요.</li>
            <li>선생님의 발음을 <b>주의 깊게</b> 듣습니다.</li>
            <li>마이크 버튼을 누르고 <b>자신 있게</b> 영어로 말해보세요!</li>
            <li>AI가 발음을 분석해 <b>풍선 보상</b>을 줄 거예요. 🎉</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("Are you ready? 준비가 끝났다면 왼쪽 메뉴를 클릭해 출발! 🏃‍♂️💨")

elif menu == "🎤 Beat the Teacher!":
    st.markdown('<div class="main-title">🌟 A.I. P.R.O.C.E.S.S. Tutor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">"선생님의 발음을 완벽하게 따라잡고 풍선을 터뜨려봐!"</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="col-header">👨‍🏫 [1단계] 선생님의 미션</div>', unsafe_allow_html=True)
        st.info("📝 미션 문장을 확인하고 원어민 발음을 들으세요.")
        
        country_choice = st.selectbox("🌍 [1단원] 출신 국가를 선택하세요:", LESSON_1_COUNTRIES)
        
        # Decide mission sentence
        if st.session_state.teacher_target_sentence:
            mission_sentence = st.session_state.teacher_target_sentence
            st.warning("👩‍🏫 선생님의 스페셜 미션입니다!")
        else:
            mission_sentence = f"I'm from {country_choice}."
            
        st.markdown(f'<div class="big-font">"{mission_sentence}"</div>', unsafe_allow_html=True)
        
        # HTML/JS Text-to-Speech Button
        tts_html = f"""
        <div style="display: flex; justify-content: center; margin-top: 10px;">
            <button onclick="let msg = new SpeechSynthesisUtterance('{mission_sentence.replace("'", "\\'")}'); msg.lang='en-US'; window.speechSynthesis.speak(msg);" 
            style="background-color: #0284C7; color: white; border: none; border-radius: 30px; padding: 15px 40px; font-size: 20px; font-weight: 900; cursor: pointer; box-shadow: 0 6px 15px rgba(2, 132, 199, 0.4); transition: transform 0.2s;">
            🎧 Listen to Teacher
            </button>
        </div>
        """
        st.components.v1.html(tts_html, height=100)
        
    with col2:
        st.markdown('<div class="col-header">🎙️ [2단계] 나의 도전!</div>', unsafe_allow_html=True)
        st.warning("🔥 Are you ready to beat the teacher? 마이크를 켜세요!")
        
        student_name = st.text_input("🙋‍♀️🙋‍♂️ 내 이름 (필수 입력):", placeholder="예: 5학년 1반 홍길동")
        
        if student_name:
            # st.audio_input button will be coral pink thanks to config.toml
            audio_value = st.audio_input("🎙️ 내 발음 녹음하기 (도전!)")
            
            if audio_value:
                with st.spinner("AI가 발음을 분석하고 있어요... 🤖"):
                    spoken_text = stt_from_audio(audio_value)
                
                if "⚠️" not in spoken_text:
                    score = calculate_similarity(mission_sentence, spoken_text)
                    
                    st.markdown("---")
                    st.markdown(f"<div class='spoken-text-box'>🗣️ <b>내가 한 말:</b> {spoken_text}</div>", unsafe_allow_html=True)
                    
                    # Highlight Evidence (CER Model - Evidence)
                    st.markdown("### 🔎 AI 분석 결과 (Evidence)")
                    highlighted_html = highlight_words(mission_sentence, spoken_text)
                    st.markdown(f"<div style='font-size: 22px; background: #fff; padding: 10px; border-radius: 8px; border: 1px solid #ddd;'>{highlighted_html}</div>", unsafe_allow_html=True)
                    st.caption("초록색은 정확한 단어, 빨간색 밑줄은 잘못 발음한 단어입니다.")
                    
                    # Similarity Score (CER Model - Reasoning / Real-time)
                    st.markdown("### 📊 선생님과의 유사도 (Similarity)")
                    st.progress(score / 100)
                    
                    # Feedback & Reward
                    if score >= 90:
                        st.markdown('<div class="perfect-score">Perfect! You beat the teacher! 🎉</div>', unsafe_allow_html=True)
                        st.balloons()
                    elif score >= 80:
                        st.success(f"**유사도 {score}%** - Excellent! 선생님이랑 거의 똑같아졌어! 👏")
                    else:
                        st.error(f"**유사도 {score}%** - Good try! 한 번만 더 선생님 목소리를 듣고 도전해 볼까? 😉")
                        
                    save_result(student_name, mission_sentence, spoken_text, score)
                else:
                    st.error(spoken_text)
        else:
            st.info("이름을 입력하면 🎙️ 녹음 버튼이 나타납니다! ✨")

elif menu == "📊 My Data":
    st.markdown('<div class="main-title">📊 My Data (학생 기록)</div>', unsafe_allow_html=True)
    st.write("### 누가누가 선생님을 이겼을까? 점수판을 확인해봐! 🏆")
    
    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        # Sort by score descending
        df_sorted = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
        
        st.dataframe(
            df_sorted.style.highlight_max(subset=['Score'], color='#D1FAE5'), 
            use_container_width=True,
            height=400
        )
        
        st.success(f"📚 지금 등록된 플레이는 총 {len(df)}건입니다!")
    else:
        st.info("아직 도전 기록이 없습니다. 첫 번째 도전자가 되어보세요! 🏃‍♂️")

elif menu == "👩‍🏫 Teacher's Room":
    st.markdown("""<div class="main-title">👩‍🏫 Teacher's Room</div>""", unsafe_allow_html=True)
    st.write("선생님 전용 관리 공간입니다. 직접 기준 문장을 설정하거나 전체 데이터를 관리하세요.")
    
    st.markdown("---")
    st.subheader("1. 🎯 특별 미션 문장 설정")
    custom_sentence = st.text_input("원하는 특별 문장을 입력하세요:", placeholder="e.g. It's a nice day.")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✨ 특별 미션 문장 적용하기", use_container_width=True):
            if custom_sentence.strip():
                st.session_state.teacher_target_sentence = custom_sentence.strip()
                st.success(f"적용 완료! 현재 미션: '{custom_sentence}'")
            else:
                st.warning("문장을 먼저 입력해주세요!")
    with col_btn2:
        if st.button("🔄 미션 초기화 (기본 국가 미션)", use_container_width=True):
            st.session_state.teacher_target_sentence = ""
            st.info("기본 미션 모드로 돌아갔습니다.")
            
    if st.session_state.teacher_target_sentence:
        st.info(f"**현재 설정된 특별 미션:** {st.session_state.teacher_target_sentence}")
        
    st.markdown("---")
    st.subheader("2. 📥 데이터베이스 관리 (results.csv)")
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "rb") as file:
            st.download_button(
                label="📥 전체 성적 CSV 파일 다운로드",
                data=file,
                file_name="student_speaking_results.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        if st.button("⚠️ 모든 데이터 초기화 (신중히 클릭!)"):
            os.remove(RESULTS_FILE)
            st.warning("데이터가 모두 삭제되었습니다. 페이지를 새로고침하세요.")
            st.rerun()
    else:
        st.write("기록된 데이터가 없습니다.")

