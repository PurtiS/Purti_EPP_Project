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
    df1 = pd.read_stata(depends_on["data1"])
    df5 = pd.read_stata(depends_on["data3"])
    df6 = pd.read_stata(depends_on["data2"])
    df_2013 = pd.read_stata(depends_on["data1"])
    df7 = pd.read_stata(depends_on["data4"])
    df8 = pd.read_stata(depends_on["data5"])
    data = clean_data(df1=df1, df5=df5, df6=df6, df_2013=df_2013, df7=df7, df8=df8)
    data.to_csv(produces, index=False)
