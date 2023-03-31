"""Tasks running the results formatting (tables, figures)."""
import pandas as pd
import pytask
from psmpy.plotting import *

from final_project.analysis.model import create_psm, drop_na, run_logistic_ps
from final_project.analysis.predict import get_predicted_data, run_knn_matched
from final_project.config import BLD
from final_project.final.plot import (
    effect_size_table,
    plot_effect_size,
    plot_loneliness_by_gender_and_employment,
    plot_loneliness_by_health,
    plot_loneliness_by_hh_income,
    plot_loneliness_by_hh_size,
    plot_loneliness_by_marital_status_unemployment,
    plot_loneliness_by_unemployment,
    plot_match,
)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "figures" / "matching.png")
def task_plot_results(depends_on, produces):
    """Plot the match quality of different covariates, it shows that we now have similar people to compare the effects of unemployment.

    The results are derived from the psmpy library

    """
    data = pd.read_csv(depends_on["data"])
    data = drop_na(data)
    psm = create_psm(
        data,
        treatment="went_unemployed",
        indx="pid",
        exclude=["hid", "aggregate_loneliness_2017"],
    )
    run_logistic_ps(psm, balance=False)
    get_predicted_data(psm)
    run_knn_matched(psm, matcher="propensity_score", replacement=False, caliper=None)
    plot_match(
        psm,
        title="Matching Result",
        ylabel="# of obs",
        xlabel="propensity logit",
        names=["treatment", "control"],
    )
    plt.savefig(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "figures" / "effect_size.png")
def task_plot_effect_size(depends_on, produces):
    """Plot the effect sizes of different covariates affecting the outcome variable before and after matching."""
    data = pd.read_csv(depends_on["data"])
    data = drop_na(data)
    psm = create_psm(
        data,
        treatment="went_unemployed",
        indx="pid",
        exclude=["hid", "aggregate_loneliness_2017"],
    )
    run_logistic_ps(psm, balance=False)
    get_predicted_data(psm)
    run_knn_matched(psm, matcher="propensity_score", replacement=False, caliper=None)
    plot_effect_size(psm)
    plt.savefig(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "figures" / "descriptive_stats_1.png")
def task_plot_des_stats_1(depends_on, produces):
    """Plot the descriptive statistics.

    The figure shows the differnce in loneliness levels of people who went unemployed between 2013-17 compared to their employed counterparts

    """
    data = pd.read_csv(depends_on["data"])
    fig = plot_loneliness_by_unemployment(data)
    fig.savefig(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "figures" / "descriptive_stats_2.png")
def task_plot_des_stats_2(depends_on, produces):
    """Plot the second descriptive figure, it shows the loneliness levels in 2013 and 2017 grouped on the basis of gender and experience of unemployment between 2013 and 2017."""
    data = pd.read_csv(depends_on["data"])
    fig = plot_loneliness_by_gender_and_employment(data)
    fig.savefig(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "tables" / "estimation_table.tex")
def task_estimation_table(depends_on, produces):
    """Create the estimation table showing effect size of different covariates before and after matching."""
    data = pd.read_csv(depends_on["data"])
    data = drop_na(data)
    psm = create_psm(
        data,
        treatment="went_unemployed",
        indx="pid",
        exclude=["hid", "aggregate_loneliness_2017"],
    )
    run_logistic_ps(psm, balance=False)
    get_predicted_data(psm)
    run_knn_matched(psm, matcher="propensity_score", replacement=False, caliper=None)
    plot_effect_size(psm)
    table = effect_size_table(psm)
    with open(produces, "w") as f:
        f.write(table.to_latex(index=False))


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "figures" / "descriptive_stats_3.png")
def task_plot_des_stats_3(depends_on, produces):
    """Plot another descriptive figure showing loneliness levels in the two years based on marital status."""
    data = pd.read_csv(depends_on["data"])
    fig = plot_loneliness_by_marital_status_unemployment(data)
    fig.savefig(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "figures" / "descriptive_stats_4.png")
def task_plot_des_stats_4(depends_on, produces):
    """Plot this descriptive figure from the filtered dataset showing loneliness levels grouped with household size."""
    data = pd.read_csv(depends_on["data"])
    fig = plot_loneliness_by_hh_size(data)
    fig.savefig(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "figures" / "descriptive_stats_5.png")
def task_plot_hh_income(depends_on, produces):
    """Plot the descriptive figuure from the cleaned dataset to show change in levels of loneliness grouped by average health differnces across the population ."""
    data = pd.read_csv(depends_on["data"])
    fig = plot_loneliness_by_hh_income(data)
    fig.savefig(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "figures" / "descriptive_stats_6.png")
def task_plot_health_indicator(depends_on, produces):
    """Plot the figure from the cleaned dataset to show the differneces in loneliness levels based on differences in average health levels across the population."""
    data = pd.read_csv(depends_on["data"])
    fig = plot_loneliness_by_health(data)
    fig.savefig(produces)
