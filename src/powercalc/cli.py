from __future__ import annotations
import argparse
from .converters import buck, boost, ldo_power, flyback_turns
from .antenna import patch


def _fmt(value: float, unit: str) -> str:
    for scale, prefix in [(1, ""), (1e-3, "m"), (1e-6, "µ"), (1e-9, "n")]:
        if abs(value) >= scale or prefix == "n":
            return f"{value/scale:.3g} {prefix}{unit}" if prefix != "" else f"{value:.3g} {unit}"
    return f"{value:.3g} {unit}"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="powercalc", description="Power & antenna design calculator")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("buck", help="Buck converter sizing")
    b.add_argument("--vin", type=float, required=True)
    b.add_argument("--vout", type=float, required=True)
    b.add_argument("--iout", type=float, required=True)
    b.add_argument("--fs", type=float, required=True, help="switching freq in Hz")

    bo = sub.add_parser("boost", help="Boost converter sizing")
    bo.add_argument("--vin", type=float, required=True)
    bo.add_argument("--vout", type=float, required=True)
    bo.add_argument("--iout", type=float, required=True)
    bo.add_argument("--fs", type=float, required=True)

    a = sub.add_parser("patch", help="Patch antenna sizing")
    a.add_argument("--freq", type=float, required=True, help="freq in GHz")
    a.add_argument("--er", type=float, required=True)
    a.add_argument("--h", type=float, required=True, help="substrate thickness in mm")

    args = p.parse_args(argv)
    if args.cmd == "buck":
        r = buck(args.vin, args.vout, args.iout, args.fs)
        print(f"Duty: {r.duty:.1%}")
        print(f"Inductor ripple: {r.inductor_ripple_a:.3g} A")
        print(f"Inductor min: {_fmt(r.inductor_min_h, 'H')}")
        print(f"Capacitor min: {_fmt(r.capacitor_min_f, 'F')}")
        print(f"Peak inductor current: {r.peak_inductor_a:.3g} A")
    elif args.cmd == "boost":
        r = boost(args.vin, args.vout, args.iout, args.fs)
        print(f"Duty: {r.duty:.1%}")
        print(f"Inductor min: {_fmt(r.inductor_min_h, 'H')}")
        print(f"Capacitor min: {_fmt(r.capacitor_min_f, 'F')}")
    elif args.cmd == "patch":
        r = patch(args.freq * 1e9, args.er, args.h * 1e-3)
        print(f"Width: {r.width_m*1e3:.2f} mm")
        print(f"Length: {r.length_m*1e3:.2f} mm")
        print(f"Effective Er: {r.effective_er:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
