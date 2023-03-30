"""Tasks for managing the data."""

import pandas as pd
import pytask

from final_project.config import BLD, SRC
from final_project.data_management import clean_data


@pytask.mark.depends_on(
    {
        "data1": SRC / "data" / "pgen.dta",
        "data2": SRC / "data" / "pl.dta",
        "data3": SRC / "data" / "ppath.dta",
        "data4": SRC / "data" / "hgen.dta",
        "data5": SRC / "data" / "hbrutto.dta",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "data_clean.csv")
def task_clean_data_python(depends_on, produces):
    """Clean the data (Python version)."""
    pgen_treat_df = pd.read_stata(depends_on["data1"])
    ppath_df = pd.read_stata(depends_on["data3"])
    pl_df = pd.read_stata(depends_on["data2"])
    pgen_cov_df = pd.read_stata(depends_on["data1"])
    hgen_df = pd.read_stata(depends_on["data4"])
    hbrutto_df = pd.read_stata(depends_on["data5"])
    data = clean_data(pgen_treat_df, pgen_cov_df, ppath_df, pl_df, hgen_df, hbrutto_df)
    data.to_csv(produces, index=False)
