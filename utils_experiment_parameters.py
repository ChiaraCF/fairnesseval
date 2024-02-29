import itertools
import json
from typing import List

import pandas as pd

ADULT_ACS_PUBLIC_COVERAGE_ = ['adult', 'ACSPublicCoverage']
ACS_SELECTED_DATASETS = ['ACSPublicCoverage', 'ACSEmployment']

ACS_dataset_names = [
    'ACSPublicCoverage',  # 1138289
    'ACSEmployment',  # 3236107
    'ACSIncomePovertyRatio',  # 3236107
    'ACSHealthInsurance',  # 3236107
    'ACSIncome',  # 1664500
    'ACSMobility',  # 620937
    'ACSTravelTime',  # 1466648
    'ACSEmploymentFiltered'  # 2590315
]

dataset_names = ['adult'] + ACS_dataset_names

bigger_selected_datasets = ['adult', 'ACSPublicCoverage', 'ACSEmployment']

sigmod_datasets = ['adult_sigmod', 'compas', 'german', ]

sigmod_dataset_map = dict(zip(['compas', 'german', 'adult_sigmod'], ['CompasDataset', 'GermanDataset', 'AdultDataset']))

sigmod_datasets_aif360 = [x + '_aif360' for x in sigmod_datasets]

RANDOM_SEEDS_v1 = range(2)
RANDOM_SEEDs_RESTRICTED_V1 = [1]
sample_variation = RANDOM_SEEDS_v1

fixed_sample_frac = 0.1

eps_v0 = 0.01  # , 0.001] # 0.05 old value
eps_values_v0 = [.005, 0.01, 0.02, 0.05, 0.10, 0.2]

BASE_EPS_V1 = [0.005]
EPS_LIST_V1: list[float] = [0.001, .005, 0.01, 0.02, 0.05, 0.10]
EPS_LIST_V2: list[float] = [0.001, .005, 0.01, 0.02, 0.05, 0.10, 0.15]
EXP_FRACTIONS_SMALLER_DATASETS_v1 = [0.016, 0.063, 0.251, 1.]
EXP_FRACTIONS_v1 = [0.001, 0.004, 0.016, 0.063, 0.251, 1]  # np.geomspace(0.001,1,7) np.linspace(0.001,1,7)
eta_params_v1 = json.dumps({'eta0': [0.5, 1.0, 2.0], 'run_linprog_step': [False],
                            'max_iter': [5, 10, 20, 50, 100]})
eta_params_restricted_v1 = json.dumps({'eta0': [2.0], 'run_linprog_step': [False],
                                       'max_iter': [50]})
eta_params_restricted_v2 = json.dumps({'eta0': [2.0], 'run_linprog_step': [False],
                                       'max_iter': [100]})

