# -*- coding: utf-8 -*-
"""IDS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tDLT8_cYX_juJdZdc0815sdLZTfsVGZ6
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix , accuracy_score
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import roc_curve, auc

#reading dataset file
df = pd.read_csv(r"/content/dataset.csv")
print(df.shape)

#Class 1 -> Cameo
#Class 0 -> Osmancik
df.head()

df.info()

#Pre-Processing
#checking for null/missing attributes
null_counts = df.isnull().sum()
print("Number of null values in each column are:")
print(null_counts)

#box plots
sns.set(style="whitegrid")
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(15, 10))
axes = axes.flatten()

for i, column in enumerate(df.columns[:-1]):
    sns.boxplot(x=column, data=df, ax=axes[i], showfliers=True)

plt.tight_layout()
plt.show()

#bar graph
class_counts = df['Target'].value_counts()
class_percentages = df['Target'].value_counts(normalize=True) * 100

plt.figure(figsize=(8, 6))
class_counts.plot(kind='bar', color='skyblue')
plt.title('Frequency of Each Class')
plt.xlabel('Class')
plt.ylabel('Frequency')

#Class 1 -> Cameo
#Class 0 -> Osmancik


for i, v in enumerate(class_counts):
    plt.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=10)
plt.show()

#co-relation matrix

correlation_matrix = df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()

#displays basic statistics for each variable
df.describe().T

#Pairwise Plots
sns.pairplot(df,hue='Target')

#Training and Testing

X = df.drop('Target', axis=1)
y = df['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,stratify=y, random_state=42) #will ensure equal sampling from both the classes
unique_classes_train, counts_train = pd.Series(y_train).value_counts().sort_index().items(), len(y_train)
print("Training Set Class Distribution:")
print(f"Instances: {counts_train}")
for cls, count in unique_classes_train:
    print(f"Class {cls}: {count} instances, {count / counts_train * 100:.2f}%")

unique_classes_test, counts_test = pd.Series(y_test).value_counts().sort_index().items(), len(y_test)
print("\nTesting Set Class Distribution:")
print(f"Instances: {counts_test}")
for cls, count in unique_classes_test:
    print(f"Class {cls}: {count} instances, {count / counts_test * 100:.2f}%")

#KDE Plots
sns.set(style="whitegrid")


for attribute in df.columns[:-1]:

    plt.figure(figsize=(8, 5))
    sns.kdeplot(data=df, x=attribute, hue='Target', common_norm=False, fill=True, palette='husl')
    plt.title(f'KDE Plot for {attribute}')

    plt.show()

#Logistic Regerssion
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")


print("Classification Report:")
print(classification_report(y_test, y_pred))

predictions = model.predict(X_test)

#for model comparision
accuracy_logistic = accuracy_score(predictions,y_test)
precision_logistic = precision_score(y_test, predictions, pos_label=1)
recall_logistic = recall_score(y_test, predictions, pos_label=1)
F1_logistic = f1_score(y_test, predictions, pos_label=1)

#outputs decision scores
probs1 = model.decision_function(X_test)

#confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

#support vector Machine
svm_classifier = SVC(kernel='linear', random_state=42)

svm_classifier.fit(X_train, y_train)
y_pred = svm_classifier.predict(X_test)

predictions = svm_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

probs2 = svm_classifier.decision_function(X_test)


#for model comparision
accuracy_SVM = accuracy_score(predictions,y_test)
precision_SVM = precision_score(y_test, predictions, pos_label=1)
recall_SVM = recall_score(y_test, predictions, pos_label=1)
F1_SVM = f1_score(y_test, predictions, pos_label=1)

print(f"Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(classification_rep)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=svm_classifier.classes_, yticklabels=svm_classifier.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

#K nearest Neighbour
knn_classifier = KNeighborsClassifier(n_neighbors=8)

knn_classifier.fit(X_train, y_train)
y_pred = knn_classifier.predict(X_test)

predictions = knn_classifier.predict(X_test)

accuracy_KNN = accuracy_score(predictions,y_test)
precision_KNN = precision_score(y_test, predictions, pos_label=1)
recall_KNN = recall_score(y_test, predictions, pos_label=1)
F1_KNN = f1_score(y_test, predictions, pos_label=1)

probs3 = knn_classifier.predict_proba(X_test)[:, 1]

#for model comparision
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(classification_rep)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=knn_classifier.classes_, yticklabels=knn_classifier.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

#Lowest K value calculation
k_values = list(range(1, 50))
error_rates = []


for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    error = 1 - knn.score(X_test, y_test)
    error_rates.append(error)

# Plotting the error rates for different k values
plt.figure(figsize=(14, 6))
plt.plot(k_values, error_rates, marker='o', linestyle='-', color='b')
plt.title('Error Rate vs. K Value')
plt.xlabel('K Value')
plt.ylabel('Error Rate')
plt.xticks(k_values)
plt.grid(True)
plt.show()
min_error = min(error_rates)
best_k = k_values[error_rates.index(min_error)]

print(f"Lowest Error Rate: {min_error:.4f} for k = {best_k}")
#Lowest error for K value 8

#Naives Bayes Classifier
naive_bayes_classifier = GaussianNB()

naive_bayes_classifier.fit(X_train, y_train)
y_pred = naive_bayes_classifier.predict(X_test)

predictions = naive_bayes_classifier.predict(X_test)

accuracy_NBC = accuracy_score(predictions,y_test)
precision_NBC = precision_score(y_test, predictions, pos_label=1)
recall_NBC = recall_score(y_test, predictions, pos_label=1)
F1_NBC = f1_score(y_test, predictions, pos_label=1)

#for model comparision
NBC_accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

probs4 = naive_bayes_classifier.predict_proba(X_test)[:, 1]

print(f"Accuracy: {NBC_accuracy * 100:.2f}%")
print("Confusion Matrix:")
print("Classification Report:")
print(classification_rep)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=naive_bayes_classifier.classes_, yticklabels=naive_bayes_classifier.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

df1 = {
    'Model': ['Logistic_Regression', 'KNN','NB Classifier' , 'SVM' ],
    'Precision': [precision_logistic, precision_KNN, precision_NBC, precision_SVM],
    'Recall': [recall_logistic, recall_KNN, recall_NBC, recall_SVM],
    'F1-Score': [F1_logistic, F1_KNN, F1_NBC, F1_SVM],
    'Accuracy': [accuracy_logistic, accuracy_KNN, accuracy_NBC, accuracy_SVM],
}

compare_model = pd.DataFrame(df1)
transpose = (compare_model).T

compare_model

plt.figure(figsize=(13, 6))
sns.heatmap(compare_model.set_index('Model'), annot=True, cmap='YlGnBu', fmt='.3f')
plt.title('Model Comparison')
plt.show()

# ROC curves and AUC for each classifier
fpr1, tpr1, _ = roc_curve(y_test, probs1)
roc_auc1 = auc(fpr1, tpr1)

fpr2, tpr2, _ = roc_curve(y_test, probs2)
roc_auc2 = auc(fpr2, tpr2)

fpr3, tpr3, _ = roc_curve(y_test, probs3)
roc_auc3 = auc(fpr3, tpr3)

fpr4, tpr4, _ = roc_curve(y_test, probs4)
roc_auc4 = auc(fpr4, tpr4)

#ROC curves
plt.figure(figsize=(8, 6))
plt.plot(fpr1, tpr1, label=f'Logistic Regression (AUC = {roc_auc1:.2f})')
plt.plot(fpr2, tpr2, label=f'SVM (AUC = {roc_auc2:.2f})')
plt.plot(fpr3, tpr3, label=f'KNN (AUC = {roc_auc3:.2f})')
plt.plot(fpr4, tpr4, label=f'Naive Bayes (AUC = {roc_auc4:.2f})')

plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random')


plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend()
plt.show()