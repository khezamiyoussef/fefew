import pandas as pd
import scipy.integrate as integrate


df_constants = pd.read_excel("constants_x_y_z.xlsx", header=None, names=['X(λ)', 'Y(λ)', 'Z(λ)'])
df = df_constants.apply(pd.to_numeric, errors='coerce')
cie_X = df_constants['X(λ)'].values  # CIE color matching function X
cie_Y = df_constants['Y(λ)'].values  # CIE color matching function Y
cie_Z = df_constants['Z(λ)'].values  # CIE color matching function Z


def calculate(spd, wavelengths):
  X = integrate.simpson(spd * cie_X, wavelengths)
  Y = integrate.simpson(spd * cie_Y, wavelengths)
  Z = integrate.simpson(spd * cie_Z, wavelengths)

  total = X + Y + Z
  x = X / total
  y = Y / total

  return {x, y}