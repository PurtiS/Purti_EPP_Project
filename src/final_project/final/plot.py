"""Functions plotting results."""

import matplotlib.pyplot as plt
from psmpy.plotting import *


def plot_match(psm, title, ylabel, xlabel, names):
    psm.plot_match(Title=title, Ylabel=ylabel, Xlabel=xlabel, names=names)


def plot_effect_size(psm):
    return psm.effect_size_plot()


def effect_size_table(psm):
    return psm.effect_size


def plot_loneliness_by_employment(data):
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

    fig, ax = plt.subplots()
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
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=4)
    return fig
