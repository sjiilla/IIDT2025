# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 10:42:31 2025

@author: S Jilla
"""


import os
import pandas as pd
from sklearn import tree
from sklearn import model_selection
import pydotplus
import io
from sklearn import ensemble #This is what we introduced here.

#returns current working directory 
os.getcwd()
#changes working directory
os.chdir("C:/Users/SJilla/")

titanic_train = pd.read_csv("train.csv")

#EDA
titanic_train.shape
titanic_train.info()

titanic_train1 = pd.get_dummies(titanic_train, columns=['Pclass', 'Sex', 'Embarked'])
titanic_train1.shape
titanic_train1.info()
titanic_train1.head(6)

X_train = titanic_train1.drop(['PassengerId','Age','Cabin','Ticket', 'Name','Survived'], axis=1, inplace=False)
y_train = titanic_train['Survived']

#cv accuracy for bagged tree ensemble
dt_estimator = tree.DecisionTreeClassifier()
#Appy ensemble.BaggingClassificatier
#Base_Estimator = dt_estimator, n_estimators = 5(no. of trees)
bag_tree_estimator1 = ensemble.BaggingClassifier(estimator = dt_estimator, n_estimators = 5)
#scores = model_selection.cross_val_score(bag_tree_estimator1, X_train, y_train, cv = 10)
#print(scores)
#print(scores.mean())
bag_tree_estimator1.fit(X_train, y_train)

#Alternative way with parameters and use GridSearchCV instead of cross_val_score
bag_tree_estimator2 = ensemble.BaggingClassifier(estimator = dt_estimator, n_estimators = 6, random_state=2017)
bag_grid = {'criterion':['entropy','gini']}

bag_grid_estimator = model_selection.GridSearchCV(bag_tree_estimator2, bag_grid, n_jobs=6)
bag_tree_estimator2.fit(X_train, y_train)

#oob(Out Of the Bag) accuracy for bagged tree ensemble
#==============================================================================
# bag_tree_estimator2 = ensemble.BaggingClassifier(dt_estimator, 5, oob_score=True) #oob_score=True
# bag_tree_estimator2.fit(X_train, y_train)
# bag_tree_estimator2.oob_score_
#==============================================================================

os.chdir("C:/")
n_tree = 0
for est in bag_tree_estimator1.estimators_: 
#for est in bag_tree_estimator2.estimators_: 
    dot_data = io.StringIO()
    #tmp = est.tree_
    tree.export_graphviz(est, out_file = dot_data, feature_names = X_train.columns)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())#[0] 
    graph.write_pdf("bagtree" + str(n_tree) + ".pdf")
    n_tree = n_tree + 1
    
os.getcwd()
    
