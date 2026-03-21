from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from pathlib import Path
import time
from typing import Iterable

import numpy as np
import pandas as pd
import requests


DATA_GOV_API = "https://data.gov.sg/api/action/datastore_search"
CACHE_DIR = Path(__file__).resolve().parent / ".cache"
_RESOURCE_CACHE: dict[str, pd.DataFrame] = {}
_LAST_REQUEST_AT = 0.0


@dataclass(frozen=True)
class TableSource:
    table_id: str
    resource_id: str
    title: str
    singstat_url: str
    datagov_url: str
    prefer_api: bool = False


TABLE_SOURCES: dict[str, TableSource] = {
    "M651121": TableSource(
        table_id="M651121",
        resource_id="d_22094bf608253d36c0c63b52d852dd6e",
        title="Motor Vehicle Quota, Quota Premium and Prevailing Quota Premium, Monthly",
        singstat_url="https://tablebuilder.singstat.gov.sg/table/TS/M651121",
        datagov_url=(
            "https://data.gov.sg/datasets/d_22094bf608253d36c0c63b52d852dd6e/"
            "view"
        ),
        prefer_api=True,
    ),
    "M650341": TableSource(
        table_id="M650341",
        resource_id="d_ede1a559013d10f234d209ac5e9fd9b4",
        title="Motor Vehicle Population Under Vehicle Quota System, Monthly",
        singstat_url="https://tablebuilder.singstat.gov.sg/table/TS/M650341",
        datagov_url=(
            "https://data.gov.sg/datasets/d_ede1a559013d10f234d209ac5e9fd9b4/"
            "view"
        ),
    ),
    "M650291": TableSource(
        table_id="M650291",
        resource_id="d_d520d6034b5e0c4f883b4e480de28f97",
        title="Motor Vehicles De-Registered Under Vehicle Quota System, Monthly",
        singstat_url="https://tablebuilder.singstat.gov.sg/table/TS/M650291",
        datagov_url=(
            "https://data.gov.sg/datasets/d_d520d6034b5e0c4f883b4e480de28f97/"
            "view"
        ),
    ),
    "M650281": TableSource(
        table_id="M650281",
        resource_id="d_529752a3d78beb78bd4f38e3be37f1b6",
        title="New Registration Of Motor Vehicles Under Vehicle Quota System, Monthly",
        singstat_url="https://tablebuilder.singstat.gov.sg/table/TS/M650281",
        datagov_url=(
            "https://data.gov.sg/datasets/d_529752a3d78beb78bd4f38e3be37f1b6/"
            "view"
        ),
    ),
}


def fetch_datagov_resource(
    resource_id: str,
    timeout: int = 30,
    max_retries: int = 4,
    retry_wait_seconds: int = 15,
    min_interval_seconds: int = 12,
) -> pd.DataFrame:
    source = next(
        (table_source for table_source in TABLE_SOURCES.values() if table_source.resource_id == resource_id),
        None,
    )

    global _LAST_REQUEST_AT

    if resource_id in _RESOURCE_CACHE:
        return _RESOURCE_CACHE[resource_id].copy()

    cache_path = _get_cache_path(resource_id)
    if cache_path.exists():
        cached_df = pd.read_csv(cache_path, dtype=str)
        _RESOURCE_CACHE[resource_id] = cached_df.copy()
        return cached_df

    if source is not None and not source.prefer_api:
        try:
            result_df = _fetch_datagov_html_resource(source=source, timeout=timeout)
            _persist_resource_cache(resource_id=resource_id, df=result_df)
            _RESOURCE_CACHE[resource_id] = result_df.copy()
            return result_df
        except Exception:
            pass

    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            elapsed = time.time() - _LAST_REQUEST_AT
            if elapsed < min_interval_seconds:
                time.sleep(min_interval_seconds - elapsed)

            response = requests.get(
                DATA_GOV_API,
                params={"resource_id": resource_id},
                timeout=timeout,
            )
            _LAST_REQUEST_AT = time.time()
            response.raise_for_status()

            payload = response.json()
            if not payload.get("success"):
                raise ValueError(
                    f"data.gov.sg returned an unsuccessful response: {payload}"
                )

            records = payload["result"]["records"]
            result_df = pd.DataFrame.from_records(records)
            _persist_resource_cache(resource_id=resource_id, df=result_df)
            _RESOURCE_CACHE[resource_id] = result_df.copy()
            return result_df
        except requests.HTTPError as error:
            last_error = error
            status_code = error.response.status_code if error.response is not None else None
            if status_code != 429 or attempt == max_retries - 1:
                raise
            time.sleep(retry_wait_seconds)

    if last_error is not None:
        raise last_error

    raise RuntimeError("Failed to fetch data.gov.sg resource for an unknown reason.")


