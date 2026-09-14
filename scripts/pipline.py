from pathlib import Path
import pandas as pd
from math import erfc, sqrt
from scipy.stats import chi2 as chi2_dist

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv"

# id в файле нет c таким встречаться ecom, 1 клиент = 1 строка

GROUP_COL = "segment"  # рука теста
OUTCOME_COLS = ["visit", "conversion"]  # 0/1
SPEND_COL = "spend"  # непрерывная (2 недели)
SEGMENT_COL = "channel"  # срез; ещё есть newbie

CONTROL = "No E-Mail"
TREATMENT_M = "Mens E-Mail"
TREATMENT_W = "Womens E-Mail"
ARMS = [CONTROL, TREATMENT_M, TREATMENT_W]  # план 1/3 x3


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    #print("columns", df.columns.to_list())
    #print("shape", df.shape)
    #print("dtypes", df.dtypes)
    #print("isna", df.isna().sum())
    #print(df.head(3))
    return df


def chek_grain(df: pd.DataFrame) -> str:
    rows=len(df)
    grain = "user" 
    print("grain ->", grain, "= rows = ", rows)
    return grain

def prepare_types(df: pd.DataFrame)->pd.DataFrame:
    df = df.copy()
    df[GROUP_COL] = df[GROUP_COL].astype(str).str.strip()
    df[SEGMENT_COL] = df[SEGMENT_COL].astype(str).str.strip()
    df["zip_code"] = df["zip_code"].astype(str).str.strip()
    df["history_segment"] = df["history_segment"].astype(str).str.strip()
    for c in OUTCOME_COLS:
        df[c] = df[c].astype(int)
    df["mens"] = df["mens"].astype(int)
    df["womens"] = df["womens"].astype(int)
    df["newbie"] = df["newbie"].astype(int)
    df["recency"] = df["recency"].astype(int)
    df["history"] = pd.to_numeric(df["history"], errors="coerce")
    df[SPEND_COL] = pd.to_numeric(df[SPEND_COL], errors="coerce")
    return df

def build_clean(df: pd.DataFrame)-> pd.DataFrame:
    clean = df.copy()
    # в датасете 6562 дубля, буду удалять
    # и просто вспомнил как работают дубли...
    print("dup =", int(clean.duplicated().sum()))
    #print("no dup = ", len(clean.drop_duplicates()))
    #print(clean.duplicated(keep=False))
    #print(clean[clean.duplicated(keep="first")])
    clean = clean.drop_duplicates()
    #тут уже готовые имена рук
    #befor = len(clean)
    clean["group"] = clean[GROUP_COL]
    clean = clean[clean["group"].isin(ARMS)].copy()
    #print("clean dup = ", len(clean))
    #print("befor", befor, "->", len(clean))
    return clean        

def srm_check(clean: pd.DataFrame)->None:
    n = len(clean)
    n_c = int((clean["group"] == CONTROL).sum())
    n_t1 = int((clean["group"] == TREATMENT_M).sum())
    n_t2 = int((clean["group"] == TREATMENT_W).sum())
    exp_c, exp_t1, exp_t2 = n*(1/3), n*(1/3), n*(1/3)
    # тут возникли проблемы без scipy по этому поставил
    stat_chi2 = (n_c - exp_c)**2/exp_c + (n_t1 - exp_t1)**2/exp_t1 + (n_t2 - exp_t2)**2/exp_t2
    p = chi2_dist.sf(stat_chi2, df=2)
    print("---srm---")
    print(n, CONTROL, n_c, f"{100*n_c/n:.1f}%", 
          TREATMENT_M, n_t1, f"{100*n_t1/n:.1f}%",
          TREATMENT_W, n_t2, f"{100*n_t2/n:.1f}%")
    print("chi2", round(stat_chi2, 3), "p", round(float(p), 4))

def sanity_check (raw: pd.DataFrame, clean: pd.DataFrame)->None:
    print("---sanity---")
    print("rows", len(raw), "clean rows ->", len(clean))

def add_key(clean: pd.DataFrame)->pd.DataFrame:
    print("keys=rows", len(clean))
    return clean

def save_tables(clean: pd.DataFrame)->None:
    out = ROOT /"data"/"processed"
    out.mkdir(parents=True, exist_ok=True)
    clean.to_parquet(out/ "clean.parquet")
    back=pd.read_parquet(out/"clean.parquet")
    print("save", len(back))

def main() -> None:
    raw = load_data(RAW_PATH)
    chek_grain(raw)
    dtype = prepare_types(raw)
    clean = build_clean(dtype)
    srm_check(clean)
    sanity_check(raw, clean)
    add_key(clean)
    save_tables(clean)

if __name__ == "__main__":
    main()
