import pandas as pd
import streamlit as st
import os

from carbon_calc import (
    estimate_total_emissions,
    enrich_energy_dataframe,
    generate_energy_insights,
    load_emission_factors,
)
from chatbot_module import answer_question, basic_answer
from summarizer import summarize_uploaded_file, extract_text

# 🔥 NEW IMPORTS FOR RAG
from langchain_community.document_loaders import CSVLoader, TextLoader
from langchain_core.documents import Document


# ---------------- SESSION ----------------
if "has_data" not in st.session_state:
    st.session_state["has_data"] = False

if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = None

# 🔥 NEW: store current session docs
if "docs" not in st.session_state:
    st.session_state["docs"] = []


# ---------------- CONFIG ----------------
st.set_page_config(page_title="EnergyInsightGPT", layout="wide")

os.makedirs("energy_data/usage", exist_ok=True)
os.makedirs("energy_data/reports", exist_ok=True)

st.title("🌱 EnergyInsightGPT")

tabs = st.tabs(["Overview", "Dashboard", "Carbon", "Chatbot", "Summarizer"])


# ---------------- OVERVIEW ----------------
with tabs[0]:
    st.markdown("""
### 🌍 AI-powered Sustainability Assistant

- 📊 Energy Dashboard (Charts + Insights)
- 🌱 Carbon Footprint Estimator
- 🤖 AI + Data Chatbot (RAG)
- 📄 Report Summarizer
- 📜 Policy Advisor
""")


# ---------------- DASHBOARD ----------------
with tabs[1]:
    st.header("📊 Energy Dashboard")

    csv_file = st.file_uploader("Upload Energy CSV", type=["csv"])

    if csv_file:
        try:
            path = os.path.join("energy_data/usage", csv_file.name)

            # ✅ Save file
            with open(path, "wb") as f:
                f.write(csv_file.getbuffer())

            # ✅ Load for dashboard
            df = pd.read_csv(path)
            enriched = enrich_energy_dataframe(df)

            st.success("✅ Data loaded")
            st.dataframe(enriched)

            # -------- CHARTS --------
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Energy Usage")
                st.bar_chart(enriched.set_index("location")["energy_usage_kWh"])

            with col2:
                st.subheader("CO₂ Emissions")
                st.bar_chart(enriched.set_index("location")["CO2_emission_kg"])

            # -------- PIE --------
            st.subheader("Usage Distribution")
            st.pyplot(
                enriched.set_index("location")["usage_share_pct"]
                .plot.pie(autopct="%1.1f%%")
                .figure
            )

            # -------- INSIGHTS --------
            st.subheader("💡 Insights")
            insights = generate_energy_insights(enriched)

            for i in insights:
                st.success(i)

            # 🔥 RAG FIX: Load ONLY this file into session
            loader = CSVLoader(path)
            docs = loader.load()

            st.session_state["docs"] = docs
            st.session_state["has_data"] = True
            st.session_state["vectorstore"] = None

            st.info(f"📂 Active file for RAG: {csv_file.name}")

        except Exception as e:
            st.error(f"Error: {str(e)}")


# ---------------- CARBON ----------------
with tabs[2]:
    st.header("🌱 Carbon Footprint Estimator")

    factors = load_emission_factors()

    electricity = st.number_input("Monthly Electricity (kWh)", 0.0)
    source = st.selectbox("Energy Source", factors["energy_source"])

    st.subheader("🏠 Appliance Usage (kWh/month)")

    col1, col2 = st.columns(2)

    with col1:
        ac = st.number_input("Air Conditioner", 0.0)
        fridge = st.number_input("Refrigerator", 0.0)

    with col2:
        washing = st.number_input("Washing Machine", 0.0)
        lighting = st.number_input("Lighting", 0.0)

    appliances = {
        "ac": ac,
        "fridge": fridge,
        "washing": washing,
        "lighting": lighting,
    }

    transport = st.number_input("Monthly Travel (km)", 0.0)

    if st.button("Estimate Carbon Footprint"):

        monthly, yearly = estimate_total_emissions(
            appliances, electricity, source, transport
        )

        st.subheader("📊 Results")

        c1, c2 = st.columns(2)
        c1.metric("Monthly CO₂", f"{monthly} kg")
        c2.metric("Yearly CO₂", f"{yearly} kg")

        if yearly > 3000:
            st.error("High emissions — reduce usage or switch sources")
        elif yearly > 1000:
            st.warning("Moderate emissions — optimize usage")
        else:
            st.success("Low emissions — good efficiency")


# ---------------- CHATBOT ----------------
with tabs[3]:
    st.header("🤖 AI + Data Assistant")

    mode = st.radio("Mode", ["General", "Data (RAG)", "Policy"])

    query = st.text_input("Ask your question")

    if st.button("Ask"):

        if not query.strip():
            st.warning("Enter a question")

        else:
            with st.spinner("Thinking..."):

                try:
                    if mode == "General":
                        st.markdown(basic_answer(query))

                    elif mode == "Data (RAG)":
                        if not st.session_state.get("has_data", False):
                            st.warning("Upload data first")
                        else:
                            st.markdown(answer_question(query))

                    elif mode == "Policy":
                        st.markdown(basic_answer(query))

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # 🔥 RESET FIX
    if st.button("Reset Chat Session"):
        st.session_state["has_data"] = False
        st.session_state["vectorstore"] = None
        st.session_state["docs"] = []
        st.success("Session reset")


# ---------------- SUMMARIZER ----------------
with tabs[4]:
    st.header("📄 Report Summarizer")

    file = st.file_uploader("Upload PDF/TXT")

    if file:
        try:
            path = os.path.join("energy_data/reports", file.name)

            # ✅ Save file
            with open(path, "wb") as f:
                f.write(file.getbuffer())

            # 🔥 Extract RAW text for RAG
            text = extract_text(file)

            if not text.strip():
                st.error("No readable content found.")
            else:
                docs = [Document(page_content=text)]

                # 🔥 RAG FIX
                st.session_state["docs"] = docs
                st.session_state["has_data"] = True
                st.session_state["vectorstore"] = None

                # Show summary
                with st.spinner("Analyzing report..."):
                    result = summarize_uploaded_file(file)
                    st.markdown(result)

                st.info(f"📂 Active file for RAG: {file.name}")

        except Exception as e:
            st.error(f"Error: {str(e)}")