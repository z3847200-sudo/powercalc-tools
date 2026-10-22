# powercalc-tools

Dependency-free Python calculators for **power electronics** and **microstrip patch antennas** — built for students and hardware engineers doing first-pass sizing before simulation / PCB layout.

零依赖的电源与天线初步设计计算工具，适合在仿真和画板之前快速估算参数。

## Install

```bash
pip install powercalc-tools   # after PyPI release
# or from source:
git clone https://github.com/z3847200-sudo/powercalc-tools.git
cd powercalc-tools && pip install -e .
```

## Usage

```bash
# Buck: 12V -> 5V, 2A, 500kHz
powercalc buck --vin 12 --vout 5 --iout 2 --fs 500000
# Duty: 41.7%  Inductor min: ~9.72 µH  Capacitor min: ~3.0 µF

# Boost: 5V -> 12V, 1A, 400kHz
powercalc boost --vin 5 --vout 12 --iout 1 --fs 400000

# Patch antenna: 2.45 GHz on FR4 (Er=4.4, h=1.6mm)
powercalc patch --freq 2.45 --er 4.4 --h 1.6
# Width: ~37.2 mm  Length: ~28.8 mm
```

As a library:

```python
from powercalc import buck, patch
print(buck(vin=12, vout=5, iout=2, fs_hz=500_000))
print(patch(freq_hz=2.45e9, er=4.4, height_m=1.6e-3))
```

## What it does

- **Buck / Boost** — duty cycle, inductor ripple, minimum L & C (CCM)
- **Flyback** — turns-ratio estimate from reflected voltage
- **LDO** — power dissipation & efficiency
- **Patch antenna** — width / length / effective Er (transmission-line model)

Formulas follow standard TI / ADI application-note conventions. This is a first-pass tool — always verify with simulation (e.g. LTspice, CST) and datasheets.

## Roadmap

- [ ] Flybuck, SEPIC, synchronous rectification loss estimate
- [ ] Inductor saturation / RMS current checks, common E-series part suggestions
- [ ] Circular patch & inset-feed calculator, CST export helper
- [ ] Web UI

## Contributing

Issues and PRs welcome — especially corrections to formulas with a reference (app note / textbook page).

## License

MIT
