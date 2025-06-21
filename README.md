# -CMOS-Inverter-Calculator
 Python-based simulation of a CMOS inverter that models advanced transistor behaviors in 0.25µm technology, including:  Body Effect (Threshold voltage variation with body bias)  Channel Length Modulation (Early Effect)  Drain current calculations in triode/saturation regions
# CMOS Inverter Simulation with Second-Order Effects  
A Python-based simulator for CMOS inverter behavior, accounting for:  
- **Body Effect** (Threshold voltage variation)  
- **Channel Length Modulation** (Early Effect)  
- **Velocity Saturation**  

## 📌 Key Features  
- Calculates **Vout vs. Vin** transfer characteristics  
- Models **NMOS/PMOS drain currents** with second-order effects  
- Interactive user inputs for Vdd, Vbulk, and transistor dimensions  
- Generates plots for:  
  - Transfer characteristics (Vin vs. Vout)  
  - Drain current (Vin vs. Id)  

## 🛠️ Tech Stack  
- Python (NumPy, SciPy, Matplotlib)  
- Semiconductor physics equations  

## 📊 Sample Output  
![Drain Current vs V_in](https://github.com/user-attachments/assets/3d409846-ee7f-4120-84e0-ba0cba51182a)
![V_out vs V_in](https://github.com/user-attachments/assets/dd0a8be2-e3a4-409b-a7fe-8cca7d1be865)


## 🚀 How to Run  
```bash
pip install numpy matplotlib scipy
python cmos_inverter.py
