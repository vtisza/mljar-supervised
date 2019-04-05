import unittest
import tempfile
import json
import numpy as np
import pandas as pd

from numpy.testing import assert_almost_equal
from sklearn import datasets
from supervised.automl import AutoML
from supervised.metric import Metric

import sklearn.model_selection
from sklearn.metrics import log_loss


class AutoMLTestWithData(unittest.TestCase):
    def test_fit_and_predict(self):
        with open("./result.txt", "a") as f_result:
            for dataset_id in [3, 24, 31, 38, 44, 179, 737, 720]:  # 720 # 31,44,737
                df = pd.read_csv("./tests/data/data/{0}.csv".format(dataset_id))
                x_cols = [c for c in df.columns if c != "target"]
                X = df[x_cols]
                y = df["target"]

                for repeat in range(10):

                    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
                        X, y, test_size=0.3, random_state=1706 + repeat
                    )
                    automl = AutoML(
                        total_time_limit=60 * 60,  # 1h limit
                        algorithms=["LightGBM", "CatBoost", "Xgboost", "RF", "NN"],
                        start_random_models=10,
                        hill_climbing_steps=3,
                        top_models_to_improve=3,
                        train_ensemble=True,
                        verbose=True,
                    )
                    automl.fit(X_train, y_train)

                    response = automl.predict(X_test)
                    # Compute the logloss on test dataset
                    ll = log_loss(y_test, response)
                    print(
                        "{} {} {} {}".format(repeat, dataset_id, ll, automl._fit_time)
                    )
                    f_result.write(
                        "{} {} {} {}\n".format(repeat, dataset_id, ll, automl._fit_time)
                    )


if __name__ == "__main__":
    unittest.main()
