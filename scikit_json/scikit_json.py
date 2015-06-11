
#from sklearn.datasets import load_digits
import os
import json
# Dirty, but it needs to load all models
from sklearn import *
from sklearn.externals import joblib
import sklearn
import argparse
import functools
import numpy as np
import logging


class Scikitjson:

    def __init__(self):
        self.jsonmodel = None
        self.path = None

    def loadFile(self, path):
        self.jsonmodel = self._innerLoad(path)
        self.path = path

    def loadJSONModel(self, model):
        """ Load model without reading from file"""
        self.jsonmodel = json.loads(model)
        return self.jsonmodel

    def _innerLoad(self, path):
        if not os.path.exists(path):
            raise Exception("file {0} not found".format(path))
        fs = open(path, 'r')
        raw_data = fs.read()
        fs.close()
        return self.loadJSONModel(raw_data)

    def run(self):
        if self.jsonmodel == None:
            raise Exception("Model was not loaded")
        model = ConstructModel(self.jsonmodel, title=self.path)
        return model.run()


class ConstructModel:

    def __init__(self, jsonmodel, title=None):
        self.jsonmodel = jsonmodel
        self.title = title

    def _construct_dataset(self, title):
        alldatasets = dir(datasets)
        if title in alldatasets:
            ds = getattr(datasets, title)()
            return ds.data, ds.target

    def _construct_user_dataset(self, userdataset):
        ''' Load data from file '''
        logging.info("Start to construct user dataset")
        filetype = 'default'
        if 'path' not in userdataset:
            raise Exception("path param is not found")
        path = userdataset['path']
        if 'data' not in userdataset:
            raise Exception(
                'data param (start and indexes on training) not found')
        else:
            dataidx = userdataset['data']

        if 'labels' not in userdataset:
            print(
                'Labels param not found. Default label index will be last index on file')
            labelsidx = []
        else:
            labelsidx = userdataset['labels']

        if 'split' not in userdataset:
            splitter = ' '
        else:
            splitter = userdataset['split']
        if not os.path.exists(path):
            raise Exception("Dataset file not found")
        if 'type' in userdataset:
            filetype = userdataset['type']

        if filetype == 'default':
            return self._parse_dataset_by_default(path)
        if tiletype == 'csv':
            return self._parse_as_csv(path)
        else:
            raise Exception("This type of dataset format is not supported")

    def _parse_dataset_by_default(self, path):
        fs = open(path, 'r')
        lines = fs.readlines()
        fs.close()
        X = []
        y = []
        for line in lines:
            res = line.split(splitter)
            X.append(res[dataidx[0]: dataidx[1]])
            y.extend(res[labelsidx[0]: labelsidx[1]])
        log.info("Finished to construct user dataset")
        return np.array(X), np.array(y)

    def _parse_as_csv(self, path):
        if not os.path.exists(path):
            raise Exception("Path for loading dataset is not found")
        fs = open(path, 'r')
        data = fs.read()
        fs.close()
        return csv.reader(data)

    def _split_dataset(self, X, y):
        ''' Split current dataset on training and testing '''
        pass

    def _construct_method(self, title):
        return self._find_method(title)

    def _find_method(self, title):
        args = {}
        if isinstance(title, dict):
            candsplit = title['name'].split('.')
            args = title['params']
        else:
            candsplit = title.split('.')
        allmethods = dir(sklearn)
        if len(candsplit) > 1:
            name = candsplit[0]
            #model = sklearn
            return functools.reduce(lambda x, a: getattr(x, a), candsplit[1:], getattr(sklearn, name))(**args)

    def _random_forest(self):
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(n_estimators=100)

    def _construct_default_model(self, typetitle):
        """ This comes from 'type'"""
        logging.info("Start to construct deafault model")
        typetitle = typetitle.lower()
        if typetitle == 'classification':
            return self._random_forest()
        if typetitle == 'regression':
            from sklearn.linear_model import LogisticRegression
            return LogisticRegression(penalty='l2')
        if typetitle == 'clustering':
            from sklearn.cluster import KMeans
            return KMeans()

    def try_to_save(self, model, path):
        ''' In the case if parameter save in on '''
        if path == None:
            return
        joblib.dump(model, path, compress=9)

    def try_to_load(self, path):
        return joblib.load(path)

    def _predict_and_show(self, method, methodname, data):
        result = method.predict(data)
        print("Result: {0} ({1})".format(result, methodname))
        return result

    def run(self):
        if self.title != None:
            print("Model from {0}\n".format(self.title))
        modelnames = list(self.jsonmodel.keys())
        if len(list(modelnames)) == 0:
            return []
        for key in list(modelnames):
            yield self.run_inner(key)

    def run_inner(self, name):
        '''
           return predicted value
        '''
        logging.info("Start to prepare model {0}".format(name))
        print("Model name: {0} ".format(name))
        typeparams = self.jsonmodel[name]
        if typeparams == {}:
            return []
        items = {key.lower(): value for (key, value) in typeparams.items()}
        if 'load' in items:
            method = self.try_to_load(items['load'])
            if 'predict' not in items:
                return
            return self._predict_and_show(method, items['predict'])
        if 'dataset' in items:
            X, y = self._construct_dataset(items['dataset'])
        elif 'dataset_file' in items:
            X, y = self._construct_user_dataset(items['dataset_file'])
        methodname = items['method'] if 'method' in items else 'RandomForest'
        method = self._construct_method(
            items['method']) if 'method' in items else self._random_forest()
        if 'method' in items:
            method = self._construct_method(items['method'])
        elif 'type' in items:
            # Now supported is 'classification' and 'regression'
            thistype = items['type']
            method = self._construct_default_model(thistype)
        '''else:
            raise Exception("Model not found")'''
        method.fit(X, y)
        self.try_to_save(method, items['save'] if 'save' in items else None)
        if 'predict' not in items:
            print("Predict not contains in your model")
            return
        return self._predict_and_show(method, methodname, items['predict'])


def configure_logging(level):
    if level == None:
        return
    level = level.lower()
    title = logging.NOTSET
    if level == 'debug':
        title = logging.DEBUG
    if level == 'info':
        title = logging.INFO
    if level == 'warning':
        title = logging.ERROR
    if level == 'critical':
        title = logging.CRITICAL
    if level == 'error':
        title = logging.ERROR

    logging.basicConfig(level=title)


def main(path):
    sj = Scikitjson()
    if path == None:
        log.error("Path to JSON model not found")
        return
    sj.loadFile(path)
    print(list(sj.run()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', help='path to json model')
    parser.add_argument(
        '--loglevel', help='DEBUG level to show all info messages')
    args = parser.parse_args()
    configure_logging(args.loglevel)
    main(args.json)
