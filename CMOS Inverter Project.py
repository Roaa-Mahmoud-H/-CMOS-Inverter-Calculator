# --- 0.25um transistor models for HSPICE ---
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# --- Constants for NMOS ---
Vth_n0 = 0.43
Kn_per_wl = 1e-3 * 165.6
phi_n = 0.35
gamma_n_default = 0.6
lambda_n_default = 0.09
u0n = 455.3033
tox = 5.8

# --- Constants for PMOS ---
Vth_p0 = -0.615
Kp_per_wl = 1e-3 * 102.6
phi_p = 0.35
gamma_p_default = 0.4
lambda_p_default = 0.05
u0p = 158.67

# --- User Inputs ---
Vdd = float(input("Enter the supply voltage (Vdd): "))
Vbulk = float(input("Enter the value for Vbulk (V): ") or 0)
W_n = float(input("NMOS Channel Width (W): "))
L_n = float(input("NMOS Channel Length (L): "))
W_p = float(input("PMOS Channel Width (W): "))
L_p = float(input("PMOS Channel Length (L): "))
end = float(input("Enter end value of Vin range (start is 0): "))
step = 0.01
Vin_range = np.arange(0, end + step, step)

# --- Toggle Second Order Effects ---
USE_SECOND_ORDER = input(
    "Use second-order effects? (y/n): ").strip().lower() == 'y'

cox = .34/tox * .1
# calc:
Kn = u0n * cox * (W_n / L_n)*100
Kp = u0p * cox * (W_p / L_p)*100


# --- Threshold Voltage Functions ---
def vth_nmos(Vsb):
    gamma = gamma_n_default if USE_SECOND_ORDER else 0
    return Vth_n0 + gamma * (sqrt(2 * phi_n + Vsb) - sqrt(2 * phi_n))


def vth_pmos(Vsb):
    gamma = gamma_p_default if USE_SECOND_ORDER else 0
    return Vth_p0 + gamma * (sqrt(2 * phi_p + Vsb) - sqrt(2 * phi_p))

# --- Current Equations ---


def Id_nmos(Vgs, Vds, Vsb):
    Vth = vth_nmos(Vsb)
    lamb = lambda_n_default if USE_SECOND_ORDER else 0
    if Vgs <= Vth:
        return 0
    elif Vds < (Vgs - Vth):
        return Kn * ((Vgs - Vth) * Vds - 0.5 * Vds**2) * (1 + lamb * Vds)
    else:
        return 0.5 * Kn * (Vgs - Vth)**2 * (1 + lamb * Vds)


def Id_pmos(Vsg, Vsd, Vsb):
    Vth = abs(vth_pmos(Vsb))
    lamb = lambda_p_default if USE_SECOND_ORDER else 0
    if Vsg <= Vth:  # cut off
        return 0
    elif Vsd < (Vsg - Vth):  # Triode Region
        return Kp * ((Vsg - Vth) * Vsd - 0.5 * Vsd**2) * (1 + lamb * Vsd)
    else:  # Saturation Region
        return 0.5 * Kp * (Vsg - Vth)**2 * (1 + lamb * Vsd)

# --- Vout Calculation ---


def calculate_vout(Vin_range):
    Vout_vals = []
    for Vin in Vin_range:
        def error(Vout):
            In = Id_nmos(Vin, Vout, Vbulk)
            Ip = Id_pmos(Vdd - Vin, Vdd - Vout, Vbulk)
            return In - Ip
        Vout_sol = fsolve(error, Vdd / 2)[0]
        Vout_vals.append(Vout_sol)
    return Vout_vals

# --- Id Calculation ---


def calculate_id(Vin_range, Vout_vals):
    return [Id_nmos(Vin, Vout, Vbulk) for Vin, Vout in zip(Vin_range, Vout_vals)]


# --- Run Simulation ---
Vout_vals = calculate_vout(Vin_range)
Id_vals = calculate_id(Vin_range, Vout_vals)

# --- Plot Transfer Curve ---
plt.figure(figsize=(8, 5))
plt.plot(Vin_range, Vout_vals, label="Vout vs Vin", color="blue")
plt.xlabel("Vin (V)")
plt.ylabel("Vout (V)")
plt.title("CMOS Inverter Transfer Characteristic{}".format(
    " (With 2nd Order)" if USE_SECOND_ORDER else " (No Gamma/Lambda)"))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- Plot Drain Current ---
plt.figure(figsize=(8, 5))
plt.plot(Vin_range, Id_vals, label="Id vs Vin", color="red")
plt.xlabel("Vin (V)")
plt.ylabel("Id (A)")
plt.title("Drain Current vs Vin{}".format(
    " (With 2nd Order)" if USE_SECOND_ORDER else " (No Gamma/Lambda)"))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
