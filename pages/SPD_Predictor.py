import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pages import spd_calculate
st.set_page_config(layout="wide")

st.title("SPD Predictor Based on a reference SPD and User Input")

user_file = st.file_uploader("Upload your CSV file", type=["xlsx"])




def read_reference_data():
    reference_file_path = "reference_data.csv"
    reference_data = pd.read_csv(reference_file_path, header=None, skiprows=1)
    return reference_data


reference_data = read_reference_data()

col1, col2 = st.columns([1, 2])

if user_file is not None:
    user_data =  pd.read_excel(user_file, header=None)

    try:
        combined_df = pd.concat([reference_data, user_data], axis=1, ignore_index=True)
        combined_df = combined_df.drop(columns=combined_df.columns[2])
        print(combined_df[combined_df.columns[1]])
        print(combined_df[combined_df.columns[2]])
        combined_df['sum_col_1_2'] = combined_df[combined_df.columns[1]] + combined_df[combined_df.columns[2]]

        combined_df.columns = ['wavelength (nm)', 'Reference SPD', 'Input SPD', 'Predicted SPD']

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(combined_df['wavelength (nm)'], combined_df['Input SPD'], label='Input SPD', color='red')
        ax.plot(combined_df['wavelength (nm)'], combined_df['Predicted SPD'], label='Predicted SPD', color='blue')
        x11, x12 = spd_calculate.calculate(combined_df['Input SPD'], combined_df['wavelength (nm)'])
        x21, x22 = spd_calculate.calculate(combined_df['Predicted SPD'], combined_df['wavelength (nm)'])
        st.write(f"x: {x11}, y: {x12}")
        st.write(f"x: {x21}, y: {x22}")
        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylabel("SPD")
        ax.set_title("Input SPD vs Predicted SPD")
        ax.legend()


    except Exception as e:
        st.error(f"Error processing the data: {e}")
        raise e

    with col1:

        st.write("Combined Dataframe:")
        st.dataframe(combined_df, height=750)

    with col2:
        st.pyplot(fig)


