#!/usr/bin/env python3
"""
Subatomic Materials Suite - Multi-Zone Thermal Discovery Engine
Author: Abhishek Singh
Copyright (c) 2026 Abhishek Singh
"""

import numpy as np
import pandas as pd


def run_subatomic_screening():
    print("==========================================================================")
    print("     SUBATOMIC MATERIALS SUITE: MULTI-ZONE THERMAL DISCOVERY ENGINE       ")
    print("==========================================================================")

    # --------------------------------------------------------------------------
    # ZONE A: Anharmonic Phonon Absorber Screening
    # --------------------------------------------------------------------------
    zone_a_candidates = [
        {"material": "Monolayer h-BN / GaN", "gamma_3ph_rate_ps1": 0.85, "optical_decay_ps": 1.2, "pdos_broadening_ev": 0.045},
        {"material": "Ti3C2Tx MXene (2D)", "gamma_3ph_rate_ps1": 1.42, "optical_decay_ps": 0.7, "pdos_broadening_ev": 0.068},
        {"material": "Graded TiN/AlN Monolayers", "gamma_3ph_rate_ps1": 1.15, "optical_decay_ps": 0.9, "pdos_broadening_ev": 0.058},
        {"material": "Monolayer Graphene", "gamma_3ph_rate_ps1": 0.32, "optical_decay_ps": 3.5, "pdos_broadening_ev": 0.018},
    ]

    print("\n[ZONE A] Screening Anharmonic Phonon Absorbers")
    results_a = []
    for item in zone_a_candidates:
        absorption_index = (item["gamma_3ph_rate_ps1"] / item["optical_decay_ps"]) * item["pdos_broadening_ev"] * 100
        is_pass = absorption_index > 2.5
        results_a.append({
            "Material": item["material"],
            "3-Phonon Decay Rate (ps⁻¹)": item["gamma_3ph_rate_ps1"],
            "Optical Lifetime (ps)": item["optical_decay_ps"],
            "Anharmonic Index": round(absorption_index, 3),
            "Status": "QUALIFIED" if is_pass else "REJECTED"
        })
    print(pd.DataFrame(results_a).to_string(index=False))

    # --------------------------------------------------------------------------
    # ZONE B: Acoustic Impedance Transformer Screening
    # --------------------------------------------------------------------------
    zone_b_candidates = [
        {"material": "Cu-Ag Sintered Nanopaste", "density_g_cm3": 9.5, "v_sound_m_s": 3600, "cte_ppm_k": 18.0},
        {"material": "Graded TaN/Cu Sub-micron Interlayer", "density_g_cm3": 11.2, "v_sound_m_s": 3200, "cte_ppm_k": 8.5},
        {"material": "Standard Sn-Ag-Cu Solder (SAC305)", "density_g_cm3": 7.4, "v_sound_m_s": 2400, "cte_ppm_k": 22.0},
    ]

    print("\n[ZONE B] Screening Acoustic Impedance Transformers")
    z_target_mid = 34.0
    results_b = []
    for item in zone_b_candidates:
        z_impedance = (item["density_g_cm3"] * 1000 * item["v_sound_m_s"]) / 1e6
        z_mismatch = abs(z_impedance - z_target_mid)
        cte_strain_risk = item["cte_ppm_k"] > 15.0
        is_pass = (z_mismatch < 5.0) and not cte_strain_risk
        results_b.append({
            "Material": item["material"],
            "Acoustic Impedance (MRayl)": round(z_impedance, 2),
            "Z Mismatch Delta": round(z_mismatch, 2),
            "CTE (ppm/K)": item["cte_ppm_k"],
            "Status": "QUALIFIED" if is_pass else "REJECTED"
        })
    print(pd.DataFrame(results_b).to_string(index=False))

    # --------------------------------------------------------------------------
    # ZONE C: Radiator Material Assembly Screening
    # --------------------------------------------------------------------------
    zone_c_candidates = [
        {"material": "Copper-Diamond (Cu-Diamond) Composite", "thermal_cond_w_mk": 1200, "density_g_cm3": 5.4},
        {"material": "HOPG Graphite + Ceramic Coating", "thermal_cond_w_mk": 1500, "density_g_cm3": 2.2},
        {"material": "Standard Pure Copper (C11000)", "thermal_cond_w_mk": 390, "density_g_cm3": 8.9},
        {"material": "Aluminum 6061-T6 Heat Sink", "thermal_cond_w_mk": 167, "density_g_cm3": 2.7},
    ]

    print("\n[ZONE C] Screening Radiator Materials under Forced-Air Cooling")
    h_conv = 125.0
    area_rad_m2 = 0.010  # 4x Finned surface extension
    delta_T_amb = 40.0

    results_c = []
    for item in zone_c_candidates:
        q_air_w = h_conv * area_rad_m2 * delta_T_amb
        q_spreading_factor = item["thermal_cond_w_mk"] / 390.0
        total_effective_cooling_w = q_air_w * q_spreading_factor
        is_pass = total_effective_cooling_w >= 20.0
        results_c.append({
            "Material": item["material"],
            "Thermal Cond (W/m·K)": item["thermal_cond_w_mk"],
            "Spreading Factor": round(q_spreading_factor, 2),
            "Power Dissipation Capacity (W)": round(total_effective_cooling_w, 2),
            "Status": "QUALIFIED" if is_pass else "REJECTED"
        })
    print(pd.DataFrame(results_c).to_string(index=False))


if __name__ == "__main__":
    run_subatomic_screening()
