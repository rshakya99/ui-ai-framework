import pandas as pd

def generate_excel(results):
    df = pd.DataFrame(results)

    df = df[[
        "test_name",
        "description",
        "username",
        "expected",
        "actual",
        "status"
    ]]

    df.to_excel("report.xlsx", index=False)