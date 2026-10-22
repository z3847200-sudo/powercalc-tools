import sys
sys.path.insert(0, "src")
from powercalc import buck, patch
print(buck(vin=12, vout=5, iout=2, fs_hz=500_000))
print(patch(freq_hz=2.45e9, er=4.4, height_m=1.6e-3))
