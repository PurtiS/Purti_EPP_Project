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
    """Plot the regression results by age (Python version)."""
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
    """Plot the regression results by age (Python version)."""
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
    """Plot the regression results by age (Python version)."""
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
    """Plot the regression results by age (Python version)."""
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
    """Plot the regression results by age (Python version)."""
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
    """Plot the regression results by age (Python version)."""
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
    """Plot the regression results by age (Python version)."""
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
    """Plot the regression results by age (Python version)."""
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
    """Plot the regression results by age (Python version)."""
    data = pd.read_csv(depends_on["data"])
    fig = plot_loneliness_by_health(data)
    fig.savefig(produces)
