"""Functions for fitting the regression model."""

import statsmodels.api as sm
from psmpy import PsmPy
from psmpy.plotting import *
from statsmodels.iolib.smpickle import load_pickle


def drop_na(df):
    return df.dropna()


def create_psm(df, treatment, indx, exclude):
    return PsmPy(df, treatment=treatment, indx=indx, exclude=exclude)


def run_logistic_ps(psm, balance=False):
    return psm.logistic_ps(balance=balance)


def fit_regression_model(data):
    # Define regression formula
    outcome_var = "aggregate_loneliness_2017"
    treatment_var = "went_unemployed"
    covariates = (
        "age",
        "sex",
        "education",
        "marital_status",
        "aggregate_loneliness_2013",
        "hh_members",
        "hh_income",
    )
    regression_formula = (
        outcome_var + " ~ " + treatment_var + " + " + " + ".join(covariates)
    )

    # Fit regression model
    regression_result = sm.OLS.from_formula(regression_formula, data=data).fit()

    return regression_result


def load_model(path):
    return load_pickle(path)
