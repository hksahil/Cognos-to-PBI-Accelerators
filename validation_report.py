import streamlit as st
import pandas as pd
import io
import numpy as np
import hashlib

def generate_hash_key(row):
    combined_values = ''.join(row.astype(str))
    return hashlib.md5(combined_values.encode()).hexdigest().upper()

def generate_validation_report(cognos_df, pbi_df):
    dims = [col for col in cognos_df.columns if col in pbi_df.columns and 
            (cognos_df[col].dtype == 'object' or '_id' in col.lower() or '_key' in col.lower() or
             '_ID' in col or '_KEY' in col)]
    cognos_measures = [col for col in cognos_df.columns if col not in dims]
    pbi_measures = [col for col in pbi_df.columns if col not in dims]
    all_measures = list(set(cognos_measures) & set(pbi_measures)) 

    cognos_df = cognos_df.applymap(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) else x)
    pbi_df = pbi_df.applymap(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) else x)

    cognos_df['unique_key'] = cognos_df.apply(generate_hash_key, axis=1)
    pbi_df['unique_key'] = pbi_df.apply(generate_hash_key, axis=1)

    cognos_df = cognos_df[['unique_key'] + [col for col in cognos_df.columns if col != 'unique_key']]
    pbi_df = pbi_df[['unique_key'] + [col for col in pbi_df.columns if col != 'unique_key']]

    validation_report = pd.DataFrame({'unique_key': list(set(cognos_df['unique_key']) | set(pbi_df['unique_key']))})

    for dim in dims:
        validation_report[dim] = validation_report['unique_key'].map(dict(zip(cognos_df['unique_key'], cognos_df[dim])))
        validation_report[dim].fillna(validation_report['unique_key'].map(dict(zip(pbi_df['unique_key'], pbi_df[dim]))), inplace=True)

    validation_report['presence'] = validation_report['unique_key'].apply(
        lambda key: 'Present in Both' if key in cognos_df['unique_key'].values and key in pbi_df['unique_key'].values
        else ('Present in Cognos' if key in cognos_df['unique_key'].values
              else 'Present in PBI')
    )

    for measure in all_measures:
        validation_report[f'{measure}_Cognos'] = validation_report['unique_key'].map(dict(zip(cognos_df['unique_key'], cognos_df[measure])))
        validation_report[f'{measure}_PBI'] = validation_report['unique_key'].map(dict(zip(pbi_df['unique_key'], pbi_df[measure])))
        
        if pd.api.types.is_numeric_dtype(cognos_df[measure]) and pd.api.types.is_numeric_dtype(pbi_df[measure]):
            validation_report[f'{measure}_Diff'] = validation_report[f'{measure}_PBI'].fillna(0) - validation_report[f'{measure}_Cognos'].fillna(0)
        else:
            validation_report[f'{measure}_Diff'] = validation_report[f'{measure}_PBI'].astype(str) + " vs " + validation_report[f'{measure}_Cognos'].astype(str)

    column_order = ['unique_key'] + dims + ['presence'] + \
                   [col for measure in all_measures for col in 
                    [f'{measure}_Cognos', f'{measure}_PBI', f'{measure}_Diff']]
    validation_report = validation_report[column_order]

    return validation_report, cognos_df, pbi_df

def generate_column_check(cognos_df, pbi_df):
    column_check = pd.DataFrame({
        'Cognos columns': cognos_df.columns,
        'PBI columns': pbi_df.columns,
        'match': ['Yes' if c == p else 'No' for c, p in zip(cognos_df.columns, pbi_df.columns)]
    })
    return column_check

def main():
    st.title("Validation Report Generator")

    st.markdown("""
    **Important Assumptions:**
    1. Upload the Excel file with two sheets: "Cognos" and "PBI".
    2. Make sure the column names are similar in both sheets.
    3. If there are ID/Key/Code columns, make sure the ID or Key columns contains "_ID" or "_KEY" (case insensitive)
    4. Working with merged reports? unmerge them like this [link](https://www.loom.com/share/c876bb4cf67e45e7b01cd64facb6f7d8?sid=fdd1bb3e-96cf-4eaa-af3e-2a951861a8cc)
   """)

    st.markdown("---")

    uploaded_file = st.file_uploader("Upload Excel file", type="xlsx")

    if uploaded_file is not None:
        try:
            xls = pd.ExcelFile(uploaded_file)
            cognos_df = pd.read_excel(xls, 'Cognos')
            pbi_df = pd.read_excel(xls, 'PBI')

            validation_report, cognos_df, pbi_df = generate_validation_report(cognos_df, pbi_df)
            column_check = generate_column_check(cognos_df, pbi_df)

            st.subheader("Validation Report Preview")
            st.dataframe(validation_report)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                cognos_df.to_excel(writer, sheet_name='Cognos', index=False)
                pbi_df.to_excel(writer, sheet_name='PBI', index=False)
                validation_report.to_excel(writer, sheet_name='Validation_Report', index=False)
                column_check.to_excel(writer, sheet_name='ColumnCheck', index=False)

            output.seek(0)
            
            st.download_button(
                label="Download Excel Report",
                data=output,
                file_name="validation_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
