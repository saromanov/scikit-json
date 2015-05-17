
#from sklearn.datasets import load_digits
import os
import json
#Dirty, but it needs to load all models
from sklearn import *
import sklearn
import argparse
import functools
import numpy as np
import logging


class Scikitjson:
    def __init__(self):
        self.jsonmodel = None

    def loadFile(self, path):
        self.jsonmodel = self._innerLoad(path)

    def _innerLoad(self, path):
        if not os.path.exists(path):
            raise Exception("file {0} not found".format(path))
        fs = open(path, 'r')
        raw_data = fs.read()
        fs.close()
        data = json.loads(raw_data)
        return data

    def run(self):
        if self.jsonmodel == None:
            raise Exception("Model was not loaded")
        model = ConstructModel(self.jsonmodel)
        model.run()



class ConstructModel:
    def __init__(self, jsonmodel):
        self.jsonmodel = jsonmodel

    def _construct_dataset(self, title):
        alldatasets = dir(datasets)
        if title in alldatasets:
            ds = getattr(datasets, title)()
            return ds.data, ds.target

    def _construct_user_dataset(self, userdataset):
        ''' Load data from file '''
        log.info("Start to construct user dataset")
        if 'path' not in userdataset:
            raise Exception("path param is not found")
        path = userdataset['path']
        if 'data' not in userdataset:
            raise Exception('data param (start and indexes on training) not found')
        else:
            dataidx = userdataset['data']

        if 'labels' not in userdataset:
            print('Labels param not found. Default label index will be last index on file')
            labelsidx = []
        else:
            labelsidx = userdataset['labels']

        if 'split' not in userdataset:
            splitter = ' '
        else:
            splitter = userdataset['split']
        if not os.path.exists(path):
            raise Exception("Dataset file not found")

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


    def _split_dataset(self, X, y):
        ''' Split current dataset on training and testing '''
        pass

    def _construct_method(self, title):
        return self._find_method(title)

    def _find_method(self, title):
        allmethods = dir(sklearn)
        candsplit = title.split('.')
        if len(candsplit) > 1:
            name = candsplit[0]
            #model = sklearn
            return functools.reduce(lambda x,a: getattr(x,a), candsplit[1:], getattr(sklearn, name))()

    def _construct_default_model(self, typetitle):
        """ This comes from 'type'"""
        log.info("Start to construct deafault model")
        if typetitle == 'classification':
            from sklearn.ensemble import RandomForestClassifier
            return RandomForestClassifier(n_estimators=100)
        if typetitle == 'regression':
            from sklearn.liner_model import LogisticRegression
            return LogisticRegression(penalty='l2')

    def run(self):
        #Now for case with one model
        name = list(self.jsonmodel.keys())[0]
        items = self.jsonmodel[name]
        if 'dataset' in items:
            X, y = self._construct_dataset(items['dataset'])
        elif 'dataset_file' in items:
            X, y = self._construct_user_dataset(items['dataset_file'])
        #trainX, trainY, testX, testY = self._split_dataset(X,y)
        if 'method' in items:
            method = self._construct_method(items['method'])
        elif 'type' in items:
            #Now supported is 'classification' and 'regression'
            thistype = items['type']
            method = self._construct_default_model(thistype)
        else:
            raise Exception("Model not found")
        method.fit(X,y)
        if 'predict' not in items:
            print("Predict not contains in your model")
        print("Result: ", method.predict(items['predict']))


def main(path):
    sj = Scikitjson()
    if path == None:
        log.error("Path to JSON model not found")
        return
    sj.loadFile(path)
    sj.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', help='path to json model')
    args = parser.parse_args()
    main(args.json)

