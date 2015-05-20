import unittest
import scikit_json
import json
import numpy as np


class TestBasicModels(unittest.TestCase):
    def test_type_clustering(self):
        raw_model = '''{
               "class1" : {
                  "dataset": "load_iris",
                  "type": "Clustering",
                "predict": [5.8,6.7,2.5,1.6]
               }
            }
             '''
        experiment = scikit_json.Scikitjson()
        experiment.loadJSONModel(raw_model)
        self.assertIsNotNone(experiment.run(), [1])

    def test_type_clustering_low_case(self):
        raw_model = '''{
               "class1" : {
                  "dataset": "load_iris",
                  "type": "clustering",
                "predict": [4.9,5.8,2.2,3.1]
               }
            }
             '''
        experiment = scikit_json.Scikitjson()
        experiment.loadJSONModel(raw_model)
        self.assertIsNotNone(experiment.run(), [1])

    def test_type_classification(self):
        raw_model = '''{
               "class1" : {
                  "dataset": "load_iris",
                  "type": "classification",
                "predict": [4.9,5.8,2.2,3.1]
               }
            }
             '''
        experiment = scikit_json.Scikitjson()
        experiment.loadJSONModel(raw_model)
        self.assertIsNotNone(experiment.run(), [1])

    def test_type_regression(self):
        raw_model = '''{
               "class1" : {
                  "dataset": "load_iris",
                  "type": "regression",
                "predict": [4.9,5.8,2.2,3.1]
               }
            }
             '''
        experiment = scikit_json.Scikitjson()
        experiment.loadJSONModel(raw_model)
        self.assertIsNotNone(experiment.run(), [1])



class TestSLDatasets(unittest.TestCase):
    def test_load_boston(self):
        raw_model = '''{
               "class1" : {
                  "dataset": "load_boston",
                  "type": "clustering",
                "predict": [  6.32000000e-03,   1.80000000e+01,   2.31000000e+00,
         0.00000000e+00,   5.38000000e-01,   6.57500000e+00,
         6.52000000e+01,   4.09000000e+00,   1.00000000e+00,
         2.96000000e+02,   1.53000000e+01,   3.96900000e+02,
         4.98000000e+00]
               }
            }
             '''
        experiment = scikit_json.Scikitjson()
        experiment.loadJSONModel(raw_model)




unittest.main()
