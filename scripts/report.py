from pathlib import Path
import pandas as pd
from math import erfc, sqrt

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "processed"


GROUP = "group"  # из pipeline
CONTROL = "No E-Mail"
TREATMENT_M = "Mens E-Mail"
TREATMENT_W = "Womens E-Mail"
OUTCOME = "visit"  # основная 0/1
CONV = "conversion"
SPEND = "spend"
SEGMENT_COL = "channel"  # срез
GEO_COL = "zip_code"  # срез гео 
ALPHA = 0.05  # порог значимости

def load_tables() -> pd.DataFrame:
    return pd.read_parquet(OUT_DIR / "clean.parquet")

def ztest(clean: pd.DataFrame, control: str, treatment: str, outcome: str):
    a = clean.loc[clean[GROUP] == control, outcome]
    b = clean.loc[clean[GROUP] == treatment, outcome]
    n_c, n_t = len(a), len(b)
    rate_c, rate_t = a.mean(), b.mean() 
    diff = rate_t - rate_c  
    p_pool = (a.sum() + b.sum()) / (n_c + n_t)
    se = sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_t)) 
    z = diff / se if se > 0 else 0.0
    p_val = erfc(abs(z) / sqrt(2))
    se_diff = sqrt(rate_c * (1 - rate_c) / n_c + rate_t * (1 - rate_t) / n_t)
    ci_lo = diff - 1.96 * se_diff
    ci_hi = diff + 1.96 * se_diff
    print(outcome, "|", treatment, "vs", control)
    print("n control  / test:", n_c, n_t)
    print("rate control - > test:", round(rate_c * 100, 2), round(rate_t * 100, 2))
    print("diff pp(test-control):", round(diff * 100, 2))
    print("z:", round(z, 4), "p_val", round(p_val, 4))
    print("CI95 pp:", round(ci_lo * 100, 2), round(ci_hi * 100, 2))
    return diff, p_val

def welch_spend(clean: pd.DataFrame, control: str, treatment: str):
    a = clean.loc[clean[GROUP] == control, SPEND].astype(float)
    b = clean.loc[clean[GROUP] == treatment, SPEND].astype(float)
    n_c, n_t = len(a), len(b)
    mean_c, mean_t = a.mean(), b.mean()
    diff = mean_t - mean_c
    se = sqrt(a.var(ddof=1) / n_c + b.var(ddof=1) / n_t)
    t = diff / se if se > 0 else 0.0
    p_val = erfc(abs(t) / sqrt(2)) 
    print("spend |", treatment, "vs", control)
    print("n control  / test:", n_c, n_t)
    print("mean control - > test:", round(mean_c, 4), round(mean_t, 4))
    print("diff (test-control):", round(diff, 4))
    print("t:", round(t, 4), "p_val", round(p_val, 4))
    return diff, p_val

def channel_segment(clean: pd.DataFrame) -> None:
    # срез channel
    print("--- channel ---")
    check = clean.groupby([GROUP, SEGMENT_COL])[OUTCOME].agg(["count", "sum", "mean"])
    print(check)

def zip_segment(clean: pd.DataFrame) -> None:
    # срез zip_code
    print("--- zip_code ---")
    check = clean.groupby([GROUP, GEO_COL])[OUTCOME].agg(["count", "sum", "mean"])
    print(check)

def verdict(diff_v, p_v, diff_c, p_c, diff_s, p_s) -> None:
    ok_v = p_v < ALPHA and diff_v > 0
    ok_c = p_c < ALPHA and diff_c > 0
    ok_s = p_s < ALPHA and diff_s > 0
    if ok_v and ok_c and ok_s:
        print(f"ВЕРДИКТ: катим Mens - visit/conversion/spend выше No E-Mail (visit {diff_v * 100:.2f} pp, conv {diff_c * 100:.2f} pp, spend +{diff_s:.2f})")
    elif ok_v and (ok_c or ok_s):
        print(f"ВЕРДИКТ: катим Mens - visit выше No E-Mail, {'conversion' if ok_c else 'spend'} ок ({diff_v * 100:.2f} pp, p={p_v:.4f})")
    elif ok_v:
        print(f"ВЕРДИКТ: visit у Mens выше No E-Mail, но conversion/spend без полного плюса ({diff_v * 100:.2f} pp)")
    elif p_v < ALPHA and diff_v < 0:
        print("ВЕРДИКТ: Mens хуже No E-Mail по visit - не катим")
    else:
        print("ВЕРДИКТ: не катим без доп. данных")

def main() -> None:
    clean = load_tables()
    print("--- visit ---")
    diff_v, p_v = ztest(clean, CONTROL, TREATMENT_M, OUTCOME)
    ztest(clean, CONTROL, TREATMENT_W, OUTCOME)
    ztest(clean, TREATMENT_M, TREATMENT_W, OUTCOME)
    print("--- conversion ---")
    diff_c, p_c = ztest(clean, CONTROL, TREATMENT_M, CONV)
    ztest(clean, CONTROL, TREATMENT_W, CONV)
    ztest(clean, TREATMENT_M, TREATMENT_W, CONV)
    print("--- spend ---")
    diff_s, p_s = welch_spend(clean, CONTROL, TREATMENT_M)
    welch_spend(clean, CONTROL, TREATMENT_W)
    welch_spend(clean, TREATMENT_M, TREATMENT_W)
    channel_segment(clean)
    zip_segment(clean)
    verdict(diff_v, p_v, diff_c, p_c, diff_s, p_s)

if __name__ == "__main__":
    main()
