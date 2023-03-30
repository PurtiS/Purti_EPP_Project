"""Functions for cleaning the data sets."""

import warnings

import numpy as np
import pandas as pd

warnings.simplefilter(action="ignore", category=FutureWarning)


def filter_by_year(df, year):
    df = df.copy()
    df.loc[:, "syear"] = pd.to_numeric(df["syear"], errors="coerce")
    df = df.loc[df["syear"] == year]
    return df


def replace_invalid_responses(df, column, data_type):
    unconsiderable = [
        "[-1] keine Angabe",
        "[-2] trifft nicht zu",
        "[-3] nicht valide",
        "[-4] unzulaessige Mehrfachantwort",
        "[-5] in Fragebogenversion nicht enthalten",
        "[-6] Fragebogenversion mit geaenderter Filterfuehrung",
        "[-8] Frage in diesem Jahr nicht Teil des Frageprogramms",
    ]
    df = df.copy()
    df[column] = df[column].replace(unconsiderable, np.nan)

    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in DataFrame.")

    # Convert data type
    if data_type == "int":
        df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
    elif data_type == "float":
        df[column] = pd.to_numeric(df[column], errors="coerce").astype("float")
    elif data_type == "category":
        df[column] = df[column].astype("category")
    else:
        raise ValueError("Invalid data type. Must be 'int', 'float', or 'category'.")
    return df


def pgen_treatment(df):
    df = df.copy()
    df = replace_invalid_responses(df, "pgexpue", "float")
    df_start = filter_by_year(df, 2013)
    df_end = filter_by_year(df, 2017)

    df_final = df_start.merge(
        df_end,
        on=["pid", "hid"],
        suffixes=("_2013", "_2017"),
        how="left",
    )
    df_final["pgen_treatment"] = df_final["pgexpue_2017"] - df_final["pgexpue_2013"]
    df_final["went_unemployed"] = df_final["pgen_treatment"].apply(
        lambda x: 1 if x >= 1 else 0,
    )
    df_final = df_final[["pid", "went_unemployed", "hid"]]

    df_final = df_final.sort_index()
    return df_final


def ppath_functions(df):
    df = df[["pid", "sex", "gebjahr"]]
    df_copy = df.copy()
    df_copy.loc[:, "sex"] = np.where(df_copy["sex"] == "[1] maennlich", 1, 0)
    df_copy.loc[:, "age"] = 2013.0 - df_copy["gebjahr"]
    df_copy = df_copy[df_copy["age"] >= 22]
    df_copy = df_copy[df_copy["age"] <= 64]
    df_copy = df_copy[["age", "pid", "sex"]]
    return df_copy


def pl_subfunction(df):
    df = df.copy()
    df = df.rename(
        columns={
            "ple0008": "health",
            "plj0587": "Company_missing",
            "plj0588": "Feeling_left_out",
            "plj0589": "socially_isolated",
        },
    )
    df = replace_invalid_responses(df, "health", "category")
    df = replace_invalid_responses(df, "Company_missing", "category")
    df = replace_invalid_responses(df, "Feeling_left_out", "category")
    df = replace_invalid_responses(df, "socially_isolated", "category")
    return df


def replace_categorical_values(df, column, mapping):
    df = df.copy()
    # Convert column to string if a list is passed
    df[column] = df[column].replace(mapping)
    df[column] = df[column].astype("float")
    return df


# Define the mapping of old values to new values for each column
mapping1 = {
    "[1] Sehr oft": "5",
    "[2] Oft": "4",
    "[3] Manchmal": "3",
    "[4] Selten": "2",
    "[5] Nie": "1",
}

mapping2 = {
    "[1] Sehr gut": "1",
    "[2] Gut": "2",
    "[3] Zufriedenstellend": "3",
    "[4] Weniger gut": "4",
    "[5] Schlecht": "5",
}

# Define the name of the columns to replace
column_to_replace1 = ["Company_missing", "Feeling_left_out", "socially_isolated"]
column_to_replace2 = ["health"]


# Apply the function to replace the old categorical values with the new categorical values
def pl_functions(df):
    df = df[["pid", "ple0008", "plj0587", "plj0588", "plj0589", "syear", "hid"]]
    df = df.copy()
    df = pl_subfunction(df)
    df = replace_categorical_values(df, column=column_to_replace1, mapping=mapping1)
    df = replace_categorical_values(df, column=column_to_replace2, mapping=mapping2)
    cols = ["Company_missing", "Feeling_left_out", "socially_isolated"]
    df["aggregate_loneliness"] = df[cols].mean(axis=1)
    loneliness_2013 = filter_by_year(df, 2013)
    loneliness_2017 = filter_by_year(df, 2017)
    df_merge = loneliness_2013.merge(
        loneliness_2017,
        on=["pid", "hid"],
        suffixes=["_2013", "_2017"],
    )
    df_merge = df_merge[
        [
            "pid",
            "hid",
            "aggregate_loneliness_2013",
            "aggregate_loneliness_2017",
            "health_2013",
        ]
    ]
    return df_merge


def pgen_covariates(df):
    df = df.copy()
    df = filter_by_year(df, 2013)
    df = replace_invalid_responses(df, "pgfamstd", "category")
    df["marital_status"] = np.where(
        df["pgfamstd"] == "[1] Verheiratet, mit Ehepartner zusammenlebend",
        1,
        0,
    )
    df = df.loc[df["pgemplst"] == "[1] Voll erwerbstätig"]
    df = replace_invalid_responses(df, "pgbilzeit", "float")
    df = df.rename(columns={"pgbilzeit": "education"})
    df = df[["marital_status", "education", "pid", "hid"]]
    return df


def hgen_functions(df):
    df = df[["hid", "hgi1hinc", "syear"]]
    df = df.copy()
    df = filter_by_year(df, 2013)
    df = df.rename(columns={"hgi1hinc": "hh_income"})
    df = replace_invalid_responses(df, "hh_income", "float")
    df = df[["hid", "hh_income"]]
    return df


def hbrutto_functions(df):
    df = df[["hid", "syear", "hhgr"]]
    df = df.copy()
    df = filter_by_year(df, 2013)
    df = df.rename(columns={"hhgr": "hh_members"})
    df = replace_invalid_responses(df, "hh_members", "float")
    df = df[["hid", "hh_members"]]
    return df


def clean_data(df1, df_2013, df5, df6, df7, df8):
    df1 = pgen_treatment(df1)
    df6 = pl_functions(df6)
    df_2013 = pgen_covariates(df_2013)
    df5 = ppath_functions(df5)
    df7 = hgen_functions(df7)
    df8 = hbrutto_functions(df8)

    df1 = df1.merge(df5, on="pid")
    df7 = df7.merge(df8, on="hid")
    df1 = df1.merge(df_2013, on=["pid", "hid"])
    df1 = df1.merge(df6, on=["pid", "hid"])
    df1 = df1.merge(df7, on="hid")
    return df1
