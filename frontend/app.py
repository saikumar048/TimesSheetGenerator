import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.5-flash")

# ------------------------------------------------------------
# 🧭 Page Setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI Timesheet Analyzer",
    page_icon="🧠",
    layout="centered"
)

# ------------------------------------------------------------
# 🎨 Custom CSS for professional UI
# ------------------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #eef2f3, #d9e4ec);
    font-family: 'Inter', sans-serif;
}
.main-container {
    background: white;
    padding: 2rem 3rem;
    border-radius: 15px;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.1);
}
.title {
    text-align: center;
    font-size: 2.5em;
    color: #004aad;
    font-weight: 800;
    margin-bottom: 0.5em;
}
.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.1em;
    margin-bottom: 2em;
}
.stButton>button {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    border: none;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.7em 1.2em;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.03);
}
.dataframe-container {
    background: #fafafa;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 🧾 Title Section
# ------------------------------------------------------------
st.markdown('<div class="title">AI Timesheet Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Aggregate your Calendar, Email, and Git data. Get insights and time-management advice using Gemini AI.</div>', unsafe_allow_html=True)
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ------------------------------------------------------------
# 📁 File Uploads
# ------------------------------------------------------------
st.subheader("📤 Upload Your Activity Files")

calendar_file = st.file_uploader("📅 Calendar File (.ics)", type=["ics"])
email_file = st.file_uploader("📧 Email File (.json)", type=["json"])
repo_path = st.text_input("💻 Git Repository Path (optional)")

# ------------------------------------------------------------
# 🚀 Process Button
# ------------------------------------------------------------
if st.button("Generate Timesheet Report"):
    with st.spinner("Processing your data... Please wait ⏳"):
        files, data = {}, {"repo_path": repo_path}
        if calendar_file: files["calendar_file"] = calendar_file
        if email_file: files["email_file"] = email_file

        try:
            res = requests.post("http://127.0.0.1:8000/process", files=files, data=data, timeout=90)
            if res.status_code != 200:
                st.error(f"❌ Error: {res.text}")
            else:
                result = res.json()
                df = pd.read_csv(result["csv_path"])

                st.success("✅ Timesheet generated successfully!")

                # ------------------------------------------------------------
                # 🧠 AI Summary Section
                # ------------------------------------------------------------
                st.markdown("### 🧠 AI Summary of Productivity")
                st.markdown(f"""
                <div style='background:#f0f7ff;border-left:6px solid #0072ff;padding:15px;border-radius:10px;margin-bottom:25px;'>
                {result["ai_summary"]}
                </div>
                """, unsafe_allow_html=True)

                # ------------------------------------------------------------
                # 📊 Visualization (medium-size charts)
                # ------------------------------------------------------------
                st.markdown("### 📈 Productivity Insights")

                fig_col1, fig_col2 = st.columns(2)

                with fig_col1:
                    st.markdown("#### Time Spent by Activity Type")
                    fig, ax = plt.subplots(figsize=(5, 3))
                    df.groupby("type")["hours"].sum().plot(kind="bar", color="#0072ff", ax=ax)
                    ax.set_ylabel("Hours")
                    ax.set_xlabel("Activity Type")
                    ax.set_title("")
                    plt.tight_layout()
                    st.pyplot(fig)

                with fig_col2:
                    st.markdown("#### Work Distribution")
                    fig2, ax2 = plt.subplots(figsize=(4, 3))
                    df.groupby("type")["hours"].sum().plot(
                        kind="pie",
                        autopct="%1.1f%%",
                        colors=["#0072ff", "#00c6ff", "#4ecdc4"],
                        startangle=90,
                        ax=ax2
                    )
                    ax2.set_ylabel("")
                    plt.tight_layout()
                    st.pyplot(fig2)

                # ------------------------------------------------------------
                # 📅 Display Data Table
                # ------------------------------------------------------------
                st.markdown("### 🗓️ Aggregated Timesheet Data")
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # ------------------------------------------------------------
                # 💬 Chat with Gemini
                # ------------------------------------------------------------
                st.divider()
                st.markdown("### 💬 Ask Gemini About Your Productivity")

                user_input = st.text_input("Ask Gemini something about your work pattern or time management:")
                if st.button("Ask Gemini"):
                    try:
                        model = genai.GenerativeModel(MODEL_NAME)
                        response = model.generate_content(
                            f"Based on this timesheet data:\n{df.to_string(index=False)}\n\n{user_input}"
                        )
                        st.markdown(f"""
                        <div style='background:#eef9f4;border-left:5px solid #00c6ff;padding:12px;border-radius:10px;'>
                        <b>Gemini:</b> {response.text}
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"⚠️ Gemini Chat Error: {e}")
        except Exception as e:
            st.error(f"⚠️ Server Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
