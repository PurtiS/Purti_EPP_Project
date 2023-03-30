"""Tasks running the core analyses."""
import pandas as pd
import pytask
from psmpy.plotting import *

from final_project.analysis.model import (
    create_psm,
    drop_na,
    fit_regression_model,
    load_model,
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
def task_fit_model_python(depends_on, produces):
    """Fit a logistic regression model (Python version)."""
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
    """Fit a logistic regression model (Python version)."""
    data = pd.read_csv(depends_on["data"])
    model = fit_regression_model(data)
    model.save(produces)


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "predictions" / "data_matched.csv",
        "model": BLD / "python" / "models" / "model.pickle",
    },
)
@pytask.mark.task(BLD / "python" / "predictions" / "regression.csv")
def task_predict_python(depends_on, produces):
    """Predict based on the model estimates (Python version)."""
    data = pd.read_csv(depends_on["data"])
    model = load_model(depends_on["model"])
    predicted = predict_att_ate_regression(data, model)
    predicted.to_csv("bld/python/predictions/regression.csv")
