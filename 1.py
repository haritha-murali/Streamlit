import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Student details fetcher")

st.write("""
    Upload an Excel file with student details and fetch 'Name' and 'ID' columns
    """)

# Function to read the uploaded Excel file and filter the relevant columns
def process_excel(uploaded_file):
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Check if the columns 'Name' and 'ID' exist, then extract them
    if 'Name' in df.columns and 'ID' in df.columns:
        filtered_df = df[['Name', 'ID']]
    else:
        st.error("The Excel file must contain 'Name' and 'ID' columns.")
        return None
    
    return filtered_df

# Function to convert DataFrame to Excel file for download
def to_excel(df):
    # Save DataFrame to a BytesIO object as an Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Students")
    output.seek(0)
    return output

# Streamlit UI
st.title("Excel Reader - Student Names and IDs Extractor")

# File upload widget
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Process the uploaded Excel file
    df = process_excel(uploaded_file)

    if df is not None:
        # Show the preview of the filtered DataFrame
        st.subheader("Filtered Data (Names and IDs)")
        st.write(df)

        # Create a download button for the output Excel file
        excel_file = to_excel(df)
        st.download_button(
            label="Download Filtered Excel",
            data=excel_file,
            file_name="filtered_students.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