def _fetch_datagov_html_resource(source: TableSource, timeout: int = 30) -> pd.DataFrame:
    response = requests.get(source.datagov_url, timeout=timeout)
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))
    if not tables:
        raise ValueError(f"No HTML tables were found at {source.datagov_url}")

    data_df = tables[0].copy()
    cleaned_columns = []
    for column in data_df.columns:
        cleaned = (
            str(column)
            .replace("Text", "")
            .replace("Numeric", "")
            .strip()
        )
        if cleaned == "Data Series":
            cleaned = "DataSeries"
        cleaned_columns.append(cleaned)

    data_df.columns = cleaned_columns
    data_df = data_df.loc[
        ~data_df["DataSeries"].astype(str).str.contains(r"^\(Null\)", case=False, regex=True)
    ].copy()
    data_df = data_df.reset_index(drop=True)
    data_df.insert(0, "_id", range(1, len(data_df) + 1))

    return data_df


def _get_cache_path(resource_id: str) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    return CACHE_DIR / f"{resource_id}.csv"


def _persist_resource_cache(resource_id: str, df: pd.DataFrame) -> None:
    cache_path = _get_cache_path(resource_id)
    df.to_csv(cache_path, index=False)


def describe_source_tables() -> pd.DataFrame:
    rows = [
        {
            "table_id": source.table_id,
            "resource_id": source.resource_id,
            "title": source.title,
            "singstat_url": source.singstat_url,
            "datagov_url": source.datagov_url,
        }
        for source in TABLE_SOURCES.values()
    ]
    return pd.DataFrame(rows).sort_values("table_id").reset_index(drop=True)


def _normalise_series(values: pd.Series) -> pd.Series:
    return values.astype(str).str.replace(r"\s+", " ", regex=True).str.strip()


def _melt_monthly_wide_table(df: pd.DataFrame) -> pd.DataFrame:
    id_vars = [column for column in ["_id", "DataSeries"] if column in df.columns]
    month_columns = [column for column in df.columns if column not in id_vars]

    long_df = df.melt(
        id_vars=id_vars,
        value_vars=month_columns,
        var_name="month",
        value_name="value",
    )
    long_df["month"] = pd.to_datetime(long_df["month"], format="%Y%b", errors="coerce")
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")
    long_df["DataSeries"] = _normalise_series(long_df["DataSeries"])

    return (
        long_df.dropna(subset=["month"])
        .sort_values(["month", "DataSeries"])
        .reset_index(drop=True)
    )


def _is_motorcycle_series(values: pd.Series) -> pd.Series:
    series = _normalise_series(values).str.lower()
    return (
        series.str.contains("motorcycle", regex=False)
        | series.str.contains("motorcycles & scooters", regex=False)
        | series.str.contains(r"\bcategory d\b", regex=True)
    )


def _extract_single_motorcycle_series(
    table_id: str,
    value_column: str,
) -> pd.DataFrame:
    source = TABLE_SOURCES[table_id]
    raw_df = fetch_datagov_resource(source.resource_id)
    long_df = _melt_monthly_wide_table(raw_df)
    motorcycle_df = long_df.loc[_is_motorcycle_series(long_df["DataSeries"])].copy()

    monthly_df = (
        motorcycle_df.groupby("month", as_index=False)["value"]
        .sum(min_count=1)
        .rename(columns={"value": value_column})
    )

    monthly_df["table_id"] = table_id
    return monthly_df[["month", value_column, "table_id"]]


def extract_motorcycle_coe_bidding_df() -> pd.DataFrame:
    source = TABLE_SOURCES["M651121"]
    raw_df = fetch_datagov_resource(source.resource_id)
    long_df = _melt_monthly_wide_table(raw_df)
    motorcycle_df = long_df.loc[_is_motorcycle_series(long_df["DataSeries"])].copy()

    series_text = motorcycle_df["DataSeries"].str.lower()
    motorcycle_df["bidding"] = np.select(
        [
            series_text.str.contains("1st bidding", regex=False),
            series_text.str.contains("2nd bidding", regex=False),
        ],
        [1, 2],
        default=np.nan,
    )
    motorcycle_df["metric"] = np.select(
        [
            series_text.str.contains("prevailing quota premium", regex=False),
            series_text.str.contains("quota premium", regex=False),
            series_text.str.contains("successful bids", regex=False),
            series_text.str.contains("bids received", regex=False),
            series_text.str.contains("quota", regex=False)
            & ~series_text.str.contains("premium", regex=False),
        ],
        [
            "prevailing_quota_premium",
            "quota_premium",
            "successful_bids",
            "bids_received",
            "quota",
        ],
        default=np.nan,
    )

    motorcycle_df = motorcycle_df.dropna(subset=["metric", "bidding"]).copy()
    motorcycle_df["bidding"] = motorcycle_df["bidding"].astype("Int64")

    tidy_df = (
        motorcycle_df.pivot_table(
            index=["month", "bidding"],
            columns="metric",
            values="value",
            aggfunc="first",
        )
        .reset_index()
        .sort_values(["month", "bidding"])
        .reset_index(drop=True)
    )

    tidy_df.columns.name = None
    tidy_df["table_id"] = "M651121"

    column_order = [
        "month",
        "bidding",
        "quota",
        "bids_received",
        "successful_bids",
        "quota_premium",
        "prevailing_quota_premium",
        "table_id",
    ]
    existing_columns = [column for column in column_order if column in tidy_df.columns]
    return tidy_df[existing_columns]


