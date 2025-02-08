import pandas as pd
import streamlit as st
import scipy.integrate as integrate

df = pd.read_excel('Book1.xlsx', header=None, names=['Wavelength', 'SPD','SPD Normalized', 'X(λ)', 'Y(λ)', 'Z(λ)'])

df = df.apply(pd.to_numeric, errors='coerce')

df.dropna(inplace=True)

wavelengths = df['Wavelength'].values  # Wavelengths
spd = df[('SPD Normalized')].values  # Spectral Power Distribution (intensity)
cie_X = df['X(λ)'].values  # CIE color matching function X
cie_Y = df['Y(λ)'].values  # CIE color matching function Y
cie_Z = df['Z(λ)'].values  # CIE color matching function Z

X = integrate.simpson(spd * cie_X, wavelengths)
Y = integrate.simpson(spd * cie_Y, wavelengths)
Z = integrate.simpson(spd * cie_Z, wavelengths)


total = X + Y + Z
x = X / total
y = Y / total

st.write(f"X: {X}, Y: {Y}, Z: {Z}")
st.write(f"x: {x}, y: {y}")
