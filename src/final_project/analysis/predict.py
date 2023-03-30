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


def predict_att_ate_regression(data, model):
    # Load regression model from file
    # Compute ATT
    outcome_var = "aggregate_loneliness_2017"
    treatment_var = "went_unemployed"

    att = model.params[treatment_var]

    treated_mean = np.mean(data[data[treatment_var] == 1][outcome_var])
    control_mean = np.mean(data[data[treatment_var] == 0][outcome_var])
    ate = treated_mean - control_mean

    # Return results
    result_dict = {"ATT": [att], "ATE": [ate]}
    result = pd.DataFrame(result_dict, index=[0])

    return result
