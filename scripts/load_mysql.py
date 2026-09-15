from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "processed"

DB_USER = os.getenv("MYSQL_USER", "root")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_NAME = os.getenv("MYSQL_DATABASE", "email_abc")

RENAME = {"group": "test_group"}

def read_password() -> str:
    if os.environ.get("MYSQL_PASSWORD"):
        return os.environ["MYSQL_PASSWORD"].strip()
    p = ROOT / "pass.txt"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                return line.strip()
    raise SystemExit("нет пароля: MYSQL_PASSWORD или pass.txt")

def main() -> None:
    pwd = read_password()
    root_engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{pwd}@{DB_HOST}/"
    )
    with root_engine.begin() as conn:
        conn.execute(
            text( f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`" "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    engine = create_engine( f"mysql+pymysql://{DB_USER}:{pwd}@{DB_HOST}/{DB_NAME}")
    clean = pd.read_parquet(OUT_DIR / "clean.parquet")
    clean = clean.rename(columns=RENAME)
    if "segment" in clean.columns:
        clean = clean.drop(columns=["segment"])
    clean.to_sql("clean_users", engine, if_exists="replace", index=False, chunksize=5000)
    print("clean_users", len(clean))


if __name__ == "__main__":
    main()
