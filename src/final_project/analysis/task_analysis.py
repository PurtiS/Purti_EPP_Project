"""Tasks running the core analyses."""
import pandas as pd
import pytask
from psmpy.plotting import *

from final_project.analysis.model import (
    create_psm,
    drop_na,
    fit_regression_model,
    load_model,
    perform_subgroup_analysis_age,
    perform_subgroup_analysis_education,
    perform_subgroup_analysis_gender,
    perform_subgroup_analysis_health,
    perform_subgroup_analysis_hhsize,
    perform_subgroup_analysis_marital_status,
    run_logistic_ps,
)
from final_project.analysis.predict import (
    get_predicted_data,
    matched_df,
    predict_att_ate_regression,
    run_knn_matched,
)
from final_project.config import BLD


@pytask.mark.depends_on(
    {
        "scripts": ["model.py", "predict.py"],
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "predictions" / "data_matched.csv")
def task_create_matched_data(depends_on, produces):
    """Fit a logistic model on the filtered data with propensity score matching to get matched dataset."""
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
    matched_data = matched_df(psm, data)
    matched_data.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "models" / "model.pickle")
def task_fit_model_python(depends_on, produces):
    """Fit a logistic regression model (Python version) on matched dataset."""
    data = pd.read_csv(depends_on["data"])
    model = fit_regression_model(data)
    model.save(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
        "model": BLD / "python" / "models" / "model.pickle",
    },
)
@pytask.mark.produces(BLD / "python" / "predictions" / "regression.csv")
def task_predict_python(depends_on, produces):
    """Predict ATT and ATE based on the model estimates (Python version)."""
    data = pd.read_csv(depends_on["data"])
    model = load_model(depends_on["model"])
    predicted = predict_att_ate_regression(data, model)
    predicted.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "predictions" / "subgroup_age.csv")
def task_subgroup_analysis(depends_on, produces):
    """Subgroup Analysis for age."""
    data = pd.read_csv(depends_on["data"])
    predicted = perform_subgroup_analysis_age(data)
    predicted.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "predictions" / "subgroup_gender.csv")
def task_subgroup_analysis_gender(depends_on, produces):
    """Subgroup Analysis based on sex."""
    data = pd.read_csv(depends_on["data"])
    predicted = perform_subgroup_analysis_gender(data)
    predicted.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "predictions" / "subgroup_marital_status.csv")
def task_subgroup_analysis_marital_status(depends_on, produces):
    """Subgroup Analysis based on marital status."""
    data = pd.read_csv(depends_on["data"])
    predicted = perform_subgroup_analysis_marital_status(data)
    predicted.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "predictions" / "subgroup_health.csv")
def task_subgroup_analysis_health(depends_on, produces):
    """Subgroup Analysis based on health."""
    data = pd.read_csv(depends_on["data"])
    predicted = perform_subgroup_analysis_health(data)
    predicted.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "predictions" / "subgroup_education.csv")
def task_subgroup_analysis_education(depends_on, produces):
    """Subgroup Analysis based on education."""
    data = pd.read_csv(depends_on["data"])
    predicted = perform_subgroup_analysis_education(data)
    predicted.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "predictions" / "subgroup_household_size.csv")
def task_subgroup_analysis_hhsize(depends_on, produces):
    """Subgroup Analysis based on the size of household."""
    data = pd.read_csv(depends_on["data"])
    predicted = perform_subgroup_analysis_hhsize(data)
    predicted.to_csv(produces, index=False)
