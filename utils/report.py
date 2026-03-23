import pandas as pd

def generate_excel(results):
    df = pd.DataFrame(results)

    # Only filter columns if DataFrame is not empty and has the required columns
    required_cols = [
        "test_name",
        "description",
        "username",
        "expected",
        "actual",
        "status"
    ]
    if not df.empty and all(col in df.columns for col in required_cols):
        df = df[required_cols]
    else:
        print("[WARN] No test results or missing columns, skipping report column filtering.")

    df.to_excel("report.xlsx", index=False)