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


def plot_loneliness_by_employment(data):
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
    # Subset the data for people who went unemployed and those who did not
    unemployed_means = [
        data[data["went_unemployed"] == 1]["aggregate_loneliness_2013"].mean(),
        data[data["went_unemployed"] == 1]["aggregate_loneliness_2017"].mean(),
    ]
    not_unemployed_means = [
        data[data["went_unemployed"] == 0]["aggregate_loneliness_2013"].mean(),
        data[data["went_unemployed"] == 0]["aggregate_loneliness_2017"].mean(),
    ]

    # Create a line plot to compare the mean loneliness levels for each group in both years
    x = [2013, 2017]

    # Figure and axis
    fig, ax = plt.subplots()

    # Lines
    (line1,) = ax.plot(x, unemployed_means, label="Went Unemployed", marker="o")
    (line2,) = ax.plot(x, not_unemployed_means, label="Stayed employed", marker="o")

    # Add some labels and title
    ax.set_ylabel("Mean Loneliness Level")
    ax.set_title("Loneliness Levels by Employment Status")
    ax.set_xticks(x)
    ax.legend()

    ax.grid()
    return fig


def plot_loneliness_by_gender_and_employment(data):
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

    # Plotting the data
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

    # Adding some labels and title
    ax.set_ylabel("Loneliness")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Loneliness by employment status and gender")

    # Remove legend from the bar chart
    ax.legend(loc="lower left", ncol=4)

    return fig


def plot_loneliness_by_marital_status_unemployment(data):
    # Data for married people who went unemployed
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

    # Data for unmarried people who went unemployed
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

    # Plotting the data
    labels = ["2013", "2017"]
    x = np.arange(len(labels))

    fig, ax = plt.subplots()

    # Plotting lines instead of bars
    ax.plot(x, married_unemployed_means, "-o", label="Married: Went Unemployed")
    ax.plot(x, unmarried_unemployed_means, "-o", label="Unmarried: Went Unemployed")

    # Adding some labels and title
    ax.set_ylabel("Loneliness")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.title("Loneliness by marital status and unemployment status")

    return fig
