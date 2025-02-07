import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from colour import MSDS_CMFS, SDS_ILLUMINANTS, SpectralShape, SpectralDistribution, sd_to_XYZ

st.set_page_config(layout="wide")
st.image("richter logo_schwarz.png", width=250)

uploaded_files = st.file_uploader(
    "Choose CSV files to compare", accept_multiple_files=True, type='csv'
)

if uploaded_files:
    filenames = [file.name for file in uploaded_files]
    options = st.multiselect('Select the files to compare',
                             filenames,
                             filenames[:2],
                             max_selections=2)

    if len(options) == 2:
        wavelengths = np.arange(360, 781, 1)
        spds = []

        for uploaded_file in uploaded_files:
            if uploaded_file.name not in options:
                continue

            data = pd.read_csv(uploaded_file, header=None)
            wavelength_column = data[0]
            value_column = data[1]

            interpolated_values = np.interp(wavelengths, wavelength_column, value_column)
            spds.append(interpolated_values)

        if len(spds) == 2:
            spd1, spd2 = spds

            cmfs = MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
            illuminant = SDS_ILLUMINANTS["D65"]
            shape = SpectralShape(360, 780, 1)  # Wavelengths from 360 nm to 780 nm, 1 nm step

            sd1 = SpectralDistribution(dict(zip(wavelengths, spd1)), shape)
            sd2 = SpectralDistribution(dict(zip(wavelengths, spd2)), shape)

            xyz1 = sd_to_XYZ(sd1, cmfs, illuminant)
            xyz2 = sd_to_XYZ(sd2, cmfs, illuminant)

            X1, Y1, Z1 = xyz1
            X2, Y2, Z2 = xyz2

            x1 = X1 / (X1 + Y1 + Z1)
            y1 = Y1 / (X1 + Y1 + Z1)

            x2 = X2 / (X2 + Y2 + Z2)
            y2 = Y2 / (X2 + Y2 + Z2)

            difference_in_number = spd2 - spd1
            difference_in_percentage = (difference_in_number / spd1) * 100

            data = {
                "Wavelength (nm)": wavelengths,
                "SPD1": spd1,
                "SPD2": spd2,
                "Difference in Number": difference_in_number,
                "Difference in Percentage (%)": difference_in_percentage,
                "x1 (Chromaticity SPD1)": x1,
                "y1 (Chromaticity SPD1)": y1,
                "x2 (Chromaticity SPD2)": x2,
                "y2 (Chromaticity SPD2)": y2
            }
            df = pd.DataFrame(data)
            col1, col2 = st.columns([1, 2])

            with col1:
                st.write("### Comparison Table")
                st.dataframe(df, height=750)


            with col2:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(wavelengths, spd1, label=options[0])
                ax.plot(wavelengths, spd2, label=options[1])
                ax.set_xlabel("Wavelength (nm)")
                ax.set_ylabel("Spectral Power Distribution")
                ax.set_title("Spectral Power Distribution Comparison")
                ax.legend()
                ax.grid()
                st.pyplot(fig)

            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Comparison Table as CSV",
                data=csv,
                file_name="comparison_table.csv",
                mime="text/csv"
            )

            difference_file_path = "difference_dataset.csv"
            df.to_csv(difference_file_path, index=False)
            st.write(f"Difference dataset saved as: {difference_file_path}")

            st.write(cmfs)


