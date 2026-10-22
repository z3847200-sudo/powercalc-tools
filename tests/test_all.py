import sys
sys.path.insert(0, "src")
from powercalc import buck, boost, patch

def test_buck_12_to_5():
    r = buck(vin=12, vout=5, iout=2, fs_hz=500_000)
    assert abs(r.duty - 5/12) < 1e-9
    assert r.inductor_min_h > 0 and r.capacitor_min_f > 0
    assert r.peak_inductor_a > 2

def test_boost_5_to_12():
    r = boost(vin=5, vout=12, iout=1, fs_hz=400_000)
    assert 0 < r.duty < 1
    assert r.inductor_min_h > 0

def test_patch_2_45ghz_fr4():
    r = patch(freq_hz=2.45e9, er=4.4, height_m=1.6e-3)
    # classic FR4 2.45 GHz patch is roughly 37 x 29 mm
    assert 0.030 < r.width_m < 0.045
    assert 0.025 < r.length_m < 0.035
