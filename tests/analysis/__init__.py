"""Tests for the analysis module."""
from tests.analysis.test_model import test_fit_regression_model
from tests.analysis.test_predict import test_matched_df, test_predicted_data

__all__ = test_fit_regression_model, test_predicted_data, test_matched_df
