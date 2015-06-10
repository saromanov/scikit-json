# scikit-json

Construct models for scikit-learn without programming, only with json files.

# Install and Usage

``` 
git clone https://github.com/saromanov/scikit-json
cd scikit-json
python scikit_json.py --json jsonfiles/example.json
```

# Examples
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

example of json file with link to your dataset
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

example of json file with model parameters
```
{
    "class1" : {
        "dataset": "load_iris", 
        "method": {
            "name": "svm.SVC",
            "params": {
                "kernel": "rbf",
                "gamma" : 0.001,
                "max_iter": 100

            }
        },
        "predict": [5.8,6.7,2.5,1.6]

    }

}
```

example of json file with saving model
```
{
    "class1" : {
        "dataset": "load_iris", 
        "method": "neighbors.KNeighborsClassifier",
        "predict": [5.8,6.7,2.5,1.6],
        "save": "./model1.pkl"

    },

    "class2": {
        "dataset": "load_iris", 
        "method": "svm.SVC",
        "predict": [5.8,6.7,2.5,1.6],
        "save": "./model2.pkl"
    }

}
```

example of json file with loading model
```
{
    "class1": {
        "load": "./model1.pkl",
        "predict": [5.8,6.7,2.5,1.6]
    }
}
```

# Description of fields
_class1_ - title of experiment.
Example: "Experiment1", "experiment2", "foobar", etc

_dataset_ - title of dataset from scikit
Example: "load_iris", "load_digits", "load_boston"

dataset_file - user dataset object
* _path_ - path to your dataset
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
Example: 
``` "method": "svm.SVC" ```
``` "method": "neighbors.KNeighborsClassifier"```

Or, use extended definition of method
```
"method": {
            "name": "svm.SVC",
            "params": {
                "kernel": "rbf",
                "gamma" : 0.001,
                "max_iter": 100

            }
        }
```

_predict_ - Data for prediction (in list type)
Example: [1,2,3], [1], [0.8,0.5,0.6,0.7]

# Licence
MIT
