import numpy as np
import pandas as pd
import pytest

import src.final_project.data_management.clean_data as cleaned_fn
from src.final_project.config import TEST_DIR

# All the functions are tested on sample dataset Test_fn.csv


@pytest.fixture()
def data():
    test_df = pd.read_csv(
        TEST_DIR / "data_management" / "Test_fn.csv",
        encoding="iso-8859-1",
    )
    return test_df


def test_filter_by_year(data):
    df = cleaned_fn.filter_by_year(data, 2013)
    # check that the filtered dataframe has only rows for the specified year
    assert np.all(df["syear"] == 2013)


def test_replace_invalid_responses(data):
    # create sample dataframe
    df = cleaned_fn.replace_invalid_responses(data, "pgexpue", "int")

    # check if the invalid responses are replaced and the data type is converted correctly
    expected_value = [3, 3, 3, 3, np.nan, 4, 1, np.nan, 3, np.nan, 0, 0]
    expected_series = pd.Series(expected_value, dtype="Int64", name="pgexpue")
    pd.testing.assert_series_equal(df["pgexpue"], expected_series, check_dtype=False)


def test_pgen_treatment(data):
    expected_output = pd.DataFrame(
        {"pid": [1, 2, 3, 4], "went_unemployed": [0, 1, 1, 0], "hid": [5, 6, 7, 8]},
    )
    output = cleaned_fn.pgen_treatment(data)
    pd.testing.assert_frame_equal(output, expected_output)


def test_ppath_functions(data):
    expected_output = pd.DataFrame(
        {
            "age": [28.0, 28.0, 28.0, 28.0, 28.0, 28.0, 34.0, 34.0, 34.0],
            "pid": [1, 1, 1, 2, 2, 2, 4, 4, 4],
            "sex": [1, 1, 1, 1, 1, 1, 0, 0, 0],
        },
    )
    expected_output["sex"] = expected_output["sex"].astype("int32")
    expected_output = expected_output.reset_index(drop=True)
    output = cleaned_fn.ppath_functions(data)
    output = output.sort_values(by=["pid", "age"]).reset_index(drop=True)
    pd.testing.assert_frame_equal(output, expected_output)


def test_pl_functions(data):
    # Define the expected output dataframe
    expected_output = pd.DataFrame(
        {
            "pid": [1, 2, 3, 4],
            "hid": [5, 6, 7, 8],
            "aggregate_loneliness_2013": [3.333333, 3.333333, 3.000000, 2.333333],
            "aggregate_loneliness_2017": [1.666667, 5.000000, 4.500000, 2.000000],
            "health_2013": [1.0, 1.0, np.nan, 3.0],
        },
    )

    output = cleaned_fn.pl_functions(data)
    output = output.reset_index(drop=True)
    # Check if the output matches the expected output
    pd.testing.assert_frame_equal(output, expected_output)


def test_pgen_covariates(data):
    expected_output = pd.DataFrame(
        {
            "marital_status": [1, 1],
            "education": [7.0, 7.0],
            "pid": [1, 2],
            "hid": [5, 6],
        },
    )
    expected_output["marital_status"] = expected_output["marital_status"].astype(
        "int32",
    )
    output = cleaned_fn.pgen_covariates(data)
    output = output.reset_index(drop=True)
    # Check if the output matches the expected output
    pd.testing.assert_frame_equal(output, expected_output)


def test_hgen_functions(data):
    expected_output = pd.DataFrame(
        {"hid": [5, 6, 7, 8], "hh_income": [7000.0, 7000.0, 3400.0, 5000.0]},
    )
    output = cleaned_fn.hgen_functions(data)
    output = output.reset_index(drop=True)
    # Check if the output matches the expected output
    pd.testing.assert_frame_equal(output, expected_output)


def test_hbrutto_functions(data):
    expected_output = pd.DataFrame(
        {"hid": [5, 6, 7, 8], "hh_members": [2.0, 2.0, 3.0, np.nan]},
    )
    output = cleaned_fn.hbrutto_functions(data)
    output = output.reset_index(drop=True)
    # Check if the output matches the expected output
    pd.testing.assert_frame_equal(output, expected_output)
