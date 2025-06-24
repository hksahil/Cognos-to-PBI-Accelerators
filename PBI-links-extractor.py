# Input is JSON that we get from Power BI Studio VS Code extension
## Code is %cmd SET API_PATH= /groups/groupid/
## GET ./reports

import streamlit as st
import pandas as pd
import json

st.title("Power BI Report Exporter (CSV)")
st.write("Paste your JSON list of Power BI reports below. Download a CSV with Name & Web URL.")

# Text area for JSON input
json_text = st.text_area("Paste JSON here", height=300)

if st.button("Generate CSV"):
    try:
        data = json.loads(json_text)
        df = pd.DataFrame(data)[["name", "webUrl"]]

        csv_data = df.to_csv(index=False)
        st.success("CSV generated successfully!")
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="powerbi_reports.csv",
            mime="text/csv"
        )
        st.dataframe(df)
    except Exception as e:
        st.error(f"Failed to process JSON: {e}")
