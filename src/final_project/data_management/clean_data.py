"""Functions for cleaning the data sets."""

import warnings

import numpy as np
import pandas as pd

warnings.simplefilter(action="ignore", category=FutureWarning)


def filter_by_year(df, year):
    """Filters a DataFrame by the given year, using the 'syear' column.

    Args:
        df (pandas.DataFrame): The DataFrame to filter.
        year (int): The year to filter by.

    Returns:
        pandas.DataFrame: The filtered DataFrame.

    """
    df = df.copy()
    df.loc[:, "syear"] = pd.to_numeric(df["syear"], errors="coerce")
    df = df.loc[df["syear"] == year]
    return df


def replace_invalid_responses(df, column, data_type):
    """Replaces invalid or unconsiderable responses in a DataFrame column with NaN values, and converts the data type of the column to the specified data type.

    Args:
        df (pandas.DataFrame): The DataFrame to modify.
        column (str): The name of the column to modify.
        data_type (str): The desired data type of the column. Must be 'int', 'float', or 'category'.

    Returns:
        pandas.DataFrame: The modified DataFrame.

    Raises:
        ValueError: If the specified column does not exist in the DataFrame, or if the specified data
                    type is not 'int', 'float', or 'category'.

    """
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
    """Calculates the unemployment duration between 2013-2017 using "pgexpue" variable in the pgen Dataset(input dataframe), and creates a new variable indicating whether the respondent went
    unemployed during that period which is the treatment variable.

    Args:
        df (pandas.DataFrame): The DataFrame to modify- pgen Dataset.

    Returns:
        pandas.DataFrame: A new DataFrame containing the following columns: 'pid', 'went_unemployed',
                           and 'hid'.

    Raises:
        ValueError: If the 'pgexpue' column does not exist in the DataFrame.

    """
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
    df_final["unemp_duration"] = df_final["pgexpue_2017"] - df_final["pgexpue_2013"]
    df_final["went_unemployed"] = df_final["unemp_duration"].apply(
        lambda x: 1 if x >= 1 else 0,
    )
    df_final = df_final[["pid", "went_unemployed", "hid"]]

    df_final = df_final.sort_index()
    return df_final


def ppath_functions(df):
    """Creates a new DataFrame containing information on the respondents' age, sex, and pid (personal ID),.

    based on the columns - year of birth and sex in the ppath Dataset(input dataframe).

    Args:
        df (pandas.DataFrame): The DataFrame to modify -ppath Dataset.

    Returns:
        pandas.DataFrame: A new DataFrame containing the following columns: 'age', 'pid', 'sex'.

    """
    df = df[["pid", "sex", "gebjahr"]]
    df_copy = df.copy()
    df_copy.loc[:, "sex"] = np.where(df_copy["sex"] == "[1] maennlich", 1, 0)
    df_copy.loc[:, "age"] = 2013.0 - df_copy["gebjahr"]
    df_copy = df_copy[df_copy["age"] >= 22]
    df_copy = df_copy[df_copy["age"] <= 64]
    df_copy = df_copy[["age", "pid", "sex"]]
    return df_copy


def pl_subfunction(df):
    """Modifies a DataFrame by renaming specific columns and replacing invalid responses in certain columns of pl Dataset, the function is used as a subfunction later.

    Args:
        df (pandas.DataFrame): The DataFrame to modify.

    Returns:
        pandas.DataFrame: A modified DataFrame with the following column names:
        'health', 'Company_missing', 'Feeling_left_out', and 'socially_isolated'.
        Invalid responses in these columns are replaced with NaN values.

    """
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
    """Replaces categorical values in a pandas DataFrame column with numeric values.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        column (str): The name of the column to replace values in.
        mapping (dict): A dictionary mapping old values to new values.

    Returns:
        pandas.DataFrame: A copy of the input DataFrame with the specified column's categorical values replaced with numeric values.

    """
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


def pl_functions(df):
    """The function calculates aggregate loneliness from three different indicators of loneliness, maps these indicators along with health to numerical values. It takes the aggregate loneliness from
    2013 and 2017 and health indicator 2013 from pl dataset of SOEP.

    Args:
        df (pandas.DataFrame): A DataFrame - pl Dataset, containing the following columns:
            - pid (int): Personal ID
            - ple0008 (str): Self-rated health status
            - plj0587 (str): Missing company
            - plj0588 (str): Feeling left out
            - plj0589 (str): Social isolation
            - syear (int): Survey year
            - hid (int): Household ID

    Returns:
        pandas.DataFrame: A DataFrame with the following columns:
            - pid (int): Personal ID
            - hid (int): Household ID
            - aggregate_loneliness_2013 (float): Average of plj0587, plj0588, and plj0589 in 2013
            - aggregate_loneliness_2017 (float): Average of plj0587, plj0588, and plj0589 in 2017
            - health_2013 (float): Self-rated health status in 2013, mapped to a scale from 1 to 5

    """
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
    """Function applied on pgen Dataset of SOEP to generate covariates for Propensity score matching to find the effect of employment on loneliness. It filters out only employed people from 2013,
    their marital status and years of education.

    Args:
    df (pandas.DataFrame): Input DataFrame containing the necessary variables.

    Returns:
    pandas.DataFrame: A DataFrame containing the following variables:
    - marital_status: A binary variable indicating whether the individual is married and living with their spouse (1) or not (0).
    - education: The number of years of education.
    - pid: The personal ID.
    - hid: The household ID.

    """
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
    """Processes the household income data from the hgen dataset of SOEP and returns a dataframe with the household ID and income information for the year 2013.

    Args:
        df (pandas.DataFrame): hgen Dataset(Input Dataframe) containing household income data
            from the SOEP dataset.

    Returns:
    pandas.DataFrame: A DataFrame containing the following variables:
        hid : Household ID.
        hh_income : Income of households from 2013.

    """
    df = df[["hid", "hgi1hinc", "syear"]]
    df = df.copy()
    df = filter_by_year(df, 2013)
    df = df.rename(columns={"hgi1hinc": "hh_income"})
    df = replace_invalid_responses(df, "hh_income", "float")
    df = df[["hid", "hh_income"]]
    return df


def hbrutto_functions(df):
    """Processes the household members data from the hbrutto dataset of SOEP and returns a dataframe with the household ID and number of members in the household for the year 2013.

    Args:
        df (pandas.DataFrame): The input dataframe- Hbrutto Dataset from SOEP
         containing the original household data.

    Returns:
        pandas.DataFrame: A new dataframe containing the household id and the number of household members.

    """
    df = df[["hid", "syear", "hhgr"]]
    df = df.copy()
    df = filter_by_year(df, 2013)
    df = df.rename(columns={"hhgr": "hh_members"})
    df = replace_invalid_responses(df, "hh_members", "float")
    df = df[["hid", "hh_members"]]
    return df


def data_clean(pgen_treat_df, pgen_cov_df, ppath_df, pl_df, hgen_df, hbrutto_df):
    """Perform cleaning and preprocessing on each of the SOEP datasets and merging them on Personal ID and / or Household ID."""
    df1 = pgen_treatment(pgen_treat_df)
    df2 = pl_functions(pl_df)
    df3 = pgen_covariates(pgen_cov_df)
    df4 = ppath_functions(ppath_df)
    df5 = hgen_functions(hgen_df)
    df6 = hbrutto_functions(hbrutto_df)

    df1 = df1.merge(df4, on="pid")
    df5 = df5.merge(df6, on="hid")
    df1 = df1.merge(df3, on=["pid", "hid"])
    df1 = df1.merge(df2, on=["pid", "hid"])
    df1 = df1.merge(df5, on="hid")
    return df1
