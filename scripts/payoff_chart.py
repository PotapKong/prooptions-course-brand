from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from brand_config import palette


def payoff(strategy: str, prices: np.ndarray, strike: float, premium: float, width: float) -> np.ndarray:
    if strategy == "long_call":
        return np.maximum(prices - strike, 0) - premium
    if strategy == "long_put":
        return np.maximum(strike - prices, 0) - premium
    if strategy == "short_call":
        return premium - np.maximum(prices - strike, 0)
    if strategy == "short_put":
        return premium - np.maximum(strike - prices, 0)
    if strategy == "bull_call_spread":
        long_call = np.maximum(prices - strike, 0) - premium
        short_call = (premium * 0.45) - np.maximum(prices - (strike + width), 0)
        return long_call + short_call
    if strategy == "bull_put_spread":
        short_put = premium - np.maximum(strike - prices, 0)
        long_put = np.maximum((strike - width) - prices, 0) - (premium * 0.45)
        return short_put + long_put
    raise ValueError(f"Unsupported strategy: {strategy}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate option payoff chart PNG.")
    parser.add_argument("--strategy", default="long_call", choices=[
        "long_call", "long_put", "short_call", "short_put", "bull_call_spread", "bull_put_spread"
    ])
    parser.add_argument("--strike", type=float, default=100)
    parser.add_argument("--premium", type=float, default=5)
    parser.add_argument("--width", type=float, default=15)
    parser.add_argument("--out", default="outputs/assets/payoff.png")
    parser.add_argument("--transparent", action="store_true")
    args = parser.parse_args()

    pal = palette()
    prices = np.linspace(args.strike * 0.55, args.strike * 1.45, 240)
    values = payoff(args.strategy, prices, args.strike, args.premium, args.width)

    fig = plt.figure(figsize=(8, 4.5), dpi=200)
    ax = fig.add_subplot(111)

    bg = pal["base_black"]
    fig.patch.set_facecolor("none" if args.transparent else bg)
    ax.set_facecolor("none" if args.transparent else bg)

    ax.axhline(0, linewidth=1.2, color=pal["graphite_gray"])
    ax.axvline(args.strike, linewidth=1.0, color=pal["champagne_gold"], linestyle="--")
    ax.plot(prices, values, linewidth=3.0, color=pal["terminal_green"])
    ax.fill_between(prices, values, 0, where=values >= 0, alpha=0.14, color=pal["terminal_green"])
    ax.fill_between(prices, values, 0, where=values < 0, alpha=0.16, color=pal["risk_red"])

    ax.grid(True, alpha=0.16, color=pal["warm_white"], linewidth=0.6)
    ax.tick_params(colors=pal["warm_white"], labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(pal["graphite_gray"])

    ax.set_title(args.strategy.replace("_", " ").upper(), color=pal["warm_white"], fontsize=12, pad=12)
    ax.set_xlabel("Underlying price", color=pal["warm_white"], fontsize=9)
    ax.set_ylabel("P/L", color=pal["warm_white"], fontsize=9)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    fig.savefig(out, transparent=args.transparent, bbox_inches="tight", pad_inches=0.08)
    print(out)


if __name__ == "__main__":
    main()
