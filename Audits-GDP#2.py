import hashlib
import os
import pandas as pd

INPUT_FILE   = r"C:\Users\hp\Downloads\Data_11.csv"
OUTPUT_STEP1 = r"C:\Users\hp\Downloads\Step1_minimization.csv"
OUTPUT_STEP2 = r"C:\Users\hp\Downloads\Step2_pending_access.csv"

# header=None -> the file has no header row; we name the 9 columns ourselves
df = pd.read_csv(INPUT_FILE, sep=";", header=None, dtype=str, encoding="utf-8-sig")
df.columns = ["first_name", "last_name", "email", "gender", "ip_address",
              "dsar_status", "last_login_at", "cloud_region", "other_date"]
print("Rows loaded:", len(df))

# SHA-256 hashing of personal data
def sha256(v):
    return hashlib.sha256(str(v).encode("utf-8")).hexdigest() if pd.notna(v) else v

for c in ["first_name", "last_name", "email", "ip_address"]:
    df[c] = df[c].apply(sha256)

# STEP 1: GDPR Art. 5 - every login BELOW 2026-01-01
login = pd.to_datetime(df["last_login_at"], errors="coerce")
step1 = df[login < pd.Timestamp("2026-01-01")]

# STEP 2: DSAR status = Pending_Access, within step 1
step2 = step1[step1["dsar_status"].str.strip().str.lower() == "pending_access"]


# EXPORT: save in the same folder as this script
out_dir = os.path.dirname(os.path.abspath(__file__))
path1 = os.path.join(out_dir, "Step1_minimization.csv")
path2 = os.path.join(out_dir, "Step2_pending_access.csv")

step1.to_csv(path1, index=False, encoding="utf-8-sig")
step2.to_csv(path2, index=False, encoding="utf-8-sig")

print("Step 1 rows:", len(step1), "->", path1, "| exists:", os.path.exists(path1))
print("Step 2 rows:", len(step2), "->", path2, "| exists:", os.path.exists(path2))

os.startfile(out_dir)   # opens the folder in Windows Explorer