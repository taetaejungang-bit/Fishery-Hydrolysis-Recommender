import os
import streamlit as st
import pandas as pd
import numpy as np

# 1. 바탕화면 경로 자동 설정
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "Fishery_Hydrolysis_Extracted_FINAL.xlsx")

# 2. 데이터 로드
df = pd.read_excel(file_path)

# 품질 점수 6점 이상 필터링
df = df[df["quality_score"] >= 6].copy()

st.title("Fishery Enzymatic Hydrolysis Recommendation System")

# 종 선택
species_list = sorted(df["species"].unique())
species = st.selectbox("Select Species", species_list)

# 부위 선택
part_list = sorted(df[df["species"] == species]["raw_part"].unique())
part = st.selectbox("Select Raw Part", part_list)

if st.button("Recommend Condition"):

    sub = df[(df["species"] == species) & (df["raw_part"] == part)]

    if len(sub) == 0:
        st.warning("Not enough data available.")
    else:
        enz_prob = sub["enzyme"].value_counts(normalize=True)
        best_enzyme = enz_prob.index[0]
        prob = enz_prob.iloc[0]

        sub2 = sub[sub["enzyme"] == best_enzyme]

        temp_mean = sub2["temp_C"].mean()
        temp_sd = sub2["temp_C"].std()
        time_median = sub2["time_min"].median()
        ph_median = sub2["pH"].median()

        st.subheader("Recommended Condition")

        st.write(f"**Enzyme:** {best_enzyme}")
        st.write(f"**Probability:** {round(prob*100,1)}%")
        st.write(f"**Temperature:** {round(temp_mean,1)} ± {round(temp_sd,1)} °C")
        st.write(f"**Time:** {round(time_median,1)} min")
        st.write(f"**pH:** {round(ph_median,2)}")

        st.subheader("Enzyme Distribution")
        st.bar_chart(enz_prob)