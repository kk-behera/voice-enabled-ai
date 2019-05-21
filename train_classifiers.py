# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 17:53:27 2018

@author: Kamalakanta
"""

import db_operations as dbo
from nltk.corpus import nps_chat as nc
from sklearn.naive_bayes import MultinomialNB , BernoulliNB
from sklearn.linear_model import LogisticRegression, LinearRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import train_test_split as tst
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier 
from sklearn import metrics
import matplotlib.pyplot as plt
import pickle
    

posts = nc.xml_posts()

categories = ['accept','statement','yanswer','clarify','nanswer','reject','bye','greet','whquestion','ynquestion','command']

categories_dict = {}
for i in range(len(categories)):
    if(categories[i] in {'accept','statement','yanswer','clarify'}):
        categories_dict[categories[i]] = 0
    elif(categories[i] in {'nanswer','reject'}):
        categories_dict[categories[i]] = 1
    elif(categories[i] == 'bye'):
        categories_dict[categories[i]] = 2
    elif(categories[i] == 'greet'):
        categories_dict[categories[i]] = 3
    elif(categories[i] in {'whquestion','ynquestion'}):
        categories_dict[categories[i]] = 4
    elif(categories[i] in {'command'}):
        categories_dict[categories[i]] = 5

#Insert relevent columns into db
def start_complete_insertion():
    for post in posts:
        if((str(post.get('class'))).lower()) in categories:
            dbo.insert_data_into_post_text(post.text,categories_dict[(str(post.get('class'))).lower()])

#Get the contents from db
posts_class_num = dbo.fetch_post_class_num()
posts_text = dbo.fetch_post_texts()   

        
X_train_1,X_text_1,y_train,y_test = tst(posts_text, posts_class_num, test_size = 0.4)

vect = CountVectorizer()

X_train = vect.fit_transform(X_train_1)
X_test = vect.transform(X_text_1)
#fetch_data()
knn = KNeighborsClassifier(n_neighbors = 1)
knn.fit(X_train, y_train)
result = knn.predict(X_test)
accuracy = metrics.accuracy_score(y_test, result)
print("KNeighborsClassifier accuracy "+ str(accuracy))

mnb = MultinomialNB()
mnb.fit(X_train, y_train)
result = mnb.predict(X_test)
accuracy = metrics.accuracy_score(y_test, result)
print("MultinomialNB accuracy "+ str(accuracy))
 
bernouli = BernoulliNB()
bernouli.fit(X_train,y_train);
result = bernouli.predict(X_test)
accuracy = metrics.accuracy_score(y_test, result)
print("BernoulliNB accuracy "+ str(accuracy))

logistic = LogisticRegression()
logistic.fit(X_train,y_train);
result = logistic.predict(X_test)
accuracy = metrics.accuracy_score(y_test, result)
print("LogisticRegression accuracy "+ str(accuracy))


sgdc = SGDClassifier()
sgdc.fit(X_train,y_train);
result = sgdc.predict(X_test)
accuracy = metrics.accuracy_score(y_test, result)
print("SGDClassifier accuracy "+ str(accuracy))

linearsvc = LinearSVC()
linearsvc.fit(X_train,y_train);
result = linearsvc.predict(X_test)
accuracy = metrics.accuracy_score(y_test, result)
print("LinearSVC accuracy "+ str(accuracy))

save_classifier = open("vect.pickle","wb")
pickle.dump(vect, save_classifier)
save_classifier.close()

save_classifier = open("knn.pickle","wb")
pickle.dump(knn, save_classifier)
save_classifier.close()

save_classifier = open("mnb.pickle","wb")
pickle.dump(mnb, save_classifier)
save_classifier.close()

save_classifier = open("bernouli.pickle","wb")
pickle.dump(bernouli, save_classifier)
save_classifier.close()

save_classifier = open("linearsvc.pickle","wb")
pickle.dump(linearsvc, save_classifier)
save_classifier.close()

save_classifier = open("sgdc.pickle","wb")
pickle.dump(sgdc, save_classifier)
save_classifier.close()

save_classifier = open("logistic.pickle","wb")
pickle.dump(logistic, save_classifier)
save_classifier.close()