experiment_configurations = [

{'experiment_id': 'experiment_code.0',
     'dataset_names': ['ACSEmployment'], # list of dataset names
     'model_names': ['hybrids'], # list of model names
     'eps': BASE_EPS_V1, # list of epsilons
     'exp_fractions': EXP_FRACTIONS_v1, # list of fractions
     'base_model_code': ['lr', 'lgbm'], # list of base model codes
     'random_seeds': RANDOM_SEEDS_v1, # list of random seeds
     'constraint_code': 'dp', # constraint code
     'other_params': eta_params_v1,
     },
    {'experiment_id': 's_h_1.0.TEST',
     'dataset_names': sigmod_datasets,
     'model_names': ['hybrids'],
     'params': ['--redo_tuning'],
     'eps': [0.001, 0.01],
     # 'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': 0,
     'train_test_seeds': [0],
     'constraint_code': 'dp'},

    {'experiment_id': 's_o_1.0',
     'dataset_names': sigmod_datasets_aif360,
     'model_names': ['Calmon', 'ZafarDI'],
     'random_seeds': 0,
     'train_test_seeds': [0, 1],
     'base_model_code': ['lr', 'lgbm'],
     },

    {'experiment_id': 's_h_1.0',
     'dataset_names': sigmod_datasets,
     'model_names': ['hybrids'],
     'params': ['--redo_tuning'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [1],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': range(3),
     'train_test_seeds': range(3),
     'constraint_code': 'dp'
     },

    {'experiment_id': 's_c_1.0',
     'dataset_names': sigmod_datasets_aif360,
     'model_names': ['Calmon'],
     'random_seeds': range(3),
     'train_test_seeds': range(3),
     'base_model_code': ['lr', 'lgbm'],
     },

    {'experiment_id': 's_zDI_1.1',
     'dataset_names': sigmod_datasets_aif360,
     'model_names': ['ZafarDI'],
     'random_seeds': RANDOM_SEEDS_v1,
     'base_model_code': ['lr'],
     },
    {'experiment_id': 's_zDI_1.2',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['ZafarDI'],
     'random_seeds': [0],
     'base_model_code': ['lr'],
     },
    {'experiment_id': 's_zDI_1.22',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['ZafarDI'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'base_model_code': ['lr'],
     },
    {'experiment_id': 's_zEO_1.1',
     'dataset_names': sigmod_datasets_aif360,
     'model_names': ['ZafarEO'],
     'random_seeds': RANDOM_SEEDS_v1,
     'base_model_code': ['lr'],
     'constraint_code': 'eo',
     },
    {'experiment_id': 's_zEO_1.2',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['ZafarEO'],
     'random_seeds': RANDOM_SEEDS_v1,
     'base_model_code': ['lr'],
     'constraint_code': 'eo',
     },
    {'experiment_id': 's_c_1.0r',
     'dataset_names': sigmod_datasets,
     'model_names': ['Calmon'],
     'random_seeds': RANDOM_SEEDS_v1,
     'base_model_code': ['lr', 'lgbm'],
     },
    {'experiment_id': 's_f_1.0r',
     'dataset_names': sigmod_datasets,
     'model_names': ['Feld'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     },
    {'experiment_id': 's_f_1.1r',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['Feld'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     },
    {'experiment_id': 's_f_1.1test',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['Feld'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'states': ['CA', 'LA']
     },
    {'experiment_id': 's_tr_1.0r',
     'dataset_names': sigmod_datasets,
     'model_names': ['ThresholdOptimizer'],
     'random_seeds': RANDOM_SEEDS_v1,
     'base_model_code': ['lr', 'lgbm'],
     'constraint_code': 'dp',
     },
    {'experiment_id': 's_tr_1.1r',
     'dataset_names': sigmod_datasets,
     'model_names': ['ThresholdOptimizer'],
     'random_seeds': RANDOM_SEEDS_v1,
     'base_model_code': ['lr', 'lgbm'],
     'constraint_code': 'eo',
     },
    {'experiment_id': 's_tr_2.0r',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['ThresholdOptimizer'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 's_tr_2.1r',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['ThresholdOptimizer'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },

    {'experiment_id': 's_tr_1.0',
     'dataset_names': sigmod_datasets,
     'model_names': ['ThresholdOptimizer'],
     'random_seeds': range(3),
     'train_test_seeds': range(3),
     'base_model_code': ['lr', 'lgbm'],
     },
    {'experiment_id': 's_tr_1.1',
     'dataset_names': sigmod_datasets,
     'model_names': ['ThresholdOptimizer'],
     'random_seeds': range(3),
     'train_test_seeds': range(3),
     'base_model_code': ['lr', 'lgbm'],
     'constraint_code': 'eo',
     },

    {'experiment_id': 's_tr_2.0',
     'dataset_names': bigger_selected_datasets,
     'model_names': ['ThresholdOptimizer'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 's_tr_2.1',
     'dataset_names': bigger_selected_datasets,
     'model_names': ['ThresholdOptimizer'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 's_tr_2.1.test',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['ThresholdOptimizer'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'eo',
     },
    {'experiment_id': 's_hardt_1.0',  # not goint to do that
     'dataset_names': sigmod_datasets_aif360,
     'model_names': ['Hardt'],
     'random_seeds': range(3),
     'train_test_seeds': range(3),
     'base_model_code': ['lr', 'lgbm'],
     },
    {'experiment_id': 's_h_EO_1.0',  # done
     'dataset_names': sigmod_datasets,
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [1],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': range(3),
     'train_test_seeds': range(3),
     'constraint_code': 'eo'
     },
    {'experiment_id': 'acs_h_gs1_1.test',
     'dataset_names': bigger_selected_datasets,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'train_test_seeds': RANDOM_SEEDS_v1,  # Skf 3 splits --> 2*3 = 6 different splits
     'constraint_code': 'dp',
     'states': ['CA', 'LA']},

    {'experiment_id': 'acs_h_gs1_1.0',  # done
     'dataset_names': ADULT_ACS_PUBLIC_COVERAGE_,
     'model_names': ['hybrids'],
     'params': [  # '--redo_tuning',
         '--redo_exp'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', ],
     'random_seeds': RANDOM_SEEDS_v1,
     'train_test_seeds': RANDOM_SEEDS_v1,  # Skf 3 splits --> 2*3 = 6 different splits
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acs_h_gs1_1.1',  # done
     'dataset_names': bigger_selected_datasets,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lgbm', ],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'train_test_fold': [0],
     'constraint_code': 'dp',
     },

    {'experiment_id': 'acsE_h_gs1_1.0',  # done
     'dataset_names': ['ACSEmployment', ],
     'model_names': ['hybrids'],
     'params': [  # '--redo_tuning',
         '--redo_exp'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', ],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'train_test_fold': [0],
     'constraint_code': 'dp',
     },

    # {'experiment_id': 'acsE_h_gs1_2.0',  # todo
    #  'dataset_names': ['ACSEmployment', ],
    #  'model_names': ['hybrids'],
    #  'eps': base_eps_v1,
    #  'exp_fractions': exp_fraction_list_v1,
    #  'grid_fractions': [1],
    #  'base_model_code': ['lgbm', ],
    #  'random_seeds': range(1),
    #  'train_test_seeds': range(1),
    #  'constraint_code': 'dp',
    #  'train_test_fold': [0],
    #  },

    {'experiment_id': 'acs_h_gs1_EO_1.0',  # done
     'dataset_names': bigger_selected_datasets,
     'model_names': ['hybrids'],
     'params': ['--redo_exp'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', ],  # missing 'lgbm'
     'random_seeds': range(1),  # missing lr random seed 1
     'train_test_seeds': range(1),
     'constraint_code': 'eo',
     'train_test_fold': [0],
     },
    {'experiment_id': 'acs_h_gs1_EO_2.0',  # done
     'dataset_names': bigger_selected_datasets,
     'model_names': ['hybrids'],
     'params': ['--redo_exp'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lgbm', ],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'eo',
     'train_test_fold': [0],
     },
    {'experiment_id': 'acs_h_gsSR_1.0',  # done
     'dataset_names': bigger_selected_datasets,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'dp',
     'train_test_fold': [0],
     },
    {'experiment_id': 'acsE_h_gsSR_1.0r',  # done
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acsE_h_gsSR_1.1r',  # doing
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acs_h_gsSR_1.1',  # done
     'dataset_names': ADULT_ACS_PUBLIC_COVERAGE_,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'dp',
     'train_test_fold': [0],
     },
    {'experiment_id': 'acsE_h_gsSR_1.1',  # done
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'dp',
     'train_test_fold': [0],
     },
    {'experiment_id': 'acs_h_gsSR_2.0',  # done
     'dataset_names': bigger_selected_datasets,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'eo',
     'train_test_fold': [0],
     },
    {'experiment_id': 'acs_h_gsSR_2.1',  # done
     'dataset_names': bigger_selected_datasets,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'eo',
     'train_test_fold': [0],
     },

    {'experiment_id': 'f_eta0_1.0.test',
     'dataset_names': sigmod_datasets,
     'model_names': ['fairlearn_full'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'other_params': eta_params_v1,
     },
    {'experiment_id': 'f_eta0_1.0',
     'dataset_names': sigmod_datasets,
     'model_names': ['fairlearn_full'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'other_params': eta_params_v1,
     },
    {'experiment_id': 'f_eta0_1.1',
     'dataset_names': sigmod_datasets,
     'model_names': ['fairlearn_full'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'other_params': eta_params_v1,
     },
    {'experiment_id': 'f_eta0_1.2',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['fairlearn_full'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'train_test_fold': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'dp',
     'other_params': eta_params_restricted_v1,
     },
    {'experiment_id': 'f_eta0_2.2',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['fairlearn_full'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'train_test_fold': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'eo',
     'other_params': eta_params_restricted_v1,
     },
    {'experiment_id': 'f_eta0_eps.3P',
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['fairlearn_full'],
     'eps': EPS_LIST_V2,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'train_test_fold': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'dp',
     'other_params': eta_params_restricted_v1,
     },
    {'experiment_id': 'f_eta0_eps.4P',
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['fairlearn_full'],
     'eps': EPS_LIST_V2,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'train_test_fold': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'eo',
     'other_params': eta_params_restricted_v1,
     },
    {'experiment_id': 'f_eta0_eps.3E',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['fairlearn_full'],
     'eps': EPS_LIST_V2,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'train_test_fold': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'dp',
     'other_params': eta_params_restricted_v1,
     },
    {'experiment_id': 'f_eta0_eps.4E',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['fairlearn_full'],
     'eps': EPS_LIST_V2,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'train_test_fold': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'eo',
     'other_params': eta_params_restricted_v1,
     },
    {'experiment_id': 'f_eta0_eps.3.2E',
     'dataset_names': ['ACSEmployment', 'german'],
     'model_names': ['fairlearn_full'],
     'eps': EPS_LIST_V2,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'train_test_fold': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'dp',
     'other_params': eta_params_restricted_v2,
     },
    {'experiment_id': 'f_eta0_eps.4.2E',
     'dataset_names': ['ACSEmployment', 'german'],
     'model_names': ['fairlearn_full'],
     'eps': EPS_LIST_V2,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'train_test_fold': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'eo',
     'other_params': eta_params_restricted_v2,
     },
    {'experiment_id': 'f_eta0_2.0',
     'dataset_names': sigmod_datasets,
     'model_names': ['fairlearn_full'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'other_params': eta_params_v1,
     },
    {'experiment_id': 'f_eta0_2.1',
     'dataset_names': sigmod_datasets,
     'model_names': ['fairlearn_full'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'other_params': eta_params_v1,
     },
    {'experiment_id': 'f_eta0_eps.1',
     'dataset_names': sigmod_datasets,
     'model_names': ['fairlearn_full'],
     'eps': EPS_LIST_V2,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'other_params': eta_params_v1,
     },
    {'experiment_id': 'f_eta0_eps.2',
     'dataset_names': sigmod_datasets,
     'model_names': ['fairlearn_full'],
     'eps': EPS_LIST_V2,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'other_params': eta_params_v1,
     },

    {'experiment_id': 'sigmod_h_exp_1.0',  # done
     'dataset_names': ['german', 'compas', ],
     'model_names': ['hybrids'],
     'params': ['--redo_exp'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_SMALLER_DATASETS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'train_test_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'sigmod_h_exp_2.0',  # todo
     'dataset_names': ['german', 'compas', ],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_SMALLER_DATASETS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'dp',
     },
    {'experiment_id': 'sigmod_h_exp_3.0',  # todo
     'dataset_names': ['compas', 'german', ],
     'model_names': ['hybrids'],
     'params': [  # '--redo_tuning',
         '--redo_exp'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_SMALLER_DATASETS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'eo',
     },
    {'experiment_id': 's_h_exp_EO_1.0',  # done
     'dataset_names': ['german', 'compas', ],
     'model_names': ['hybrids'],
     'params': ['--redo_exp'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_SMALLER_DATASETS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'train_test_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },

    {'experiment_id': 'acs_h_eps_1.0',  # done
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acs_h_eps_1.1',  # done
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acs_h_eps_1.E0',  # done
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'dp',
     },

    {'experiment_id': 'acs_h_eps_1.LGBM0',  # done
     'dataset_names': ['ACSPublicCoverage', 'ACSEmployment', ],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acs_eps_EO_1.0',  # done
     'dataset_names': ['ACSPublicCoverage', 'ACSEmployment', ],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acs_eps_EO_1.1',  # done
     'dataset_names': ['ACSEmployment', ],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'constraint_code': 'eo',
     'train_test_fold': [0],
     },
    {'experiment_id': 'acs_eps_EO_2.0',  # done
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'train_test_fold': [0],
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acs_eps_EO_2.1',  # done
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'train_test_fold': [0],
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acs_eps_EO_2.1.test',  # done
     'dataset_names': ['adult'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lgbm'],
     'random_seeds': range(1),
     'train_test_seeds': range(1),
     'train_test_fold': [0],
     'constraint_code': 'eo',
     },

    {'experiment_id': 's_h_EO_1.0r',
     'dataset_names': sigmod_datasets,
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [1],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo'
     },
    {'experiment_id': 's_h_1.0r',
     'dataset_names': sigmod_datasets,
     'model_names': ['hybrids'],
     'params': ['--redo_tuning'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [1],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp'
     },
    {'experiment_id': 'acs_eps_EO_1.0r',
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acsE_eps_EO_1.0r',
     'dataset_names': ['ACSEmployment', ],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acs_h_eps_1.0r',
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acs_h_eps_1.2r',
     'dataset_names': ['ACSPublicCoverage'] + sigmod_datasets,
     'model_names': ['hybrids'],
     'eps': [0.15],
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acsE_h_eps_1.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': EPS_LIST_V1,
     'exp_fractions': [0.251],
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },

    {'experiment_id': 's_h_exp_1.0r',
     'dataset_names': ['german', 'compas', ],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_SMALLER_DATASETS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 's_h_exp_EO_1.0r',
     'dataset_names': ['german', 'compas', ],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_SMALLER_DATASETS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 's_h_exp_2.0r',
     'dataset_names': ['german', 'compas', ],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_SMALLER_DATASETS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 's_h_exp_EO_2.0r',
     'dataset_names': ['german', 'compas', ],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_SMALLER_DATASETS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },

    {'experiment_id': 'acs_h_gs1_1.0r',
     'dataset_names': ADULT_ACS_PUBLIC_COVERAGE_,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acsE_h_gs1_1.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acsE_h_gs1_1.1r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lgbm'],
     'random_seeds': [0],
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acsE_h_gs1_1.2r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lgbm'],
     'random_seeds': RANDOM_SEEDs_RESTRICTED_V1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acs_h_gs1_EO_1.0r',
     'dataset_names': ADULT_ACS_PUBLIC_COVERAGE_,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acsE_h_gs1_EO_1.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acsE_h_gs1_EO_1.1r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'grid_fractions': [1],
     'base_model_code': ['lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acs_h_gsSR_1.0r',
     'dataset_names': ADULT_ACS_PUBLIC_COVERAGE_,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acs_h_gsSR_EO_1.0r',
     'dataset_names': ADULT_ACS_PUBLIC_COVERAGE_,
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': EXP_FRACTIONS_v1,
     'exp_grid_ratio': ['sqrt'],
     'base_model_code': ['lr', 'lgbm'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 'most_frequent_sig.0r',
     'dataset_names': sigmod_datasets,
     'model_names': ['most_frequent'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'most_frequent_ACS.0r',
     'dataset_names': ACS_SELECTED_DATASETS,
     'model_names': ['most_frequent'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },

    {'experiment_id': 'acs_to_binary1.0r',
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': [0.251],
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'conversion_to_binary_sensitive_attribute',
     },
    {'experiment_id': 'acs_to_binaryEO1.0r',
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'exp_fractions': [0.251],
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'conversion_to_binary_sensitive_attribute',
     },
    {'experiment_id': 'acs_to_binary1.1r',
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['ZafarDI', 'ThresholdOptimizer'],
     'exp_fractions': [0.251],
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'conversion_to_binary_sensitive_attribute',
     },
    {'experiment_id': 'acs_to_binary1.2r',
     'dataset_names': ['ACSPublicCoverage'],
     'model_names': ['Calmon', ],
     'exp_fractions': [0.251],
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'conversion_to_binary_sensitive_attribute',
     },

    {'experiment_id': 'acsER_bin1.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'conversion_to_binary_sensitive_attribute',
     'states': ['NY', 'PA'],
     },

    {'experiment_id': 'acsER_bin2.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     'states': ['NY', 'PA'],
     },
    {'experiment_id': 'acsER_bin2.1r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['ThresholdOptimizer', 'Feld', 'ZafarDI', ],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     'states': ['NY', 'PA'],
     },
    {'experiment_id': 'acsER_bin2.2r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids', 'ThresholdOptimizer', 'Feld', 'ZafarDI', ],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'states': ['NY', 'PA'],
     },
    {'experiment_id': 'acsER_bin3.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids', 'ThresholdOptimizer', ],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     'states': ['NY', 'PA'],
     },
    {'experiment_id': 'acsER_bin4.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['ZafarEO', ],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     'states': ['NY', 'PA'],
     },
    {'experiment_id': 'acsER_bin3.1r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids', 'ThresholdOptimizer', 'ZafarEO', ],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'states': ['NY', 'PA'],
     },
    {'experiment_id': 'acsER_bin3.0rtest',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids', 'ThresholdOptimizer', 'ZafarEO', ],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     'states': ['NY', 'PA'],
     },
    {'experiment_id': 'acsER_binB1.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['ThresholdOptimizer'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     },
    {'experiment_id': 'acsER_binB1.0Mr',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['ThresholdOptimizer'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acsER_binB1.1r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids', 'Feld', 'ZafarDI'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     },
    {'experiment_id': 'acsER_binB1.1Mr',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids', 'Feld', 'ZafarDI'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'dp',
     },
    {'experiment_id': 'acsER_binB2.0r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids', 'ThresholdOptimizer', 'Feld', 'ZafarDI'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     },
    {'experiment_id': 'acsER_binB2.0Mr',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['hybrids', 'ThresholdOptimizer', 'Feld', 'ZafarDI'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     },
    {'experiment_id': 'acsER_binB2.1r',
     'dataset_names': ['ACSEmployment'],
     'model_names': ['ZafarEO'],
     'eps': BASE_EPS_V1,
     'base_model_code': ['lr'],
     'random_seeds': RANDOM_SEEDS_v1,
     'constraint_code': 'eo',
     'metrics': 'conversion_to_binary_sensitive_attribute',
     'preprocessing': 'binary_split_by_mean_y',
     },

]

config_values_dict = {
    'vary': ['eps', 'exp_frac', 'fairlearn_eta0'],
    'constrain_code': ['dp', 'eo'],
    'base_model_code': ['lr', 'lgbm'],
    'model_names': ['hybrids'],
    'dataset_name': ['compas', 'german', 'adult_sigmod', 'ACSPublicCoverage', 'ACSEmployment'],
}
configurations_matrix = []
for combination in itertools.product(*config_values_dict.values()):
    configurations_matrix.append(dict(zip(config_values_dict.keys(), combination)))

cols_to_unstack = set(config_values_dict.keys()) - set(['vary'])
df = pd.DataFrame(configurations_matrix)
df['state'] = 'todo'
df['exp_name'] = ''


# df.pivot(index=['vary'], columns=cols_to_unstack, values=['state', 'exp_name'])
# df.to_csv('run_experiments/experiment_matrix_state.csv')
def get_config_by_id(experiment_id):
    exp_dict = None
    for x in experiment_configurations:
        if x['experiment_id'] == experiment_id:
            exp_dict: dict = x
            break
    return exp_dict
