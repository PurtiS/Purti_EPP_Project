"""Tests for the regression model."""

import final_project.analysis.model as model_fn
import numpy as np
import pandas as pd
import statsmodels.api as sm


def test_fit_regression_model():
    # Generate random data for testing
    np.random.seed(123)
    data = pd.DataFrame(
        {
            "aggregate_loneliness_2017": np.random.normal(size=100),
            "went_unemployed": np.random.binomial(n=1, p=0.5, size=100),
            "age": np.random.normal(loc=40, scale=10, size=100),
            "sex": np.random.binomial(n=1, p=0.5, size=100),
            "education": np.random.choice(
                ["High school", "College", "Graduate"],
                size=100,
            ),
            "marital_status": np.random.binomial(n=1, p=0.5, size=100),
            "aggregate_loneliness_2013": np.random.normal(size=100),
            "hh_members": np.random.randint(low=1, high=5, size=100),
            "hh_income": np.random.normal(loc=50000, scale=10000, size=100),
        },
    )

    # Fit regression model
    model = model_fn.fit_regression_model(data)

    # Test that the model was fit successfully
    assert isinstance(model, sm.regression.linear_model.RegressionResultsWrapper)

    # Test that the model contains the expected variables
    expected_vars = [
        "Intercept",
        "went_unemployed",
        "age",
        "sex",
        "education[T.Graduate]",
        "education[T.High school]",
        "marital_status",
        "aggregate_loneliness_2013",
        "hh_members",
        "hh_income",
    ]
    assert all(var in model.params.index for var in expected_vars)

    # Test that the model has non-null coefficients for all variables
    assert model.params.notnull().all()
