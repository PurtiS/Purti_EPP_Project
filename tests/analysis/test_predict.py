"""Tests for the prediction model."""

import pandas as pd
import pytest
from psmpy.plotting import *

import src.final_project.analysis.model as model_fn
import src.final_project.analysis.predict as predict_fn
from src.final_project.config import TEST_DIR


@pytest.fixture()
def data():
    test_match_df = pd.read_csv(TEST_DIR / "analysis" / "test_match.csv")
    return test_match_df


def test_predicted_data(data):
    expected_df = pd.DataFrame(
        {
            "marital_status": [1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
            "propensity_score": [
                0.692085,
                0.921919,
                0.790986,
                0.566517,
                0.721278,
                0.592211,
                0.692085,
                0.586988,
                0.288803,
                0.140653,
            ],
        },
    )
    psm = model_fn.create_psm(
        data,
        treatment="went_unemployed",
        indx="pid",
        exclude=["hid", "aggregate_loneliness_2017"],
    )
    model_fn.run_logistic_ps(psm, balance=False)
    output = predict_fn.get_predicted_data(psm).reset_index(drop=True)
    output = output[["marital_status", "propensity_score"]]
    output["propensity_score"] = output["propensity_score"].round(6)
    pd.testing.assert_frame_equal(expected_df, output)


def test_matched_df(data):
    expected_df = pd.DataFrame(
        {
            "marital_status": [1, 1, 1, 0, 0, 1, 0],
            "propensity_score": [
                0.692085,
                0.586988,
                0.288803,
                0.140653,
                0.592211,
                0.566517,
                0.721278,
            ],
            "matched_ID": [2.0, 9.0, 7.0, 8.0, np.nan, np.nan, np.nan],
        },
    )

    psm = model_fn.create_psm(
        data,
        treatment="went_unemployed",
        indx="pid",
        exclude=["hid", "aggregate_loneliness_2017"],
    )
    model_fn.run_logistic_ps(psm, balance=False)
    predict_fn.get_predicted_data(psm).reset_index(drop=True)
    predict_fn.run_knn_matched(
        psm,
        matcher="propensity_score",
        replacement=False,
        caliper=None,
    )
    output = predict_fn.matched_df(psm, data).reset_index(drop=True)
    output = output[["marital_status", "propensity_score", "matched_ID"]]
    output["propensity_score"] = output["propensity_score"].round(6)
    pd.testing.assert_frame_equal(expected_df, output)
