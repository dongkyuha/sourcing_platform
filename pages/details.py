import streamlit as st
import pandas as pd

st.set_page_config(page_title="후보자 상세 정보", layout="wide")

st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #FFCC99;
    }
    .main-content {
        background-color: #FFDDC1;
        padding: 20px;
        border-radius: 10px;
    }
    .profile-box {
        padding: 15px;
        background-color: #FFCC99;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .name-box {
        font-size: 24px;
        font-weight: bold;
        text-decoration: underline;
        padding-bottom: 5px;
    }
    .skill-box {
        display: inline-block;
        padding: 5px 10px;
        margin: 3px;
        border-radius: 5px;
        background-color: #FFA07A;
        color: white;
    }
    .source-box {
        background-color: #FFE4B5;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
    }
    .sidebar .sidebar-content, .stSidebar {
        background-color: #FFCC99 !important;
        padding: 10px;
    }
    .stButton > button {
        background-color: #FE642E !important;
        color: white !important;
        border-radius: 5px !important;
    }
    .container-box {
        background-color: #FFE4B5;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ **세션 상태에서 후보자 데이터 가져오기**
if "selected_profile" in st.session_state:
    profile_info = st.session_state["selected_profile"]

    st.title(f"📌 {profile_info['Name']}님의 상세 프로필")

    # 🔹 **출처 및 Public URL**
    source = profile_info.get("Source", "정보 없음")
    public_url = profile_info["Public_URL"]

    source_html = f'''
    <div style="background-color: #FFF3E0; padding: 10px; border-radius: 10px; margin-bottom: 15px;">
        <b>{profile_info['Name']}님의 정보 URL - 출처:</b> <a href="{public_url}" target="_blank">{source}</a>
    </div>
    '''
    st.markdown(source_html, unsafe_allow_html=True)

    # 🔹 학력 정보
    if isinstance(profile_info.get("Education"), list) and profile_info["Education"]:
        st.markdown('<div style="background-color: #FBF5EF; padding: 15px; border-radius: 10px; margin-bottom: 15px;"><h3>🎓 학력 정보</h3></div>', unsafe_allow_html=True)
        education_df = pd.DataFrame(profile_info["Education"])
        st.dataframe(education_df, use_container_width=True)

    # 🔹 경력 정보
    if isinstance(profile_info.get("Experience"), list) and profile_info["Experience"]:
        st.markdown('<div style="background-color: #FBF5EF; padding: 15px; border-radius: 10px; margin-bottom: 15px;"><h3>💼 경력 정보</h3></div>', unsafe_allow_html=True)
        experience_df = pd.DataFrame(profile_info["Experience"])
        st.dataframe(experience_df, use_container_width=True)

    def safe_dataframe(data, column_name):
        """데이터를 안전하게 DataFrame으로 변환"""
        if isinstance(data, list) and data:
            if all(isinstance(item, dict) for item in data):  # 리스트 내부 요소가 딕셔너리일 경우
                df = pd.DataFrame(data)
            elif all(isinstance(item, str) for item in data):  # 리스트 내부 요소가 문자열일 경우
                df = pd.DataFrame({column_name: data})
            else:
                return None
            df.fillna("", inplace=True)
            if df.empty or df.shape[1] == 0:
                return None
            return df
        return None  

    # 🔹 자격증
    cert_df = safe_dataframe(profile_info.get("Certifications"), "자격증")
    if cert_df is not None:
        st.markdown('<div style="background-color: #FBF5EF; padding: 15px; border-radius: 10px; margin-bottom: 15px;"><h3>📜 자격증</h3></div>', unsafe_allow_html=True)
        st.dataframe(cert_df, use_container_width=True)

    # 🔹 언어 능력
    lang_df = safe_dataframe(profile_info.get("Languages"), "언어 능력")
    if lang_df is not None:
        st.markdown('<div style="background-color: #FBF5EF;  padding: 15px; border-radius: 10px; margin-bottom: 15px;"><h3>🌍 언어 능력</h3></div>', unsafe_allow_html=True)
        st.dataframe(lang_df, use_container_width=True)

    # 🔹 주요 업적
    acc_df = safe_dataframe(profile_info.get("Accomplishment"), "역량 스택")
    if acc_df is not None:
        st.markdown('<div style="background-color: #FBF5EF; padding: 15px; border-radius: 10px; margin-bottom: 15px;"><h3>🚀 역량 스택</h3></div>', unsafe_allow_html=True)
        st.dataframe(acc_df, use_container_width=True)

    # 🔹 보유 스킬 (각 스킬을 박스로 표시)
    if isinstance(profile_info.get("Skill"), list) and profile_info["Skill"]:
        st.markdown('<div style="background-color: #FBF5EF; padding: 15px; border-radius: 10px; margin-bottom: 15px;"><h3>💡 보유 스킬</h3></div>', unsafe_allow_html=True)
        skill_list = [skill.get("Skill", "") if isinstance(skill, dict) else skill for skill in profile_info["Skill"]]
        skill_html = " ".join([
            f'<span style="display:inline-block; padding:5px 10px; margin:3px; border-radius:5px; background-color:#FF7043; color:white;">{skill}</span>'
            for skill in skill_list
        ])
        st.markdown(f'<div style="display: flex; flex-wrap: wrap;">{skill_html}</div>', unsafe_allow_html=True)

    st.write("---")

    summary = profile_info.get("Summary")
    introduction = profile_info.get("Introduction")

    # 🔹 '#' 기호 제거 추가
    if isinstance(summary, str):
        summary = summary.replace("#", "")

    if isinstance(introduction, str):
        introduction = introduction.replace("#", "")
        introduction = introduction.replace("—— ", "")

    if pd.notna(summary) and summary:
        st.markdown('<div style="background-color: #FBF5EF; padding: 15px; border-radius: 10px; margin-bottom: 15px;"><h3>📝 Summary</h3></div>', unsafe_allow_html=True)
        st.markdown(summary)
    elif pd.notna(introduction) and introduction:
        st.markdown('<div style="background-color: #FBF5EF; padding: 15px; border-radius: 10px; margin-bottom: 15px;"><h3>🗣 Introduction</h3></div>', unsafe_allow_html=True)
        st.markdown(introduction)

    st.write("---")

    # 🔹 돌아가기 버튼
    if st.button("🔙 목록으로 돌아가기"):
        st.switch_page("Data_Platform_v7.py")

else:
    st.error("⚠️ 선택된 프로필이 없습니다. 목록에서 다시 선택하세요.")
