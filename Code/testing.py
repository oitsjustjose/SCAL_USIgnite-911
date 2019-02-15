# Use the plaidml backend dynamically if AMD GPU is in use

try:
    import tensorflow as tf
    from tensorflow.python.client import device_lib
    LST = [x.device_type for x in device_lib.list_local_devices()]
    if not 'GPU' in LST:
        import os
        os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
except ImportError:
    import os
    os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"


from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_yaml
import numpy
import os
# Import matplotlib pyplot safely
import matplotlib
import matplotlib.pyplot as plt
import numpy
import pandas
import talos
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from keras.models import Sequential
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib
    matplotlib.use("GtkAgg")
    import matplotlib.pyplot as plt

from ann_visualizer.visualize import ann_viz
from keras_sequential_ascii import keras2ascii
from keras.models import model_from_json


def generate_results(y_test, y_score):
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    font = {'family': 'serif',
            'weight': 'bold',
            'size': 16}

    plt.rc('font', **font)
    fig = plt.figure()
    # plt.subplot(211)
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic curve')
    print('AUC: %f' % roc_auc)
    fig.savefig('roctest.png', bbox_inches='tight')
    # plt.subplot(212)
    print("This point reached. ")
    fig = plt.figure()

    plt.xticks(range(0, 20), range(1, 21))
    plt.yticks(range(0, 2), ['No', 'Yes', ''])
    plt.ylabel('Accident')
    plt.xlabel('Record')
    plt.grid(which='major', axis='x')
    x= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
 
    plt.scatter(x=x, y=predictions_round[0:20], s=100, c='blue', marker='x', linewidth=2)
    plt.scatter(x=x, y=y_test[0:20], s=110,
                facecolors='none', edgecolors='r', linewidths=2)
    fig.savefig('predtest.png', bbox_inches='tight')

    print("Second point reached. ")
    # fig = plt.figure()
    # # plt.subplot(211)
    # plt.plot(hist.history['acc'])
    # plt.plot(hist.history['val_acc'])
    # plt.ylabel('Accuracy')
    # plt.xlabel('Epoch')
    # plt.legend(['Train Accuracy', 'Test Accuracy'], loc='lower right')
    # # plt.show()
    # fig.savefig('acc.png', bbox_inches='tight')
    # print("Third point reached. ")
    # # summarize history for loss
    # # plt.subplot(212)
    # fig = plt.figure()
    # plt.plot(hist.history['loss'])
    # plt.plot(hist.history['val_loss'])
    # plt.ylabel('Loss')
    # plt.xlabel('Epoch')
    # plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
    # # plt.show()
    # fig.savefig('loss.png', bbox_inches='tight')
    # print("End reached. ")

## The steps of creating a neural network or deep learning model ##
    # 1. Load Data
    # 2. Defining a neural network
    # 3. Compile a Keras model using an efficient numerical backend
    # 4. Train a model on some data.
    # 5. Evaluate that model on some data!


#           1. Load Data

test = pandas.read_csv(
    "../Excel & CSV Sheets/TestDay.csv", sep=",")
test = shuffle(test)
test = shuffle(test)

X = test.ix[:, 1:(len(test.columns)+1)].values
y = (test.ix[:, 0].values).reshape((138, 1))
print("Size of X_Test:", X.shape, "Size of y_test:", y.shape)

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")
 
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, y, batch_size=500, verbose=1)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

predictions = loaded_model.predict(X)
print(y[0:5])
print(predictions[0:5])

# Then, let's round to either 0 or 1, since we have only two options.
predictions_round = [abs(round(x[0])) for x in predictions]
# print(rounded)
accscore1 = accuracy_score(y, predictions_round)
print("Rounded Test Accuracy:", accscore1*100)

generate_results(y, predictions)
