"""Tasks running the core analyses."""
import pandas as pd
import pytask
from psmpy.plotting import *

from final_project.analysis.model import create_psm, drop_na, run_logistic_ps
from final_project.analysis.predict import (
    get_predicted_data,
    matched_df,
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
