#!/usr/bin/env python3
"""
3-Zone Thermal Stress & Safe Operating Area (SOA) Simulation Suite
Author: Abhishek Singh
Copyright (c) 2026 Abhishek Singh
"""

import numpy as np
import pandas as pd


class ThermalStackStressSimulator:
    def __init__(self, fin_multiplier=4.0, h_conv=125.0):
        self.kappa_gan = 130.0          # W/m·K
        self.kappa_mxene = 65.0         # Cross-plane W/m·K
        self.kappa_tan_cu = 180.0       # Interlayer W/m·K
        self.kappa_cu_diamond = 1200.0  # Radiator W/m·K

        self.d_mxene = 8.0e-9           # 8 nm
        self.d_tan_cu = 18.0e-9         # 18 nm
        self.d_cu_diamond = 1.5e-3      # 1.5 mm

        self.cte_gan = 5.6e-6
        self.cte_tan_cu = 8.5e-6
        self.youngs_modulus_tan_cu = 120.0e9

        self.eta_siphon = 0.95
        self.fin_multiplier = fin_multiplier
        self.h_conv = h_conv
        self.base_area_m2 = 0.0025

    def compute_junction_temp(self, q_local_kw_cm2, t_ambient_c):
        q_m2 = q_local_kw_cm2 * 1.0e7
        r_spot = 50.0e-9

        delta_t_unmitigated = (q_m2 * r_spot) / self.kappa_gan
        delta_t_hotspot = delta_t_unmitigated * (1.0 - self.eta_siphon)

        r_cond_m2k_w = (self.d_mxene / self.kappa_mxene) + \
                       (self.d_tan_cu / self.kappa_tan_cu) + \
                       (self.d_cu_diamond / self.kappa_cu_diamond)
        delta_t_conduction = q_m2 * r_cond_m2k_w * 1.0e-4

        q_channel_total_w = q_local_kw_cm2 * 0.15
        area_eff = self.base_area_m2 * self.fin_multiplier
        delta_t_convection = q_channel_total_w / (self.h_conv * area_eff)

        t_junction_c = t_ambient_c + delta_t_hotspot + delta_t_conduction + delta_t_convection
        return t_junction_c, delta_t_hotspot, delta_t_conduction, delta_t_convection

    def compute_interface_shear_stress(self, t_junction_c, t_ref_c=25.0):
        delta_t = abs(t_junction_c - t_ref_c)
        delta_cte = abs(self.cte_tan_cu - self.cte_gan)
        shear_stress_pa = self.youngs_modulus_tan_cu * delta_cte * delta_t
        return shear_stress_pa / 1.0e6


def run_soa_sweep():
    sim = ThermalStackStressSimulator(fin_multiplier=4.0, h_conv=125.0)
    ambient_temps = [-40.0, -10.0, 25.0, 45.0, 65.0]
    power_densities = [50.0, 100.0, 200.0, 300.0]

    results = []
    for t_amb in ambient_temps:
        for q_flux in power_densities:
            t_j, dt_spot, dt_cond, dt_conv = sim.compute_junction_temp(q_flux, t_amb)
            shear_stress = sim.compute_interface_shear_stress(t_j)

            pass_tj = t_j <= 150.0
            pass_stress = shear_stress <= 150.0
            status = "PASS (SOA)" if (pass_tj and pass_stress) else "DERATED"

            results.append({
                "Ambient (°C)": t_amb,
                "Flux (kW/cm²)": q_flux,
                "Hotspot ΔT (K)": round(dt_spot, 2),
                "Cond ΔT (K)": round(dt_cond, 2),
                "Conv ΔT (K)": round(dt_conv, 2),
                "T_j (°C)": round(t_j, 2),
                "Shear (MPa)": round(shear_stress, 2),
                "Status": status
            })

    df = pd.DataFrame(results)
    print("==========================================================================")
    print("      SUBATOMIC MATERIALS SUITE: THERMAL STRESS & SOA SIMULATION LOG      ")
    print("==========================================================================")
    print(df.to_string(index=False))


if __name__ == "__main__":
    run_soa_sweep()
