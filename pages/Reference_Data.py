import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os
import base64

st.set_page_config(layout="wide")
st.title('Reference Data')

def load_data():
    return pd.read_csv('difference_dataset.csv')


df = load_data()
col1, col2 = st.columns([1, 2])
current_directory = os.getcwd()

output_csv_path = os.path.join(current_directory, "reference_data.csv")

with col1:
    selected_columns = df.iloc[:, [0, 3]]
    st.dataframe(selected_columns, height=750)

    selected_columns.to_csv(output_csv_path, index=False)

    csv_data = selected_columns.to_csv(index=False).encode('utf-8')
    b64_csv = base64.b64encode(csv_data).decode('utf-8')

    st.markdown(f'<a href="data:file/csv;base64,{b64_csv}" download="reference_data.csv">Download Reference Data as CSV</a>', unsafe_allow_html=True)

with col2:
    x = selected_columns.iloc[:, 0]
    y = selected_columns.iloc[:, 1]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label="Difference in SPD", color="red")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Difference in SPD")
    plt.title("Difference Between SPDs")
    plt.legend()

    st.pyplot(plt)


