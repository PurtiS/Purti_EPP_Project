"""Functions for fitting the regression model."""

from psmpy import PsmPy
from psmpy.plotting import *


def drop_na(df):
    return df.dropna()


def create_psm(df, treatment, indx, exclude):
    return PsmPy(df, treatment=treatment, indx=indx, exclude=exclude)


def run_logistic_ps(psm, balance=False):
    return psm.logistic_ps(balance=balance)
