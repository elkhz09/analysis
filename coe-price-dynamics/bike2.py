import requests
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def fetch_singstat_table(table_id, search=None, offset=0, limit=500):
    url = f"https://tablebuilder.singstat.gov.sg/api/table/tabledata/{table_id}"
    params = {"offset": offset, "limit": limit}
    if search:
        params["search"] = search
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def clean_colname(s):
    return (
        s.lower()
         .replace(",", "")
         .replace("(", "")
         .replace(")", "")
         .replace("/", "_")
         .replace("-", "_")
         .replace(" ", "_")
    )

def singstat_rows_to_long_df(data):
    records = []
    for row in data["Data"]["row"]:
        for col in row["columns"]:
            records.append({
                "month": col["key"],
                "metric": row["rowText"],
                "value": col["value"]
            })
    df = pd.DataFrame(records)
    df["month"] = pd.to_datetime(df["month"], format="%Y %b", errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df

def extract_motorcycle_series(table_id, value_name):
    data = fetch_singstat_table(table_id, search="motorcycle")
    rows = data["Data"]["row"]
    matched = [r for r in rows if "motorcycle" in r["rowText"].lower()]
    if not matched:
        raise ValueError(f"No motorcycle row found for {table_id}")
    if len(matched) > 1:
        print(f"Multiple motorcycle rows in {table_id}:")
        for r in matched:
            print(r["seriesNo"], "-", r["rowText"])
    row = matched[0]
    records = [{"month": c["key"], value_name: c["value"]} for c in row["columns"]]
    df = pd.DataFrame(records)
    df["month"] = pd.to_datetime(df["month"], format="%Y %b", errors="coerce")
    df[value_name] = pd.to_numeric(df[value_name], errors="coerce")
    return df.sort_values("month").reset_index(drop=True)

# COE motorcycle table
motor_coe_data = fetch_singstat_table("M651121", search="motor")
motor_coe_long = singstat_rows_to_long_df(motor_coe_data)
motor_coe_df = motor_coe_long.pivot(index="month", columns="metric", values="value").reset_index()
motor_coe_df.columns = ["month"] + [clean_colname(c) for c in motor_coe_df.columns[1:]]

# Population / dereg / new reg
motor_pop_df = extract_motorcycle_series("M650341", "motorcycle_population")   # swap to M650271 if needed
motor_dereg_df = extract_motorcycle_series("M650291", "motorcycle_deregistrations")
motor_newreg_df = extract_motorcycle_series("M650281", "motorcycle_new_registrations")

# Merge
master_df = (
    motor_coe_df
    .merge(motor_pop_df, on="month", how="outer")
    .merge(motor_dereg_df, on="month", how="outer")
    .merge(motor_newreg_df, on="month", how="outer")
    .sort_values("month")
    .reset_index(drop=True)
)

print(master_df.head())