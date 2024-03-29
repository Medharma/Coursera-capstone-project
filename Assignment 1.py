# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 03:07:00 2020

@author: dell
"""

#-----------------------------------
# Import packages
#-----------------------------------
import itertools
import urllib
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.ticker import NullFormatter
import pandas as pd
#import matplotlib.ticker as ticker
from sklearn import preprocessing
#import scipy.optimize as opt
#import pylab as pl
#%matplotlib inline

# Downloading file
#!wget -O loan_train.csv https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/FinalModule_Coursera/data/loan_train.csv
#Reading file
url1='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/FinalModule_Coursera/data/loan_train.csv'
urllib.request.urlretrieve(url1,"loan_train.csv")

df = pd.read_csv('loan_train.csv')
df.head()
df.shape

# Convert to date time object
df['due_date'] = pd.to_datetime(df['due_date'])
df['effective_date'] = pd.to_datetime(df['effective_date'])
df.head()
#---------------------------------------

# DATA VISUALIZATION AND PRE PROCESSING

#---------------------------------------

df['loan_status'].value_counts()

import seaborn as sns

bins = np.linspace(df.Principal.min(), df.Principal.max(), 10)
g = sns.FacetGrid(df, col="Gender", hue="loan_status", palette="Set1", col_wrap=2)
g.map(plt.hist, 'Principal', bins=bins, ec="k")

g.axes[-1].legend()
plt.show()

bins = np.linspace(df.age.min(), df.age.max(), 10)
g = sns.FacetGrid(df, col="Gender", hue="loan_status", palette="Set1", col_wrap=2)
g.map(plt.hist, 'age', bins=bins, ec="k")

g.axes[-1].legend()
plt.show()

# PRE PROCESSING 

df['dayofweek'] = df['effective_date'].dt.dayofweek
bins = np.linspace(df.dayofweek.min(), df.dayofweek.max(), 10)
g = sns.FacetGrid(df, col="Gender", hue="loan_status", palette="Set1", col_wrap=2)
g.map(plt.hist, 'dayofweek', bins=bins, ec="k")
g.axes[-1].legend()
plt.show()

df['weekend'] = df['dayofweek'].apply(lambda x: 1 if (x>3)  else 0)
df.head()
df.groupby(['Gender'])['loan_status'].value_counts(normalize=True)

df['Gender'].replace(to_replace=['male','female'], value=[0,1],inplace=True)
df.head()

df.groupby(['education'])['loan_status'].value_counts(normalize=True)

df[['Principal','terms','age','Gender','education']].head()

# Feature Extraction

Feature = df[['Principal','terms','age','Gender','weekend']]
Feature = pd.concat([Feature,pd.get_dummies(df['education'])], axis=1)
Feature.drop(['Master or Above'], axis = 1,inplace=True)
Feature.head()
X = Feature
X[0:5]
y = df['loan_status'].values
y[0:5]

# Normalization

X= preprocessing.StandardScaler().fit(X).transform(X)
X[0:5]

#-----------------------------------------------------

## #Train Test Split

#-----------------------------------------------------



from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=4)
print('Train set in TTS:', X_train.shape, y_train.shape)
print('Test set in TTS:', X_test.shape, y_test.shape)

#-----------------------------------------------------

## MODELING

#-----------------------------------------------------


#KNN Classifier Model

from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
k=4
neigh=KNeighborsClassifier(n_neighbors=k).fit(X_train,y_train)
yKNNhat=neigh.predict(X_test)
Trainset_accuracy_initialKNN=metrics.accuracy_score(y_train, neigh.predict(X_train))
print('Trainset accuracy initial', Trainset_accuracy_initialKNN)
Testset_accuracy_initialKNN=metrics.accuracy_score(y_test, yKNNhat)
print('Testset accuracy initial', Testset_accuracy_initialKNN)
#Compare k value
Ks = 10
mean_accKNN = np.zeros((Ks-1))
std_accKNN = np.zeros((Ks-1))
ConfustionMxKNN = [];
for n in range(1,Ks):
    
    #Train Model and Predict  
    neigh = KNeighborsClassifier(n_neighbors = n).fit(X_train,y_train)
    yKNNhat=neigh.predict(X_test)
    mean_accKNN[n-1] = metrics.accuracy_score(y_test, yKNNhat)

    
    std_accKNN[n-1] = np.std(yKNNhat==y_test)/np.sqrt(yKNNhat.shape[0])

mean_accKNN
k_new = mean_accKNN.argmax()+1
print(metrics.confusion_matrix(y_test,yKNNhat))

#Plot neighbor accuracy for different k
plt.plot(range(1,Ks),mean_accKNN,'g')
plt.fill_between(range(1,Ks),mean_accKNN - 1 * std_accKNN,mean_accKNN + 1 * std_accKNN, alpha=0.10)
plt.legend(('Accuracy ', '+/- 3xstd'))
plt.ylabel('Accuracy ')
plt.xlabel('Number of Neibors (K)')
plt.tight_layout()
plt.show()

#RESULT
print( "The best accuracy was ", mean_accKNN.max(), "with k=", mean_accKNN.argmax()+1)


#--------------------------------------
#DECISION TREE
from sklearn.tree import DecisionTreeClassifier
decisionTree = DecisionTreeClassifier(criterion="entropy", max_depth = 4)
decisionTree # it shows the default parameters

decisionTree.fit(X_train,y_train)

predTree = decisionTree.predict(X_test)

#Results of training module
print (predTree [0:5])
print (y_test [0:5])

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, predTree))
print(classification_report(y_test, predTree))
print("DecisionTrees's Accuracy while training: ", metrics.accuracy_score(y_test, predTree))

# Notice: You might need to uncomment and install the pydotplus and graphviz libraries if you have not installed these before
#!conda install -c conda-forge pydotplus -y
#!conda install -c conda-forge python-graphviz -y
!pip install six

!pip install external
from sklearn.external.six import StringIO
import pydotplus
import matplotlib.image as mpimg
from sklearn import tree
 

dot_data = StringIO()
filename = "decisiontree.png"
featureNames = df.columns[0:6]
targetNames = df["loan"].unique().tolist()
out=tree.export_graphviz(decisionTree,feature_names=featureNames, out_file=dot_data, class_names= np.unique(y_train), filled=True,  special_characters=True,rotate=False)  
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png(filename)
img = mpimg.imread(filename)
plt.figure(figsize=(100, 200))
plt.imshow(img,interpolation='nearest')

#-------------
#SVM Classifier Model
from sklearn import svm
clf = svm.SVC(kernel='rbf')
clf.fit(X_train, y_train) 

yhat_SVM = clf.predict(X_test)

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, yhat_SVM, labels=[2,4])
np.set_printoptions(precision=2)



# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=['PAIDOFF','COLLECTION'],normalize= False,  title='Confusion matrix')

print (classification_report(y_test, yhat_SVM))
print("SVM Model's Accuracy while training: ", metrics.accuracy_score(y_test, yhat_SVM))
#--------------------

#Logistic Regression Classifier Model

from sklearn.linear_model import LogisticRegression
LR = LogisticRegression(C=0.01, solver='liblinear').fit(X_train,y_train)
LR
yhat_LR = LR.predict(X_test)
yhat_LR
#Predict probabilities
yhat_LR_prob = LR.predict_proba(X_test)
yhat_LR_prob

#Initial Accuracy for training module
print(metrics.accuracy_score(y_test, yhat_LR))

#Confusion Matrix
from sklearn.metrics import classification_report, confusion_matrix

print(confusion_matrix(y_test, yhat_LR, labels=[1,0]))

# Compute confusion matrix
cnf_matrix2 = confusion_matrix(y_test, yhat_LR, labels=[1,0])
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix2, classes=['PAIDOFF','COLLECTION'],normalize= False,  title='Confusion matrix')

print (classification_report(y_test, yhat_LR))
print("SVM Model's Accuracy while training: ", metrics.accuracy_score(y_test, yhat_LR))

#----------------------------------

## MODEL EVALUATION

#----------------------------------

from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
#Downloading different test set
#!wget -O loan_test.csv https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_test.csv
url2='https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_test.csv'
urllib.request.urlretrieve(url2,"loan_test.csv")
test_df = pd.read_csv('loan_test.csv')
test_df.head()

test_df['due_date'] = pd.to_datetime(test_df['due_date'])
test_df['effective_date'] = pd.to_datetime(test_df['effective_date'])
test_df['dayofweek'] = test_df['effective_date'].dt.dayofweek
test_df['weekend'] = test_df['dayofweek'].apply(lambda x: 1 if (x>3)  else 0)
test_df.head()
test_df.groupby(['Gender'])['loan_status'].value_counts(normalize=True)
test_df['Gender'].replace(to_replace=['male','female'], value=[0,1],inplace=True)
test_df.groupby(['education'])['loan_status'].value_counts(normalize=True)
test_df[['Principal','terms','age','Gender','education']].head()

test_Feature = test_df[['Principal','terms','age','Gender','weekend']]
test_Feature = pd.concat([test_Feature,pd.get_dummies(test_df['education'])], axis=1)
test_Feature.drop(['Master or Above'], axis = 1,inplace=True)
test_Feature.head()

X_test_df = test_Feature
X_test_df= preprocessing.StandardScaler().fit(X_test_df).transform(X_test_df)
y_test_df = test_df['loan_status'].values

#--------------------
#KNN Model Evaluation

yKNNhat_test_df=neigh.predict(X_test_df)

#Accuracy Scores for KNN model
KNN_Jaccard_accuracy=metrics.jaccard_similarity_score(y_test_df, yKNNhat_test_df)
KNN_F1score_accuracy=metrics.F1_score(y_test_df, yKNNhat_test_df)

#Results
print('Final Accuracy score for KNN Model:')
print('Jaccard of KNN model on loan test %.6f', KNN_Jaccard_accuracy)
print('F1 score of KNN model on loan test %.6f', KNN_F1score_accuracy)
print('Log Loss of KNN model on loan test: NA')
#---------------------
#Decision Tree Model Evaluation

predTree_test_df = decisionTree.predict(X_test_df)

#Accuracy Scores for Decision Tree model
DT_Jaccard_accuracy=metrics.jaccard_similarity_score(y_test_df, predTree_test_df)
DT_F1score_accuracy=metrics.F1_score(y_test_df, predTree_test_df)


#Results
print(confusion_matrix(y_test_df, predTree_test_df))
print(classification_report(y_test_df, predTree_test_df))

print('Final Accuracy score for Decsion Tree Model:')
print('Jaccard of Decision Tree model on loan test %.6f', DT_Jaccard_accuracy)
print('F1 score of Decision Tree model on loan test %.6f', DT_F1score_accuracy)
print('Log Loss of Decision Tree model on loan test: NA')
#--------------------------

#SVM Model Evaluation

yhatSVM_test_df = clf.predict(X_test_df)
#Accuracy Scores for SVM model
SVM_Jaccard_accuracy=metrics.jaccard_similarity_score(y_test_df, yhatSVM_test_df)
SVM_F1score_accuracy=metrics.F1_score(y_test_df, yhatSVM_test_df)


#Results
print(confusion_matrix(y_test_df, yhatSVM_test_df))
print(classification_report(y_test_df, yhatSVM_test_df))

print('Final Accuracy score for SVM Model:')
print('Jaccard of SVM model on loan test %.6f', SVM_Jaccard_accuracy)
print('F1 score of SVM model on loan test %.6f', SVM_F1score_accuracy)
print('Log Loss of SVM model on loan test: NA')

#--------------------------------------------------------------------------------
#Logistic Regression Model Evaluation
yhatLR_test_df = LR.predict(X_test_df)

#Predict probabilities
yhatLR_prob_test_df = LR.predict_proba(X_test_df)

#Accuracy Scores for LR model
LR_Jaccard_accuracy=metrics.jaccard_similarity_score(y_test_df, yhatLR_test_df)
LR_F1score_accuracy=metrics.F1_score(y_test_df, yhatLR_test_df)
LR_LogLoss_accuracy=metrics.log_loss(y_test_df, yhatLR_prob_test_df)

#RESULTS
print(confusion_matrix(y_test_df, yhatLR_test_df))
print(classification_report(y_test_df, yhatLR_test_df))

print('Final Accuracy score for Logistic Regression Model:')
print('Jaccard of LR model on loan test %.6f', LR_Jaccard_accuracy)
print('F1 score of LR model on loan test %.6f', LR_F1score_accuracy)
print('Log Loss of LR model on loan test %.6f', LR_LogLoss_accuracy)
