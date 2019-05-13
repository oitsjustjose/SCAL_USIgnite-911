from sklearn.decomposition import PCA
import pandas
import seaborn as sns
import warnings
import os, sys
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model, decomposition, datasets
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

warnings.filterwarnings("ignore")
path = os.path.dirname(sys.argv[0])
folderpath = '/'.join(path.split('/')[0:-1]) + '/'


# def draw_vector(v0, v1, ax=None):
#     ax = ax or plt.gca()
#     arrowprops = dict(arrowstyle="->", linewidth=2, shrinkA=0, shrinkB=0)
#     ax.annotate("", v1, v0, arrowprops=arrowprops)
#
#
# # MAIN Calldata 2018 + 2017 #
calldata = pandas.read_csv("../Excel & CSV Sheets/Grid Layout Test Files/Full Data Grid.csv")

mini = 1
maxi = len(calldata.columns)
# X = calldata.ix[:, mini:maxi].values
# Y = calldata.ix[:, 0].values
# print("Variables in X: ", calldata.columns.values[mini:maxi])

# Principal Component Analysis #
# Link to website covering PCA: https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
# PCA is a dimensionality reduction algorithm, used for visusalization, noise filtering, feature extraction, and more

# The following is useful for a 2D dataset, which we don't use #
# plt.scatter(X[:, 0], X[:, 0])
# plt.axis("equal")
# plt.show()

# In PCA, a relationship between X and Y values is quantified by finding a list of the principal axes in the data,
# and using those axes to describe the dataset
# Using Scikit-Learn's PCA estimator, we can compute the following:
# pca = PCA(n_components=4)  # number of components
# print("PCA Fit: \n\t", pca.fit(X))
# The fit learns some quantities of the data, most importantly the "components" and "explained variance"
# print("PCA Components: \n\t", pca.components_)
# print("PCA Explained Variance: \n\t", pca.explained_variance_)

# Visualize the numbers as vectors over the input data, using "components" do define the direction of the vector,
# and the "explained variance" to define the squared-length of the vector
# Again, this is mainly useful for 2D datasets #
# plt.scatter(X[:, 0], X[:, 1], alpha=0.2)
# for length, vector in zip(pca.explained_variance_, pca.components_):
#     v = vector * 3 * np.sqrt(length)
#     unpack = pca.mean_ + v
#     draw_vector(pca.mean_, unpack)
# plt.show()
# The vectors shown represent the principal axes of the data, and the length of the vector is an indication of how
# "important" that axis is in describing the distribution of the data; it's a measure of the variance of the data when
# projected onto that axis
# The projection of each data point onto the principal axes are the "principal components" of the data

# PCA as dimensionality reduction #
# Using PCA for dimenstionality reduction involves zeroing out one or more of the smallest principal components,
# resulting in a lower-dimensional projection of the data that preserves the maximal data variance
# In the above code, we set the shape of the dataset to 4 components, now we transform it and store it in a new variable
# X_pca = pca.transform(X)
# print("Original shape: ", X.shape)
# print("New Shape: ", X_pca.shape)

# PCA for visualization #
# Plot the first two principal components of each point to learn about the data
# plt.scatter(X_pca[:, 0], X_pca[:, 1], c=Y, edgecolor="none", alpha=0.5, cmap=plt.cm.get_cmap("Spectral", 10))
# plt.xlabel("component 1")
# plt.ylabel("component 2")
# plt.colorbar()
# plt.show()

# The main difference between classification and regression methods is that the input data are unlabeled
# The classification algorithm learns the structure of the data without any assistance
# This allows us to process large amounts of data since the data doesn't need to be manually labeled
# It also is hard to evaluate the quality of an unsupervised algorithm due to the absence of an explicit goodness metric
# used in supervised learning
# Dimensionality reduction may help with data visualization and help deal with multicollinearity of data, and help
# prepare data for supervised learning
# Using PCA, we can remove highly correlated features
# To decrease dimentionality from n to k, we sort our list of axes in order of decreasing dispersion and take the
# top k of them

# Create a 3D plot

# https://www.kaggle.com/kashnitsky/topic-7-unsupervised-learning-pca-and-clustering
# fig = plt.figure(1)
# plt.clf()
# ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
# plt.cla()
#
# for name, label in [("Setosa", 0), ("Versicolour", 1), ("Virginica", 2)]:
#     ax.test3D(X[Y == label, 0].mean(),
#               X[Y == label, 1].mean() + 1.5,
#               X[Y == label, 2].mean(), name,
#               horizonatalalignment="center",
#               bbox=dict(alpha=.5, edgecolor="w", facecolor="w"))
# # Change order of labels so they match
# y_clr = np.choose(Y, [1, 2, 0]).astype(np.float)
# ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y_clr, cmap=plt.cm.nipy_spectral)
#
# ax.w_xaxis.set_ticklabels([])
# ax.w_yaxis.set_ticklabels([])
# ax.w_zaxis.set_ticklabels([])


logistic = linear_model.LogisticRegression()

pca = decomposition.PCA()
pipe = Pipeline(steps=[('pca', pca), ('logistic', logistic)])

X_digits = calldata.ix[:, mini:maxi].values
y_digits = calldata.ix[:, 0].values

# digits = datasets.load_digits()
# X_digits = digits.data
# y_digits = digits.target
print("X_digits: ", X_digits)
print(type(X_digits))
print("Y_digits: ", y_digits)
print(type(y_digits))

# Plot the PCA spectrum
pca.fit(X_digits)

plt.figure(1, figsize=(4, 3))
plt.clf()
plt.axes([.2, .2, .7, .7])
plt.plot(pca.explained_variance_, linewidth=2)
plt.axis('tight')
plt.xlabel('n_components')
plt.ylabel('explained_variance_')

print(pca.components_.shape)
# Prediction
n_components = [5, 8, 11]
Cs = np.logspace(-4, 4, 3)

# Parameters of pipelines can be set using ‘__’ separated parameter names:
estimator = GridSearchCV(pipe,
                         dict(pca__n_components=n_components,
                              logistic__C=Cs))
estimator.fit(X_digits, y_digits)

plt.axvline(estimator.best_estimator_.named_steps['pca'].n_components,
            linestyle=':', label='n_components chosen')
plt.legend(prop=dict(size=12))
plt.show()