def _flatten_columns(columns: Iterable[tuple[str, str]]) -> list[str]:
    flattened = []
    for metric, bidding_label in columns:
        flattened.append(f"{metric}_{bidding_label}_bidding")
    return flattened


def _build_coe_monthly_wide_df(coe_bidding_df: pd.DataFrame) -> pd.DataFrame:
    working_df = coe_bidding_df.copy()
    working_df["bidding_label"] = working_df["bidding"].map({1: "first", 2: "second"})

    metric_columns = [
        "quota",
        "bids_received",
        "successful_bids",
        "quota_premium",
        "prevailing_quota_premium",
    ]
    wide_df = working_df.pivot(
        index="month",
        columns="bidding_label",
        values=metric_columns,
    )
    wide_df.columns = _flatten_columns(wide_df.columns)
    wide_df = wide_df.reset_index().sort_values("month").reset_index(drop=True)

    for metric in ["quota", "bids_received", "successful_bids"]:
        component_columns = [
            f"{metric}_first_bidding",
            f"{metric}_second_bidding",
        ]
        present_columns = [column for column in component_columns if column in wide_df.columns]
        if present_columns:
            wide_df[f"{metric}_total"] = wide_df[present_columns].sum(
                axis=1,
                min_count=1,
            )

    for metric in ["quota_premium", "prevailing_quota_premium"]:
        component_columns = [
            f"{metric}_first_bidding",
            f"{metric}_second_bidding",
        ]
        present_columns = [column for column in component_columns if column in wide_df.columns]
        if present_columns:
            wide_df[f"{metric}_average"] = wide_df[present_columns].mean(axis=1)

    return wide_df


def build_motorcycle_monthly_dataframe() -> pd.DataFrame:
    coe_bidding_df = extract_motorcycle_coe_bidding_df()
    coe_monthly_df = _build_coe_monthly_wide_df(coe_bidding_df)

    population_df = _extract_single_motorcycle_series(
        table_id="M650341",
        value_column="motorcycle_population_under_vqs",
    ).drop(columns="table_id")
    dereg_df = _extract_single_motorcycle_series(
        table_id="M650291",
        value_column="motorcycle_deregistered",
    ).drop(columns="table_id")
    new_reg_df = _extract_single_motorcycle_series(
        table_id="M650281",
        value_column="motorcycle_new_registrations",
    ).drop(columns="table_id")

    bike_df = (
        coe_monthly_df.merge(population_df, on="month", how="outer")
        .merge(dereg_df, on="month", how="outer")
        .merge(new_reg_df, on="month", how="outer")
        .sort_values("month")
        .reset_index(drop=True)
    )
    bike_df["motorcycle_net_registrations"] = (
        bike_df["motorcycle_new_registrations"] - bike_df["motorcycle_deregistered"]
    )

    numeric_columns = [
        column
        for column in bike_df.columns
        if column != "month"
    ]
    bike_df[numeric_columns] = bike_df[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce",
    )

    preferred_order = [
        "month",
        "quota_first_bidding",
        "quota_second_bidding",
        "quota_total",
        "bids_received_first_bidding",
        "bids_received_second_bidding",
        "bids_received_total",
        "successful_bids_first_bidding",
        "successful_bids_second_bidding",
        "successful_bids_total",
        "quota_premium_first_bidding",
        "quota_premium_second_bidding",
        "quota_premium_average",
        "prevailing_quota_premium_first_bidding",
        "prevailing_quota_premium_second_bidding",
        "prevailing_quota_premium_average",
        "motorcycle_population_under_vqs",
        "motorcycle_new_registrations",
        "motorcycle_deregistered",
        "motorcycle_net_registrations",
    ]
    existing_columns = [column for column in preferred_order if column in bike_df.columns]
    remaining_columns = [column for column in bike_df.columns if column not in existing_columns]
    return bike_df[existing_columns + remaining_columns]


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 180)

    motorcycle_coe_bidding_df = extract_motorcycle_coe_bidding_df()
    bike_df = build_motorcycle_monthly_dataframe()

    print("Motorcycle COE bidding-level dataframe")
    print(motorcycle_coe_bidding_df.head(12).to_string(index=False))
    print()
    print("Motorcycle monthly dataframe")
    print(bike_df.head(12).to_string(index=False))
