# scikit-json

Construct models in scikit-learn without programming, only with construction of json files.
json file example with datasets from sklearn
```
{
    "class1" : {
        "dataset": "load_iris", 
        "method": "neighbors.KNeighborsClassifier",
        "predict": [5.8,6.7,2.5,1.6]

    }

}
```

json file example with your dataset
```
{
    "class1" : {
        "dataset_file": {
            "path": "./toy.txt",
            "data": [0,3],
            "labels": [4,5],
            "split": ","
        },
        "method": "neighbors.KNeighborsClassifier",
        "predict": [7,8,5]

    }

}

```

#### Description
_class1_ - title of experiment.
Example: "Experiment1", "experiment2", "foobar", etc

_dataset_ - title of dataset from scikit
Example: "load_iris", "load_digits", "load_boston"

dataset_file - user dataset object
* _path_ - path to dataset
* _data_ - [startindex, endindex] - Get 
* _labels_ - [startindex, endindex] - Get labels
* _split_ - spliting string symbol

Example:
``` 
"dataset_file": {
            "path": "data.csv",
            "data": [0,3],
            "labels": [4],
            "split": ","
        }
```

_method_ - Method name from scikit learn
Example: "svm.SVC", "neighbors.KNeighborsClassifier"

_predict_ - Data to prediction (in list type)
Example: [1,2,3], [1], [0.8,0.5,0.6,0.7]

