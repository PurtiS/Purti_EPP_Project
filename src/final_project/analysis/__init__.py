"""Code for the core analyses."""
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

__all__ = [
    create_psm,
    drop_na,
    fit_regression_model,
    load_model,
    run_logistic_ps,
    get_predicted_data,
    matched_df,
    predict_att_ate_regression,
    run_knn_matched,
    perform_subgroup_analysis_age,
    perform_subgroup_analysis_education,
    perform_subgroup_analysis_gender,
    perform_subgroup_analysis_health,
    perform_subgroup_analysis_hhsize,
    perform_subgroup_analysis_marital_status,
]
