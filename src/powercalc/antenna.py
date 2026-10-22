"""Microstrip patch antenna first-pass sizing (transmission-line model)."""
from __future__ import annotations
import math
from dataclasses import dataclass

C0 = 299_792_458.0


@dataclass
class PatchResult:
    width_m: float
    length_m: float
    effective_er: float
    delta_l_m: float


def patch(freq_hz: float, er: float, height_m: float) -> PatchResult:
    """Rectangular patch dimensions for given substrate.

    freq_hz in Hz, er = substrate relative permittivity,
    height_m = substrate thickness in metres.
    """
    if freq_hz <= 0 or er < 1 or height_m <= 0:
        raise ValueError("invalid antenna parameters")
    w = (C0 / (2 * freq_hz)) * math.sqrt(2 / (er + 1))
    e_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * height_m / w) ** -0.5
    dl = 0.412 * height_m * ((e_eff + 0.3) * (w / height_m + 0.264)) / \
         ((e_eff - 0.258) * (w / height_m + 0.8))
    l_eff = C0 / (2 * freq_hz * math.sqrt(e_eff))
    length = l_eff - 2 * dl
    return PatchResult(w, length, e_eff, dl)
