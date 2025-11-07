import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime
import plotly.express as px

# -------------------------------------------------------------
# 🎨 PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="AI Timesheet Generator",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------------------------------
# 🌈 CUSTOM CSS
# -------------------------------------------------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at 20% 30%, #0f2027, #203a43, #2c5364);
    color: #fff;
}
.main-container {
    padding: 2rem;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.3);
}
.title {
    text-align: center;
    font-size: 2.8em;
    font-weight: 800;
    color: #00e0c6;
    margin-bottom: 0.3em;
}
.subtitle {
    text-align: center;
    font-size: 1.1em;
    color: #ccc;
    margin-bottom: 1.5em;
}
.stButton>button {
    background: linear-gradient(90deg, #00bfa5, #0091ea);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.8em 1em;
    transition: 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #0091ea, #00bfa5);
    transform: scale(1.03);
}
.dataframe-container {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 10px;
    overflow-x: auto;
}
.footer {
    text-align: center;
    color: #aaa;
    margin-top: 1.5em;
    font-size: 0.9em;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 🧭 HEADER
# -------------------------------------------------------------
st.markdown('<div class="title">🧠 AI Timesheet Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your Calendar (.ics), Email (.json/.csv), and Git data — Gemini AI will auto-generate your smart productivity report.</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# ⚙️ SIDEBAR
# -------------------------------------------------------------
st.sidebar.header("⚙️ Configuration")
backend_url = st.sidebar.text_input("Backend API URL", "http://127.0.0.1:8000/upload_files/")
st.sidebar.divider()
st.sidebar.markdown("💡 Tip: Upload any combination of Calendar, Email, or Git data to build your AI-powered timesheet.")

# -------------------------------------------------------------
# 📁 FILE UPLOADS
# -------------------------------------------------------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.subheader("📤 Upload Your Activity Data")
col1, col2 = st.columns(2)

with col1:
    calendar_file = st.file_uploader("📅 Calendar (.ics)", type=["ics"])
    repo_path = st.text_input("💻 Git Repository Path (optional)")

with col2:
    email_file = st.file_uploader("📧 Email Data (.json or .csv)", type=["json", "csv"])
    user_name = st.text_input("👤 Your Name", value="Sai Kumar Nimmala")

# -------------------------------------------------------------
# 🚀 PROCESS
# -------------------------------------------------------------
if st.button("🚀 Generate Timesheet"):
    files, data = {}, {"user_name": user_name, "git_repo_path": repo_path}
    if calendar_file: files["calendar_file"] = calendar_file
    if email_file: files["email_file"] = email_file

    with st.spinner("🧠 Generating your AI Timesheet... Please wait..."):
        try:
            response = requests.post(backend_url, data=data, files=files)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Timesheet Generated Successfully!")

                csv_data = result["csv_data"]
                summary = result["summary"]

                st.subheader("📊 Timesheet Summary")
                st.info(summary["ai_summary"])
                st.write(f"**Total Working Hours:** {summary['total_hours']} hrs")

                df = pd.read_csv(StringIO(csv_data))
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # -------------------------------------------------------------
                # 🥧 PIE CHART VISUALIZATION
                # -------------------------------------------------------------
                if "type" in df.columns and "duration_hours" in df.columns:
                    st.subheader("📈 Work Distribution by Activity Type")
                    chart_data = df.groupby("type")["duration_hours"].sum().reset_index()
                    fig = px.pie(
                        chart_data,
                        names="type",
                        values="duration_hours",
                        title="Time Spent by Activity Type",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)

                st.download_button(
                    label="⬇️ Download Timesheet CSV",
                    data=csv_data.encode("utf-8"),
                    file_name=f"{user_name.replace(' ', '_')}_timesheet.csv",
                    mime="text/csv"
                )

                # 🔁 Save to session
                if "history" not in st.session_state:
                    st.session_state["history"] = []
                st.session_state["history"].append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": user_name,
                    "hours": summary["total_hours"],
                    "summary": summary["ai_summary"]
                })
            else:
                st.error("❌ Failed to process files. Please check backend logs.")
                st.json(response.json())
        except Exception as e:
            st.error(f"⚠️ Error occurred: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 🕒 HISTORY
# -------------------------------------------------------------
if "history" in st.session_state and st.session_state["history"]:
    st.divider()
    st.subheader("📜 Previous Generations")
    hist_df = pd.DataFrame(st.session_state["history"])
    st.dataframe(hist_df, use_container_width=True)


