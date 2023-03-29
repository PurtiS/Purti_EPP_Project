"""Functions for predicting outcomes based on the estimated model."""

from psmpy.plotting import *


def run_knn_matched(psm, matcher="propensity_logit", replacement=False, caliper=None):
    return psm.knn_matched(matcher=matcher, replacement=replacement, caliper=caliper)


def get_predicted_data(psm):
    return psm.predicted_data


def matched_df(psm, data):
    df = psm.df_matched
    df = df.merge(data[["pid", "aggregate_loneliness_2017"]], on="pid")
    return df
