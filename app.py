import streamlit as st
import pandas as pd
from pathlib import Path
import tempfile

from src.csv_profiler.io import read_csv_rows
from src.csv_profiler.profile import profile_rows
from src.csv_profiler.render import render_markdown


st.set_page_config(page_title="CSV Profiler", layout="wide")

st.title("CSV Profiling App")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = Path(tmp.name)

    try:
        rows = read_csv_rows(tmp_path)
        report = profile_rows(rows)

        st.subheader("Summary")
        col1, col2 = st.columns(2)
        col1.metric("Rows", report["n_rows"])
        col2.metric("Columns", report["n_cols"])

        st.subheader("Column Profiles")
        df = pd.DataFrame(report["columns"])
        st.dataframe(df, use_container_width=True)

        st.subheader("Markdown Report")
        md = render_markdown(report)
        st.code(md, language="markdown")

        st.download_button(
            label="Download Markdown Report",
            data=md,
            file_name="report.md",
            mime="text/markdown",
        )

    except Exception as e:
        st.error(str(e))
