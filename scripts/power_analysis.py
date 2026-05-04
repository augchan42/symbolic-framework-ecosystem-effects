#!/usr/bin/env python3
"""Supplementary: Power analysis at current sample size."""
from statsmodels.stats.power import NormalIndPower, TTestIndPower
from statsmodels.stats.proportion import proportion_effectsize

prop_analysis = NormalIndPower()
ttest_analysis = TTestIndPower()


def main():
    print("="*60)
    print("POWER ANALYSIS — Current N=10 per cell")
    print("="*60)

    print("\nRequired n per arm for 80% power (alpha=0.05, two-sided):")

    es1 = proportion_effectsize(0.05, 0.45)
    n1 = prop_analysis.solve_power(effect_size=es1, power=0.8, alpha=0.05, alternative='two-sided')
    print(f"  Qin suppression (yarrow 5% vs tarot 45%): n={n1:.0f}")

    es2 = proportion_effectsize(0.05, 0.25)
    n2 = prop_analysis.solve_power(effect_size=es2, power=0.8, alpha=0.05, alternative='two-sided')
    print(f"  Qin suppression (yarrow 5% vs control 25%): n={n2:.0f}")

    es3 = proportion_effectsize(0.55, 0.19)
    n3 = prop_analysis.solve_power(effect_size=es3, power=0.8, alpha=0.05, alternative='two-sided')
    print(f"  Qi dominance (scrambled 55% vs others 19%): n={n3:.0f}")

    n4 = ttest_analysis.solve_power(effect_size=1.0, power=0.8, alpha=0.05, alternative='two-sided')
    print(f"  Peak SCs (d=1.0): n={n4:.0f}")

    print("\nPower at current n=10:")
    for label, es in [("Qin yarrow vs tarot", es1), ("Qi scrambled vs others", es3)]:
        pwr = prop_analysis.solve_power(effect_size=es, nobs1=10, alpha=0.05, alternative='two-sided')
        print(f"  {label}: {pwr:.0%}")

    pwr_peak = ttest_analysis.solve_power(effect_size=1.0, nobs1=10, alpha=0.05, alternative='two-sided')
    print(f"  Peak SCs (d=1.0): {pwr_peak:.0%}")

    print("\nWith Bonferroni correction (alpha=0.017, 3 primary tests):")
    n1b = prop_analysis.solve_power(effect_size=es1, power=0.8, alpha=0.017, alternative='two-sided')
    n3b = prop_analysis.solve_power(effect_size=es3, power=0.8, alpha=0.017, alternative='two-sided')
    n4b = ttest_analysis.solve_power(effect_size=1.0, power=0.8, alpha=0.017, alternative='two-sided')
    print(f"  Qin suppression: n={n1b:.0f}")
    print(f"  Qi dominance: n={n3b:.0f}")
    print(f"  Peak SCs: n={n4b:.0f}")


if __name__ == "__main__":
    main()
