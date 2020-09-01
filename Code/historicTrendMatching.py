from sklearn import preprocessing
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt


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

    col5 = ['Accident', 'Hour', 'Join_Count', 'Grid_Num', 'DayFrame']
    if type == 1:
        dataChanged = data.reindex(columns=col1)
    elif type == 2:
        dataChanged = data.reindex(columns=col2)
    elif type == 3:
        dataChanged = data.reindex(columns=col3)
    elif type == 4:
        dataChanged = data.reindex(columns=col4)
    elif type == 5:
        dataChanged = data.reindex(columns=col5)

    return dataChanged


def pred_test_type(data, type):
    """
    An easy to use method for selecting which columns to use for the testing you do
    Also serves as an easy way to find which variables are used in each test type
    :param data:
    :param type:
    :return:
    """

    col5 = ['Hour', 'Join_Count', 'Grid_Num', 'DayFrame']
    if type == 5:
        dataChanged = data.reindex(columns=col5)

    return dataChanged


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


def logRegForecast(X, Y):
    # Have a list of the days you want to predict for
    # Have them in m-d-yyyy format, or a format that follows the date format of the files you want to read in
    dates = ['1-1-2020', '1-2-2020', '1-3-2020', '1-4-2020', '1-5-2020', '1-6-2020', '1-7-2020']
    for date in dates:
        print("Date is ", date)
        # This file read-in requires that the date provided match the format of the date in the file name
        predictData = pandas.read_csv(
            "../Jeremy Thesis/Forecasting/Forecast Files/Forecast Forum %s-Filled.csv" % str(date))

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
        logreg = LogisticRegression()
        logreg.fit(X_train, y_train)

        # These determine what variables to keep
        predictData = pred_test_type(predictData, 5)
        standPredictData = standardize(predictData)

        y_pred = logreg.predict(standPredictData)
        predictData["Prediction"] = y_pred
        predictData.to_csv("../Jeremy Thesis/LogReg_Forecast_%s.csv" % date)


# allAcc = pandas.read_csv("../Jeremy Thesis/All Accidents Formatted.csv")
# acc2020 = pandas.read_csv("../Jeremy Thesis/2020 Accidents to 6-4-2020.csv")

data = pandas.read_csv("../Jeremy Thesis/Total Shift/Data/TS Data 50-50 Split.csv")
cutData = test_type(data, 5)  # set what variables to use
standData = standardize(cutData)  # standardize the data
X = standData.iloc[:, 1:(len(standData.columns) + 1)].values  # Our independent variables
Y = standData.iloc[:, 0].values  # Our dependent variable

# Perform predictions
# logRegForecast(X, Y)

# Make a Logic Table
# logit_model = sm.Logit(Y, X)
# result = logit_model.fit()
# print(result.summary())

# Split the data and create the model
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=7)
# logreg = LogisticRegression()
# logreg.fit(X_train, y_train)

# Predicting on the training set and printing the accruacy
# y_pred = logreg.predict(X_test)
# logAcc = logreg.score(X_test, y_test) * 100
# print('Accuracy of logistic regression classifier on test set: ', round(logAcc, 2))

# Getting the confusion matrix values for the predictions (TN, FP, FN, TN)
# confusion_matrix = confusion_matrix(y_test, y_pred)
# print("[TP  FP]\n[FN  TN]")
# print(confusion_matrix)

# Getting the Precision, Recall, F1 Score, and Support
# print(classification_report(y_test, y_pred))

# Plotting the ROC curve
# logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
# fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:, 1])
# plt.figure()
# plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
# plt.plot([0, 1], [0, 1], 'r--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('ROC Curve')
# plt.legend(loc="lower right")
# plt.show()
