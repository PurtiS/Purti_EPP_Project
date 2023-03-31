"""Functions plotting results."""

import matplotlib.pyplot as plt
from psmpy.plotting import *


def plot_match(psm, title, ylabel, xlabel, names):
    """Plots the match between treatment and control groups for all teh covariates to see the matching quality."""
    psm.plot_match(Title=title, Ylabel=ylabel, Xlabel=xlabel, names=names)


def plot_effect_size(psm):
    """Plots the effect size of covariates that is the standardized difference in means of the covariates between the treatment and control groups, before and after matching has been performed."""
    return psm.effect_size_plot()


def effect_size_table(psm):
    """Returns a table of effect sizes for the matched data."""
    return psm.effect_size


def plot_loneliness_by_unemployment(data):
    """Plot the mean loneliness levels for 2013 and 2017 for those who went unemployed and those who stayed employed during the same period.

    Parameters:
    -----------
    data : pandas.DataFrame
        A DataFrame containing the columns "went_unemployed", "aggregate_loneliness_2013", and "aggregate_loneliness_2017".

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The Figure object that contains the plot.

    """
    unemployed_means = [
        data[data["went_unemployed"] == 1]["aggregate_loneliness_2013"].mean(),
        data[data["went_unemployed"] == 1]["aggregate_loneliness_2017"].mean(),
    ]
    not_unemployed_means = [
        data[data["went_unemployed"] == 0]["aggregate_loneliness_2013"].mean(),
        data[data["went_unemployed"] == 0]["aggregate_loneliness_2017"].mean(),
    ]

    x = [2013, 2017]
    fig, ax = plt.subplots()

    (line1,) = ax.plot(x, unemployed_means, label="Went Unemployed", marker="o")
    (line2,) = ax.plot(x, not_unemployed_means, label="Stayed employed", marker="o")

    ax.set_ylabel("Mean Loneliness Level")
    ax.set_title("Loneliness Levels by Employment Status")
    ax.set_xticks(x)
    ax.legend()

    ax.grid()
    return fig


def plot_loneliness_by_gender_and_employment(data):
    """The function takes a pandas DataFrame data as input and creates a bar chart that shows the mean level of loneliness in 2013 and 2017 for four groups: men who went unemployed, men who stayed
    employed, women who went unemployed, and women who stayed employed.

    The function returns the created figure.

    """
    # Data for men
    men_unemployed_means = [
        data.loc[
            (data["went_unemployed"] == 1) & (data["sex"] == 1),
            "aggregate_loneliness_2013",
        ].mean(),
        data.loc[
            (data["went_unemployed"] == 1) & (data["sex"] == 1),
            "aggregate_loneliness_2017",
        ].mean(),
    ]
    men_not_unemployed_means = [
        data.loc[
            (data["went_unemployed"] == 0) & (data["sex"] == 1),
            "aggregate_loneliness_2013",
        ].mean(),
        data.loc[
            (data["went_unemployed"] == 0) & (data["sex"] == 1),
            "aggregate_loneliness_2017",
        ].mean(),
    ]

    # Data for women
    women_unemployed_means = [
        data.loc[
            (data["went_unemployed"] == 1) & (data["sex"] == 0),
            "aggregate_loneliness_2013",
        ].mean(),
        data.loc[
            (data["went_unemployed"] == 1) & (data["sex"] == 0),
            "aggregate_loneliness_2017",
        ].mean(),
    ]
    women_not_unemployed_means = [
        data.loc[
            (data["went_unemployed"] == 0) & (data["sex"] == 0),
            "aggregate_loneliness_2013",
        ].mean(),
        data.loc[
            (data["went_unemployed"] == 0) & (data["sex"] == 0),
            "aggregate_loneliness_2017",
        ].mean(),
    ]

    labels = ["2013", "2017"]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.bar(
        x - width / 2,
        men_unemployed_means,
        width / 2,
        label="Men: Went Unemployed",
    )
    ax.bar(
        x - width / 4,
        men_not_unemployed_means,
        width / 2,
        label="Men: Stayed employed",
    )
    ax.bar(
        x + width / 4,
        women_unemployed_means,
        width / 2,
        label="Women: Went Unemployed",
    )
    ax.bar(
        x + width / 2,
        women_not_unemployed_means,
        width / 2,
        label="Women: Stayed employed",
    )

    ax.set_ylabel("Loneliness")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Loneliness by employment status and gender")

    ax.legend(loc="lower left", ncol=4)

    return fig


def plot_loneliness_by_marital_status_unemployment(data):
    """This function takes in a pandas DataFrame data and plots the mean loneliness scores for people who went unemployed, grouped by their marital status."""
    married_unemployed_means = [
        data.loc[
            (data["went_unemployed"] == 1)
            & (data["marital_status"] == 1)
            & (data["aggregate_loneliness_2013"].notnull()),
            "aggregate_loneliness_2013",
        ].mean(),
        data.loc[
            (data["went_unemployed"] == 1)
            & (data["marital_status"] == 1)
            & (data["aggregate_loneliness_2017"].notnull()),
            "aggregate_loneliness_2017",
        ].mean(),
    ]

    unmarried_unemployed_means = [
        data.loc[
            (data["went_unemployed"] == 1)
            & (data["marital_status"] == 0)
            & (data["aggregate_loneliness_2013"].notnull()),
            "aggregate_loneliness_2013",
        ].mean(),
        data.loc[
            (data["went_unemployed"] == 1)
            & (data["marital_status"] == 0)
            & (data["aggregate_loneliness_2017"].notnull()),
            "aggregate_loneliness_2017",
        ].mean(),
    ]

    labels = ["2013", "2017"]
    x = np.arange(len(labels))

    fig, ax = plt.subplots()

    ax.plot(x, married_unemployed_means, "-o", label="Married: Went Unemployed")
    ax.plot(x, unmarried_unemployed_means, "-o", label="Unmarried: Went Unemployed")

    ax.set_ylabel("Loneliness")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.title("Loneliness by marital status and unemployment status")

    return fig


def plot_loneliness_by_hh_size(data):
    """This function takes a pandas DataFrame as input and creates a line plot of the difference between aggregate loneliness levels in 2013 and 2017 for individuals in households with more than two
    members (hh_members > 2) versus those in smaller households.

    The function returns the resulting matplotlib figure object.

    """
    data["hh_large"] = (data["hh_members"] > 2).astype(int)

    hh_large_data = data.loc[
        data["hh_large"] == 1,
        ["aggregate_loneliness_2013", "aggregate_loneliness_2017"],
    ]
    hh_small_data = data.loc[
        data["hh_large"] == 0,
        ["aggregate_loneliness_2013", "aggregate_loneliness_2017"],
    ]

    hh_large_means = hh_large_data.mean()
    hh_small_means = hh_small_data.mean()

    fig, ax = plt.subplots()
    ax.plot(hh_large_means.index, hh_large_means.values, label="Household size > 2")
    ax.plot(hh_small_means.index, hh_small_means.values, label="Household size <= 2")

    ax.set_xlabel("Year")
    ax.set_ylabel("Aggregate loneliness")
    ax.set_title("Loneliness by Household Size")
    ax.legend()

    return fig
