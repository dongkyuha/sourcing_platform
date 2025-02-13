import streamlit as st
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# 데이터 로드 함수
def load_data():
    base_path = "C:/Users/dkyuha/OneDrive - Smilegate/하동규/글로벌 인재 플랫폼/14. Chrome Extension/Unified_v2"
    files = {
        "experience": "Experience.xlsx",
        "education": "Education.xlsx",
        "profile": "Profile.xlsx",
        "skill": "Skill.xlsx",
        "awards": "Awards.xlsx",
        "certifications": "Certifications.xlsx",
        "languages": "Languages.xlsx",
        "accomplishment": "Accomplishment.xlsx",
        "recommendation": "Recommendation.xlsx",
    }
    
    data = {}
    for key, file in files.items():
        file_path = os.path.join(base_path, file)
        try:
            data[key] = pd.read_excel(file_path)
        except Exception as e:
            st.error(f"{file} 파일을 불러오는 중 오류 발생: {e}")
            data[key] = pd.DataFrame()  # 오류 시 빈 데이터프레임 생성
    
    return data

# 데이터 로드
data = load_data()

experience = data["experience"]
education = data["education"]
profile = data["profile"]
skill = data["skill"]
awards = data["awards"]
certifications = data["certifications"]
languages = data["languages"]
accomplishment = data["accomplishment"]
recommendation = data["recommendation"]

# Streamlit 페이지 설정
st.set_page_config(page_title="인재 데이터 플랫폼", layout="wide")
st.markdown("""
    <style>

    .sidebar .sidebar-content, .stSidebar {
        background-color: #FFCC99 !important;
        padding: 10px;
    }
    .stButton > button {
        background-color: #FF9966 !important;
        color: white !important;
        border-radius: 5px !important;
    }

    /* 프로필 박스 스타일 */
    .profile-container {
        background-color: #FFCC99 !important;
        padding: 4px !important;
        border-radius: 5px !important;
        margin-bottom: 2px !important;
    }

    </style>
""", unsafe_allow_html=True)
st.title("🌍 잠재후보자 프로필 Overview")



# 프로필 데이터 결합
def merge_data(profile, experience, education, skill, awards, certifications, languages, accomplishment, recommendation):
    profile["Name"] = profile["Name"].fillna(profile["MaskedName"])
    profile["Public_URL"] = profile["Public_URL"].fillna("")
    profile["Source"] = profile["Public_URL"].apply(lambda x: "LinkedIn" if "linkedin" in str(x).lower() else "Remember")


    def group_data(df, id_col, cols, name):
        """ 데이터 그룹핑 함수 """
        available_cols = [col for col in cols if col in df.columns]
        if available_cols:
            return df.groupby(id_col)[available_cols].apply(lambda x: x.to_dict(orient="records")).reset_index(name=name)
        return pd.DataFrame(columns=[id_col, name])

    experience_grouped = group_data(experience, "ID", ["CompanyName", "Position", "Duration"], "Experience")
    education_grouped = group_data(education, "ID", ["SchoolName", "Major", "Degree", "Education_Date"], "Education")
    skill_grouped = group_data(skill, "ID", ["Skill"], "Skill")
    awards_grouped = group_data(awards, "ID", ["AwardName", "Year"], "Awards")
    certifications_grouped = group_data(certifications, "ID", ["Certification", "Institution", "Year"], "Certifications")
    languages_grouped = group_data(languages, "ID", ["Language"], "Languages")
    accomplishment_grouped = group_data(accomplishment, "ID", ["Accomplishment_Section", "Accomplishment_Title", "Accomplishment_Period"], "Accomplishment")
    recommendation_grouped = group_data(recommendation, "ID", ["Recommender", "Content"], "Recommendation")

    profile_merged = profile.merge(experience_grouped, on="ID", how="left")\
                            .merge(education_grouped, on="ID", how="left")\
                            .merge(skill_grouped, on="ID", how="left")\
                            .merge(awards_grouped, on="ID", how="left")\
                            .merge(certifications_grouped, on="ID", how="left")\
                            .merge(languages_grouped, on="ID", how="left")\
                            .merge(accomplishment_grouped, on="ID", how="left")\
                            .merge(recommendation_grouped, on="ID", how="left")

    return profile_merged

profile_data = merge_data(profile, experience, education, skill, awards, certifications, languages, accomplishment, recommendation)

# 필터 적용
st.sidebar.header("검색 필터")

# 이름 필터 추가
name_filter = st.sidebar.text_input("이름 필터", "")

if name_filter:
    profile_data = profile_data[profile_data["Name"].str.contains(name_filter, case=False, na=False)]

