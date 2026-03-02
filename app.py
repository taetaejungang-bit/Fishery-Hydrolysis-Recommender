import streamlit as st
import pandas as pd
import numpy as np

# ==============================
# 1. 제목
# ==============================
st.set_page_config(page_title="FEPOS-AI", layout="wide")

st.markdown("## 🐟 Fishery Enzymatic Process Optimization System (FEPOS-AI)")
st.markdown("Literature-based Enzymatic Hydrolysis Recommendation Platform")
st.markdown("---")

# ==============================
# 2. 데이터 로드 (Cloud 전용 방식)
# ==============================
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Fishery_Hydrolysis_Extracted_FINAL.xlsx")
        return df
    except Exception as e:
        st.error("❌ Data file not found. Please check repository file structure.")
        st.stop()

df = load_data()

# 품질 점수 필터
df = df[df["quality_score"] >= 6].copy()

# ==============================
# 3. 사이드바 선택
# ==============================
st.sidebar.header("Select Input Conditions")

species_list = sorted(df["species"].dropna().unique())
species = st.sidebar.selectbox("Select Species", species_list)

part_list = sorted(df[df["species"] == species]["raw_part"].dropna().unique())
part = st.sidebar.selectbox("Select Raw Part", part_list)

# ==============================
# 4. 추천 알고리즘 (문헌 빈도 기반)
# ==============================
st.subheader("🔎 Recommended Hydrolysis Condition")

if st.button("Recommend Condition"):

    sub = df[(df["species"] == species) & (df["raw_part"] == part)]

    if len(sub) == 0:
        st.warning("⚠ Not enough data available for this combination.")
    else:
        # 1️⃣ 가장 많이 사용된 효소
        enz_prob = sub["enzyme"].value_counts(normalize=True)
        best_enzyme = enz_prob.index[0]
        prob = enz_prob.iloc[0]

        sub2 = sub[sub["enzyme"] == best_enzyme]

        # 2️⃣ 통계값 계산
        temp_mean = sub2["temp_C"].mean()
        temp_sd = sub2["temp_C"].std()
        time_median = sub2["time_min"].median()
        ph_median = sub2["pH"].median()

        # ==============================
        # 5. 결과 출력
        # ==============================
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Recommended Enzyme", best_enzyme)
            st.metric("Literature Probability", f"{round(prob*100,1)} %")

        with col2:
            st.metric("Temperature (°C)", f"{round(temp_mean,1)} ± {round(temp_sd,1)}")
            st.metric("Time (min)", f"{round(time_median,1)}")
            st.metric("pH", f"{round(ph_median,2)}")

        st.markdown("---")

        st.subheader("📊 Enzyme Distribution")
        st.bar_chart(enz_prob)

        st.markdown("---")

        st.subheader("📈 Data Summary")
        st.write(f"Total Literature Cases: **{len(sub)}**")
        st.write(f"Unique Enzymes Reported: **{sub['enzyme'].nunique()}**")

# ==============================
# 6. Footer
# ==============================
st.markdown("---")
st.caption("Developed for Mid-term Research Evaluation | FEPOS-AI Platform")