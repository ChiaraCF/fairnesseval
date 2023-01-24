import os

import pandas as pd

import folktables
from utils_prepare_data import load_transform_ACS
from run import ExpreimentRun

if __name__ == '__main__':
    er = ExpreimentRun()
    descriptions_dir = os.path.join(er.base_result_dir, 'ACSDataset_descriptions')
    os.makedirs(descriptions_dir, exist_ok=True)
    dict_list = []
    t_dict = {}
    for dataset_str in ['ACSEmploymentFiltered', 'ACSIncomePovertyRatio',
                        'ACSMobility',
                        'ACSPublicCoverage', 'ACSEmployment', 'ACSTravelTime',
                        'ACSHealthInsurance',
                        'ACSIncome',
                        ]:
        loader_method = getattr(folktables, dataset_str)
        X, y, A = load_transform_ACS(loader_method=loader_method)
        t_dict.update(dataset_name=dataset_str, size=X.shape[0], columns=X.shape[1], sensitive_attr=A.name,
                      sensitive_attr_nunique=A.nunique(), target_col=y.name, sensitive_attr_unique_values=A.unique())
        desc = X.describe().join([y.describe(), A.describe()])
        desc.to_csv(os.path.join(descriptions_dir, dataset_str + 'describe.csv'))
        dict_list.append(t_dict.copy())
    pd.DataFrame(dict_list).to_csv(os.path.join(descriptions_dir, 'all_df_descriptions_summary.csv'))