experience_filter = st.sidebar.text_input("경력 필터", "")
education_filter = st.sidebar.text_input("학력 필터", "")
skill_filter = st.sidebar.text_input("스킬 필터", "")
# Summary 또는 Introduction 기반 필터 추가
summary_intro_filter = st.sidebar.text_input("Summary / Introduction 필터", "")

if experience_filter:
    profile_data = profile_data[profile_data["Experience"].apply(lambda x: any(experience_filter in str(item) for item in x) if isinstance(x, list) else False)]
if education_filter:
    profile_data = profile_data[profile_data["Education"].apply(lambda x: any(education_filter in str(item) for item in x) if isinstance(x, list) else False)]
if skill_filter:
    profile_data = profile_data[profile_data["Skill"].apply(lambda x: any(skill_filter in str(item) for item in x) if isinstance(x, list) else False)]

if summary_intro_filter:
    if "Summary" in profile_data.columns and "Introduction" in profile_data.columns:
        profile_data = profile_data[
            profile_data["Summary"].apply(lambda x: summary_intro_filter.lower() in str(x).lower() if pd.notna(x) else False) |
            profile_data["Introduction"].apply(lambda x: summary_intro_filter.lower() in str(x).lower() if pd.notna(x) else False)
        ]

# 페이지네이션 설정
items_per_page = 5
page_number = st.sidebar.number_input("페이지 번호", min_value=1, max_value=(len(profile_data) // items_per_page) + 1, step=1)
start_idx = (page_number - 1) * items_per_page
end_idx = start_idx + items_per_page
paginated_data = profile_data.iloc[start_idx:end_idx]

# 프로필 출력
st.write(f"### 총 {len(profile_data)}명의 인재 데이터 (페이지 {page_number})")

# 📌 Expander 위에 index, row in paginated_data.iterrows():
for index, row in paginated_data.iterrows():
    with st.container():
        

        st.markdown(
            """
            <div style='background-color: #FFF3E0; padding: 5px; border-radius: 5px;'>
            """,
            unsafe_allow_html=True
        )


        
        col1, col2, col3 = st.columns([3, 2.5, 9])
        col1, col2, col3, col4 = st.columns([3, 3, 7, 2])
        
        with col1:
            st.write(f"### {row['Name']}")
            
        with col2:
            st.markdown(
                """
                <p style="font-weight: bold; font-size:16px; word-spacing: 10px;">
                    🎓 학력   /  전공   /   학위
                </p>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                """
                <p style="font-weight: bold; font-size:16px; word-spacing: 10px;">
                    💼 기업   /   직책   /   경력
                </p>
                """,
                unsafe_allow_html=True
            )

        with col4:
            detail_page_url = f"/details?name={row['Name']}"
            if st.button(f"🔍 세부정보", key=f"detail_{row['ID']}"):
                st.session_state["selected_profile"] = row.to_dict()
                st.switch_page("pages/details.py")
                st.rerun()

        
        education_df = pd.DataFrame(row["Education"]) if isinstance(row["Education"], list) else pd.DataFrame()
        experience_df = pd.DataFrame(row["Experience"]) if isinstance(row["Experience"], list) else pd.DataFrame()
        
        if not education_df.empty or not experience_df.empty:
            max_length = min(3, max(len(education_df), len(experience_df)))
            for i in range(max_length):
                with st.container():
                    col1, col2, col3 = st.columns([3, 3, 10])
                    education = education_df.iloc[i].dropna().to_dict() if i < len(education_df) else {}
                    experience = experience_df.iloc[i].dropna().to_dict() if i < len(experience_df) else {}
                    
                    with col1:
                        st.write(" ")  # 빈 공간 유지
                    with col2:
                        if education:
                            st.write(f"\n- {education.get('SchoolName', '')}   /   {education.get('Major', '')}  /   {education.get('Degree', '')}")
                    with col3:
                        if experience:
                            st.write(f"\n- {experience.get('CompanyName', '')}   /   {experience.get('Position', '')}   /   {experience.get('Duration', '')}")

      
        # 추가 정보 (비어 있는 경우 expander 자체를 숨김)
        extra_info_sections = {
            "📌 경력": row["Experience"],
            "🎓 학력": row["Education"],
            "💡 보유 스킬": row["Skill"],
            "🏆 수상 경력": row["Awards"],
            "📜 자격증": row["Certifications"],
            "🌍 언어 능력": row["Languages"],
            "⭐ 주요 업적": row["Accomplishment"],
            "📝 추천서": row["Recommendation"],
        }
        
        valid_sections = {title: data for title, data in extra_info_sections.items() if isinstance(data, list) and len(data) > 0}
        
        st.write("")

st.markdown(
    """
    <div style='background-color: #FFF3E0; padding: 5px; border-radius: 5px;'>
    """,
    unsafe_allow_html=True
)

