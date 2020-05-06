import pandas
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras import callbacks
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing

# Import matplotlib pyplot safely
try:
    import matplotlib.pyplot as plt
except ImportError:
    import matplotlib

    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
from os.path import exists
import datetime


def test_type(data, type):
    """
    An easy to use method for selecting which columns to use for the testing you do
    Also serves as an easy way to find which variables are used in each test type
    :param data:
    :param type:
    :return:
    """
    col1 = ['Accident', 'Longitude', 'Latitude', 'Unix', 'Hour',
            'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    col2 = ['Accident', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'cloudCover', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']

    col3 = ['Accident', 'Join_Count', 'Grid_Num', 'NBR_LANES', 'TY_TERRAIN',
            'FUNC_CLASS', 'DayFrame', 'WeekDay', 'DayOfWeek']

    col4 = ['Accident', 'Grid_Num', 'cloudCover', 'humidity', 'precipIntensity',
            'pressure', 'temperature', 'uvIndex', 'visibility', 'windSpeed', 'Rain',
            'Cloudy', 'Foggy', 'Snow', 'Clear', 'RainBefore', 'DayFrame', 'WeekDay',
            'DayOfWeek']
    if type == 1:
        dataChanged = data.reindex(columns=col1)
    elif type == 2:
        dataChanged = data.reindex(columns=col2)
    elif type == 3:
        dataChanged = data.reindex(columns=col3)
    elif type == 4:
        dataChanged = data.reindex(columns=col4)

    return dataChanged


def get_difference():
    """
    A utility method for finding what variables were dropped between tests
    """
    col1 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col2 = ['Accident', 'Clear', 'Cloudy', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col3 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    col4 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'precipIntensity']

    col5 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'FUNC_CLASS', 'Foggy',
            'Grid_Num', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN',
            'WeekDay', 'cloudCover', 'precipIntensity']

    col6 = ['Accident', 'Clear', 'Cloudy', 'DayFrame', 'DayOfWeek', 'FUNC_CLASS', 'Foggy',
            'Hour', 'Join_Count', 'NBR_LANES', 'Rain', 'RainBefore', 'Snow', 'TY_TERRAIN', 'Unix',
            'WeekDay', 'cloudCover', 'dewPoint', 'humidity', 'precipIntensity', 'temperature', 'windSpeed']

    print("Variables Removed:", (set(col1).difference(col6)))


def standardize(data):
    """
    This standardizes the data into the MinMaxReduced version used for model creation
    """
    columns = data.columns.values[0:len(data.columns.values)]
    # Create the Scaler object
    scaler = preprocessing.MinMaxScaler()
    # Fit your data on the scaler object
    dataScaled = scaler.fit_transform(data)
    dataScaled = pandas.DataFrame(dataScaled, columns=columns)
    return dataScaled


