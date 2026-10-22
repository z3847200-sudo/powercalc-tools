"""Power converter design calculations.

Formulas follow standard textbook / TI & ADI app-note conventions
for continuous conduction mode (CCM) unless noted.
"""
from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass
class BuckResult:
    duty: float
    inductor_ripple_a: float
    inductor_min_h: float
    capacitor_min_f: float
    peak_inductor_a: float


def buck(vin: float, vout: float, iout: float, fs_hz: float,
         ripple_ratio: float = 0.3, vripple: float = 0.01) -> BuckResult:
    """Buck converter first-pass sizing.

    vin, vout in V; iout in A; fs_hz switching frequency;
    ripple_ratio = inductor ripple / iout (0.2-0.4 typical);
    vripple = allowed output ripple as fraction of vout.
    """
    if not (0 < vout < vin):
        raise ValueError("buck requires 0 < vout < vin")
    duty = vout / vin
    di = iout * ripple_ratio
    # L = (Vin - Vout) * D / (fs * dI)
    l_min = (vin - vout) * duty / (fs_hz * di)
    # C >= dI / (8 * fs * dV)
    dv = vout * vripple
    c_min = di / (8 * fs_hz * dv)
    return BuckResult(duty, di, l_min, c_min, iout + di / 2)


@dataclass
class BoostResult:
    duty: float
    inductor_ripple_a: float
    inductor_min_h: float
    capacitor_min_f: float


def boost(vin: float, vout: float, iout: float, fs_hz: float,
          ripple_ratio: float = 0.3, vripple: float = 0.01,
          efficiency: float = 0.9) -> BoostResult:
    if not (0 < vin < vout):
        raise ValueError("boost requires 0 < vin < vout")
    duty = 1 - vin / vout
    i_in = (vout * iout) / (vin * efficiency)
    di = i_in * ripple_ratio
    l_min = vin * duty / (fs_hz * di)
    dv = vout * vripple
    c_min = iout * duty / (fs_hz * dv)
    return BoostResult(duty, di, l_min, c_min)


def ldo_power(vin: float, vout: float, iout: float) -> dict:
    """LDO dissipated power and junction temp estimate."""
    pd = (vin - vout) * iout
    return {"power_dissipation_w": pd, "efficiency": vout / vin if vin else 0}


def flyback_turns(vin_min: float, vout: float, duty_max: float = 0.45,
                  diode_drop: float = 0.5) -> float:
    """Flyback Ns/Np turns ratio from reflected voltage constraint."""
    vor = (vin_min * duty_max) / (1 - duty_max)
    return vor / (vout + diode_drop)
