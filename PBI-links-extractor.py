# Input is JSON that we get from Power BI Studio VS Code extension
## Code is %cmd SET API_PATH= /groups/groupid/
## GET ./reports

import streamlit as st
import pandas as pd
import json
import re

st.title("Power BI Report Exporter (CSV)")
st.write("Paste your JSON list of Power BI reports below. Download a CSV with Name & Web URL.")

# Text area for JSON input
json_text = st.text_area("Paste JSON here", height=300)

if st.button("Generate CSV"):
    if not json_text.strip():
        st.error("Please paste JSON data first!")
    else:
        try:
            # Try to clean common JSON issues
            cleaned_json = json_text.strip()
            
            # Remove trailing commas before closing brackets/braces
            cleaned_json = re.sub(r',(\s*[}\]])', r'\1', cleaned_json)
            
            # Parse the JSON
            data = json.loads(cleaned_json)
            
            # Handle different JSON structures
            if isinstance(data, dict):
                # If it's a dict, look for a 'value' key (common in Power BI API responses)
                if 'value' in data:
                    data = data['value']
                else:
                    st.error("JSON object doesn't contain expected 'value' array")
                    st.stop()
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Check if required columns exist
            required_cols = ['name', 'webUrl']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"Missing required columns: {missing_cols}")
                st.write("Available columns:", list(df.columns))
                st.stop()
            
            # Select only the required columns
            df_export = df[required_cols].copy()
            
            # Generate CSV
            csv_data = df_export.to_csv(index=False)
            
            st.success(f"CSV generated successfully! Found {len(df_export)} reports.")
            
            # Download button
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="powerbi_reports.csv",
                mime="text/csv"
            )
            
            # Display preview
            st.dataframe(df_export)
            
        except json.JSONDecodeError as e:
            st.error(f"Failed to process JSON: {e}")
            st.write("**Tips to fix JSON issues:**")
            st.write("1. Remove trailing commas before closing brackets")
            st.write("2. Use double quotes (not single quotes)")
            st.write("3. Escape special characters in URLs")
            st.write("4. Ensure all brackets/braces are properly closed")
            
            # Show the problematic area
            error_line = getattr(e, 'lineno', None)
            error_col = getattr(e, 'colno', None)
            if error_line and error_col:
                st.write(f"**Error at line {error_line}, column {error_col}**")
                lines = json_text.split('\n')
                if error_line <= len(lines):
                    st.code(lines[error_line-1])
                    st.write("^" + " " * (error_col-1) + "Problem might be here")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write("Please check your JSON format and try again.")