def fitting_loops(X, Y, folder, modelname, avgHolderName):
    # 2 Defining a Neural Network
    # Model creation
    model = Sequential()

    # Input
    # X.shape[1] is the number of columns inside of X
    # Done to remove need to alter input values every time we alter variables used (simplicity)
    model.add(Dense(X.shape[1], input_dim=X.shape[1], activation='sigmoid'))

    # Hidden Layers
    # Use for standard sized variable set
    model.add(Dense(X.shape[1] - 5, activation='sigmoid'))
    model.add(Dropout(.1))
    try:
        model.add(Dense(X.shape[1] - 10, activation='sigmoid'))
    except:
        model.add(Dense(X.shape[1] - 5, activation='sigmoid'))

    # Output
    model.add(Dense(1, activation='sigmoid'))

    # 3 Compiling a model
    model.compile(loss='mse', optimizer='nadam', metrics=['accuracy'])
    print(model.summary())

    # File path to hold results of learning cycle
    file = folder + avgHolderName + "Averages.csv"

    # Training Cycles
    # Each cycle's output is the next cycle's input, so the model learns for each new cycle
    for i in range(0, 10):
        # Splitting data into train and test
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=7)

        # If the model already exists, import and update/use it. If not, create it.
        if exists(folder + modelname):
            model.load_weights(folder + modelname)
            print("Loading Grid Model")

        # If the average holder file exists, import it. If not, create it.
        if exists(file):
            avg_holder = pandas.read_csv(file,
                                         usecols=["Train_Acc", "Train_Loss", "Test_Acc", "Test_Loss", "AUC", "TN", "FP",
                                                  "FN", "TP", "Accuracy", "Precision", "Recall", "Specificity", "FPR"])
            j = avg_holder.shape[0]

        else:
            avg_holder = pandas.DataFrame(
                columns=["Train_Acc", "Train_Loss", "Test_Acc", "Test_Loss", "AUC", "TN", "FP", "FN", "TP", "Accuracy",
                         "Precision", "Recall", "Specificity", "FPR"])
            j = avg_holder.shape[0]

        print("Cycle: ", i)

        # If the model doesn't improve over the past X epochs, exit training
        patience = 30
        stopper = callbacks.EarlyStopping(monitor='accuracy', patience=patience)
        hist = model.fit(X_train, y_train, epochs=500, batch_size=5000, validation_data=(X_test, y_test), verbose=1,
                         callbacks=[stopper])

        # Save the weights for next run.
        model.save_weights(folder + modelname)
        print("Saved grid model to disk")

        # This is evaluating the model, and printing the results of the epochs.
        scores = model.evaluate(X_train, y_train, batch_size=5000)
        print("\nModel Training Accuracy:", scores[1] * 100)
        print("Model Training Loss:", sum(hist.history['loss']) / len(hist.history['loss']))

        # Okay, now let's calculate predictions probability.
        predictions = model.predict(X_test)

        # Then, let's round to either 0 or 1, since we have only two options.
        predictions_round = [abs(round(x[0])) for x in predictions]

        # Finding accuracy score of the predictions versus the actual Y.
        accscore1 = accuracy_score(y_test, predictions_round)
        # Printing it as a whole number instead of a percent of 1. (Just easier for me to read)
        print("Rounded Test Accuracy:", accscore1 * 100)
        # Find the Testing loss as well:
        print("Test Loss", sum(hist.history['val_loss']) / len(hist.history['val_loss']))

        # Finding the AUC for the cycle:
        fpr, tpr, _ = roc_curve(y_test, predictions_round)
        # try:
        roc_auc = auc(fpr, tpr)
        print('AUC: %f' % roc_auc)
        # except:
        #     print("ROC Error, FPR: ", tpr, "TPR: ", tpr)

        # Confusion Matrix:
        tn, fp, fn, tp = confusion_matrix(y_test, predictions_round).ravel()
        print(tn, fp, fn, tp)

        # Adding the scores to the average holder file.
        avg_holder.at[j, 'Train_Acc'] = scores[1] * 100
        avg_holder.at[j, 'Train_Loss'] = sum(hist.history['loss']) / len(hist.history['loss'])
        avg_holder.at[j, 'Test_Acc'] = accscore1 * 100
        avg_holder.at[j, 'Test_Loss'] = sum(hist.history['val_loss']) / len(hist.history['val_loss'])
        try:
            avg_holder.at[j, 'AUC'] = roc_auc
        except:
            avg_holder.at[j, 'AUC'] = 'error in the matrix'
        avg_holder.at[j, 'TP'] = tp
        avg_holder.at[j, 'TN'] = tn
        avg_holder.at[j, 'FP'] = fp
        avg_holder.at[j, 'FN'] = fn

        try:
            accuracy = (tn + tp) / (tp + tn + fp + fn)
        except:
            accuracy = 0
        try:
            precision = tp / (fp + tp)
        except:
            precision = 0
        try:
            recall = tp / (fn + tp)
        except:
            recall = 0
        try:
            fprate = fp / (tn + fp)
        except:
            fprate = 0
        try:
            specificity = tn / (tn + fp)
        except:
            specificity = 0
        print(accuracy, precision, recall, specificity, fprate)
        avg_holder.at[j, 'Accuracy'] = accuracy
        avg_holder.at[j, 'Precision'] = precision
        avg_holder.at[j, 'Recall'] = recall
        avg_holder.at[j, 'Specificity'] = specificity
        avg_holder.at[j, 'FPR'] = fprate

        # Save the average holder file:
        avg_holder.to_csv(file, sep=",")

# The steps of creating a neural network or deep learning model
# 1. Load Data
# 2. Defining a neural network
# 3. Compile a Keras model using an efficient numerical backend
# 4. Train a model on some data.
# 5. Evaluate that model on some data!


files = []

for file in files:
    # 1. Load Data
    data = pandas.read_csv("../%s" % file)
    for i in range(1, 5):
        # Select which type of test you want to do: this determines what columns are used
        cutData = test_type(data, i)
        # Standardize the data before modelling
        cutData = standardize(cutData)

        if "Grid Fix" in file:
            modelType = "Grid Fix"
            modelname = "model_GF_" + file.split(" ")[4] + "Split_Test%d.h5" % i
            avgHolderName = "GF " + file.split(" ")[4] + " Split Test %d" % i
        elif "Hour Shift" in file:
            modelType = "Hour Shift"
            modelname = "model_HS_" + file.split(" ")[4] + "Split_Test%d.h5" % i
            avgHolderName = "HS " + file.split(" ")[4] + " Split Test %d" % i
        elif "Spatial Shift" in file:
            modelType = "Spatial Shift"
            modelname = "model_SS_" + file.split(" ")[4] + "Split_Test%d.h5" % i
            avgHolderName = "SS " + file.split(" ")[4] + " Split Test %d" % i
        elif "Total Shift" in file:
            modelType = "Total Shift"
            modelname = "model_TS_" + file.split(" ")[4] + "Split_Test%d.h5" % i
            avgHolderName = "TS " + file.split(" ")[4] + " Split Test %d" % i
        elif "Date Shift" in file:
            modelType = "Date Shift"
            modelname = "model_DS_" + file.split(" ")[4] + "Split_Test%d.h5" % i
            avgHolderName = "DS " + file.split(" ")[4] + " Split Test %d" % i
        else:
            print("Model naming error")
            exit()
        # Choose a folder for storing all of the results of the code in, including the model itself
        # Note, if the folder you specify doesn't exist, you'll have to create it
        # These are made for code automation later on
        folder = '../Jeremy Thesis/'+modelType+'/Model Results/'

        # Shuffling
        cutData = shuffle(cutData)
        # Creating X and Y. Accident is the first column, therefore it is 0
        X = cutData.iloc[:, 1:(len(cutData.columns) + 1)].values  # Our independent variables
        Y = cutData.iloc[:, 0].values  # Our dependent variable

        # Steps 2-5 are inside the fitting loops method
        fitting_loops(X, Y, folder, modelname, avgHolderName)
