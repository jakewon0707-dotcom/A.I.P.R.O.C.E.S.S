import streamlit as st
import speech_recognition as sr
import difflib
import os
import csv
from datetime import datetime
import pandas as pd

# Basic Setup
st.set_page_config(page_title="Beat the Teacher! 🏆", layout="centered", initial_sidebar_state="expanded")

# --- CSS / Aesthetics ---
st.markdown("""
<style>
    .big-font {
        font-size:36px !important;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        background-color: #F0F9FF;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .metric-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'teacher_target_sentence' not in st.session_state:
    st.session_state.teacher_target_sentence = ""

# --- Constants ---
LESSON_1_COUNTRIES = ["Korea", "UK", "USA", "Canada", "Australia"]
RESULTS_FILE = "results.csv"

# --- Helper Functions ---
def clean_text(text):
    import string
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator).lower().strip()

def calculate_similarity(target, spoken):
    target_clean = clean_text(target)
    spoken_clean = clean_text(spoken)
    
    matcher = difflib.SequenceMatcher(None, target_clean, spoken_clean)
    score = int(matcher.ratio() * 100)
    return score

def stt_from_audio(audio_data):
    recognizer = sr.Recognizer()
    try:
        # Save audio byte data to a temporary file
        temp_wav = "temp_student_audio.wav"
        with open(temp_wav, "wb") as f:
            f.write(audio_data.getbuffer())
        
        # Read the audio file
        with sr.AudioFile(temp_wav) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="en-US")
            return text
    except sr.UnknownValueError:
        return "⚠️ 음성을 인식할 수 없어요! 다시 크게 말해주세요."
    except sr.RequestError as e:
        return f"⚠️ 구글 STT 서버에 연결할 수 없어요: {e}"
    except Exception as e:
        return f"⚠️ 오류 발생: {e}"

def save_result(student_name, target_sentence, spoken_text, score):
    file_exists = os.path.isfile(RESULTS_FILE)
    with open(RESULTS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Student Name", "Target Sentence", "Spoken Text", "Score"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), student_name, target_sentence, spoken_text, score])

# --- UI Header ---
st.title("🗣️ A.I. P.R.O.C.E.S.S.")
st.subheader("Beat the Teacher! (5th Grade Edition) 🏆")

# --- Tabs ---
tab_teacher, tab_student, tab_data = st.tabs(["👨‍🏫 선생님 모드 (Teacher)", "👦👧 학생 모드 (Student)", "📊 연구 데이터 (Data)"])

with tab_teacher:
    st.header("✨ Teacher's Gold Standard")
    st.write("학생들이 도전할 기준 문장을 설정하는 곳입니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("📖 **[5학년 1단원] 국가 이름 선택**")
        country_choice = st.selectbox("Where are you from?", LESSON_1_COUNTRIES)
        preset_sentence = f"I'm from {country_choice}."
        if st.button("목록에서 이 문장 선택"):
            st.session_state.teacher_target_sentence = preset_sentence
            st.success(f"기준 문장이 설정되었습니다: '{preset_sentence}'")
            
    with col2:
        st.write("✏️ **직접 입력하기**")
        custom_sentence = st.text_input("원하는 문장을 입력하세요:", placeholder="e.g. It's beautiful.")
        if st.button("직접 입력한 문장 선택"):
            if custom_sentence.strip():
                st.session_state.teacher_target_sentence = custom_sentence.strip()
                st.success(f"기준 문장이 설정되었습니다: '{custom_sentence}'")
            else:
                st.warning("문장을 먼저 입력해주세요!")
                
    st.markdown("---")
    if st.session_state.teacher_target_sentence:
        st.info(f"📍 **현재 설정된 도전 문장:** {st.session_state.teacher_target_sentence}")
    else:
        st.warning("❗️ 아직 기준 문장이 설정되지 않았습니다.")

with tab_student:
    st.header("🎮 Student Challenge")
    
    if not st.session_state.teacher_target_sentence:
        st.error("아직 도전할 문장이 없어요! 선생님께 문장을 설정해 달라고 요청하세요. 👨‍🏫")
    else:
        st.markdown('이 문장을 크고 또렷하게 읽어보세요! 👇')
        st.markdown(f'<div class="big-font">"{st.session_state.teacher_target_sentence}"</div>', unsafe_allow_html=True)
        
        student_name = st.text_input("🙋‍♀️🙋‍♂️ 이름이나 번호를 입력하세요:", max_chars=20)
        
        if student_name:
            st.write("🎙️ **마이크 버튼을 누르고 녹음을 시작하세요!**")
            audio_value = st.audio_input("Record your voice! (목소리 녹음)")
            
            if audio_value:
                with st.spinner("AI가 발음을 듣고 있어요... 🤖"):
                    spoken_text = stt_from_audio(audio_value)
                    
                st.markdown(f"**🗣️ 내가 한 말:** {spoken_text}")
                
                if "⚠️" not in spoken_text:
                    score = calculate_similarity(st.session_state.teacher_target_sentence, spoken_text)
                    
                    st.markdown("---")
                    col_score, _ = st.columns([1, 1])
                    with col_score:
                        st.metric(label="내 점수 (Score)", value=f"{score} / 100")
                    
                    # 피드백 로직
                    if score >= 90:
                        st.balloons()
                        st.success("🎉 우와! 원어민 같아요! 🏆 You beat the teacher!")
                        st.write("🎧 내 목소리를 다시 들어보세요:")
                        st.audio(audio_value, format="audio/wav")
                    elif score >= 70:
                        st.info("👍 Good job! 거~의 비슷하게 따라했어요! You're getting there!")
                    else:
                        st.warning("💪 Keep trying! You can do it! 포기하지 말고 다시 한 번 해볼까요?")
                        
                    # Easy CER Model (추가 보너스!)
                    original_words = len(clean_text(st.session_state.teacher_target_sentence).split())
                    spoken_words = len(clean_text(spoken_text).split())
                    
                    # 정답을 포함하고 있고, 덧붙여서 말했다면 보너스!
                    if spoken_words > original_words and score >= 60:
                        # 정답 문장이 내 말 안에 포함되어 있는지 확인
                        if clean_text(st.session_state.teacher_target_sentence) in clean_text(spoken_text):
                            st.success("🌟 Oho! 이유(Reason)나 추가 내용을 잘 말했군요! +10점 보너스! (Easy CER Model)")
                            score += 10
                            
                    # 자동 저장
                    save_result(student_name, st.session_state.teacher_target_sentence, spoken_text, min(score, 100))
                    st.toast("저장되었습니다! 💾")
                    
        else:
            st.info("시작하려면 이름을 먼저 입력해야 해요! ✨")

with tab_data:
    st.header("📊 연구용 누적 데이터 (Admin Only)")
    st.write("학생들의 스피킹 기록을 확인할 수 있습니다.")
    
    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        st.dataframe(df, use_container_width=True)
        
        # CSV 다운로드 버튼
        with open(RESULTS_FILE, "rb") as file:
            st.download_button(
                label="📥 CSV 데이터 다운로드",
                data=file,
                file_name="student_speaking_results.csv",
                mime="text/csv",
            )
    else:
        st.write("아직 기록된 데이터가 없습니다.")
