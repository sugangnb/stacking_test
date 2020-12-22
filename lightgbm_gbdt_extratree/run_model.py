# encoding:utf-8
# -*- coding: UTF-8 -*-
import re
import pandas as pd
import multiprocessing

from sklearn.model_selection import KFold
from open_competition.tabular.model_fitter import LGBFitter, LGBOpt
from datetime import datetime


def run_model(fitter, param):
    kfold = KFold(n_splits=5)
    _, _, acc_result, _ = fitter.train_k_fold(kfold, df_train, df_test, param)
    print("acc result is " + ",".join([str(acc) for acc in acc_result]))
    return acc_result


train_path = "../data/train_onehot.csv"
test_path = "../data/test_onehot.csv"
df_train = pd.read_csv(train_path)
df_test = pd.read_csv(test_path)


def find_best_param(change_param, value_range, best_param, best_acc):
    acc_result_dict = {}
    change_value = None

    for change_value in value_range:
        param = best_param.copy()
        param[change_param] = change_value
        model = LGBFitter()
        start = datetime.now()
        acc_result = run_model(model, param)
        end = datetime.now()
        print("change_param is " + change_param + ", change_value is " + str(change_value))
        print("time spend is " + str((end - start).microseconds))
        acc_result_dict[change_value] = sum(acc_result) / 5

    tmp_best_acc = min(acc_result_dict.values())
    if tmp_best_acc <= best_acc:
        best_param[change_param] = [value for value in acc_result_dict.keys()
                                    if acc_result_dict.get(value) == tmp_best_acc][0]
        best_acc = tmp_best_acc

        return change_value, best_acc
    else:
        return best_param[change_param], best_acc


def save_process(change_param, best_acc, change_value):
    with open("find_process.csv", mode="a") as file:
        acc = str(best_acc)
        value = str(change_value)
        file.write(f"The best value for {change_param} is {value}, the acc is {acc}.\n")


cpu_count = multiprocessing.cpu_count()
best_acc = 1

# need change
best_param = {'num_thread': cpu_count, 'metric': 'binary_error', 'objective': 'binary', 'num_round': 1000,
              "max_depth": -1, 'num_leaves': 31, 'learning_rate': 1e-1, 'feature_fraction': 1, 'bagging_fraction': 1,
              "lambda_l1": 0, "lambda_l2": 0, "boosting": "gbdt", "extra_trees": True}

# need change
change_param = "learning_rate"
value_range = [3e-2, 5e-2, 7e-2, 9e-2, 1e-1]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "max_depth"
value_range = [-1, 3, 4, 5, 6, 7]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "num_leaves"
value_range = [16, 31, 32, 64, 96]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "feature_fraction"
value_range = [0.2, 0.4, 0.6, 0.8, 1]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "bagging_fraction"
value_range = [0.2, 0.4, 0.6, 0.8, 1]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "lambda_l1"
value_range = [0, 2, 4, 6, 8]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)

change_param = "lambda_l2"
value_range = [0, 2, 4, 6, 8]
change_value, best_acc = find_best_param(change_param, value_range, best_param, best_acc)
save_process(change_param, best_acc, change_value)
