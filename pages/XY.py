import pandas as pd
import streamlit as st
import scipy.integrate as integrate


def page():


  df_constants = pd.read_excel("constants_x_y_z.xlsx", header=None, names=['X(λ)', 'Y(λ)', 'Z(λ)'])
  df = df_constants.apply(pd.to_numeric, errors='coerce')
  cie_X = df_constants['X(λ)'].values  # CIE color matching function X
  cie_Y = df_constants['Y(λ)'].values  # CIE color matching function Y
  cie_Z = df_constants['Z(λ)'].values  # CIE color matching function Z




  st.set_page_config(layout="wide")

  st.title("Upload to predict")

  user_file = st.file_uploader("Upload your CSV file", type=["xlsx"])
  if user_file == None:
    return

  df = pd.read_excel(user_file, header=None, names=['Wavelength', 'SPD'])

  df = df.apply(pd.to_numeric, errors='coerce')

  df.dropna(inplace=True)

  wavelengths = df['Wavelength'].values  # Wavelengths
  spd = df[('SPD')].values  # Spectral Power Distribution (intensity)



  print(wavelengths)
  print(spd)

  X = integrate.simpson(spd * cie_X, wavelengths)
  Y = integrate.simpson(spd * cie_Y, wavelengths)
  Z = integrate.simpson(spd * cie_Z, wavelengths)

  total = X + Y + Z
  x = X / total
  y = Y / total


  st.write(f"X: {X}, Y: {Y}, Z: {Z}")
  st.write(f"x: {x}, y: {y}")


page()