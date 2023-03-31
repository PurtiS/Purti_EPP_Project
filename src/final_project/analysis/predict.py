"""Functions for predicting outcomes based on the estimated model."""

from psmpy.plotting import *


def run_knn_matched(psm, matcher="propensity_logit", replacement=False, caliper=None):
    """Run k-nearest neighbor (KNN) matching using the specified matcher.

    Args:
        psm (PsmPy): The PsmPy object containing data and matching results.
        matcher (str): The name of the matcher to use. Defaults to "propensity_logit".
        replacement (bool): Whether to allow replacement during matching. Defaults to False.
        caliper (float): The maximum difference in propensity score allowed for matches. Defaults to None.

    Returns:
        PsmPy: The PsmPy object with the matched data.

    """
    return psm.knn_matched(matcher=matcher, replacement=replacement, caliper=caliper)


def get_predicted_data(psm):
    """Get the predicted data for the matched sample.

    Args:
        psm (PsmPy): The PsmPy object containing data and matching results.

    Returns:
        pandas.DataFrame: The predicted data for the matched sample.

    """
    return psm.predicted_data


def matched_df(psm, data):
    """Get the matched dataframe along with outcome variable and personal ID.

    Args:
        psm (PsmPy): The PsmPy object containing data and matching results.
        data (pandas.DataFrame): The filtered dataset.

    Returns:
        pandas.DataFrame: The matched dataframe with the outcome variable.

    """
    df = psm.df_matched
    df = df.merge(data[["pid", "aggregate_loneliness_2017"]], on="pid")
    return df


def predict_att_ate_regression(data, model):
    """Predicts the average treatment effect on the treated (ATT) and average treatment effect (ATE) using a regression model.

    Args:
        data (pandas.DataFrame): The matched dataset.
        model (statsmodels.regression.linear_model.RegressionResultsWrapper): The fitted regression model.

    Returns:
        pandas.DataFrame: A DataFrame containing the ATT and ATE.

    """
    outcome_var = "aggregate_loneliness_2017"
    treatment_var = "went_unemployed"

    att = model.params[treatment_var]

    treated_mean = np.mean(data[data[treatment_var] == 1][outcome_var])
    control_mean = np.mean(data[data[treatment_var] == 0][outcome_var])
    ate = treated_mean - control_mean

    # Return results
    result = pd.DataFrame({"ATT": [att], "ATE": [ate]})

    return result


def get_loneliness_change(matched_data):
    """The funcion takes the matched dataset and finds the difference in the aggregate loneliness levels(2017) of people who had the same aggregate loneliness levels in 2013 but some of them went
    unemployed and the others did not.

    This clearly indicates that when starting with the sme levels of loneliness, those who experience unemployement are more lonely thena those who stayed employed during the same period of time.

    """
    # Create a subset of data for individuals who went unemployed
    unemployed = matched_data[matched_data["went_unemployed"] == 1]

    # Create a subset of data for individuals who did not go unemployed
    not_unemployed = matched_data[matched_data["went_unemployed"] == 0]

    # Group by the initial level of loneliness in 2013 and calculate the mean loneliness change
    agg_loneliness_2013 = matched_data.groupby("aggregate_loneliness_2013").agg(
        {"aggregate_loneliness_2017": "mean"},
    )

    # Merge the unemployment data with the loneliness data
    unemployed_merged = pd.merge(
        agg_loneliness_2013,
        unemployed,
        on="aggregate_loneliness_2013",
        how="inner",
    )
    not_unemployed_merged = pd.merge(
        agg_loneliness_2013,
        not_unemployed,
        on="aggregate_loneliness_2013",
        how="inner",
    )

    # Calculate the change in loneliness between 2013 and 2017 for each group
    unemployed_merged["loneliness_change"] = (
        unemployed_merged["aggregate_loneliness_2017_y"]
        - unemployed_merged["aggregate_loneliness_2013"]
    )
    not_unemployed_merged["loneliness_change"] = (
        not_unemployed_merged["aggregate_loneliness_2017_y"]
        - not_unemployed_merged["aggregate_loneliness_2013"]
    )

    # Calculate the difference in loneliness change between the two groups
    diff = pd.DataFrame(
        {
            unemployed_merged["loneliness_change"].mean()
            - not_unemployed_merged["loneliness_change"].mean(),
        },
    )

    return diff
