from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from utils import get_train_and_test_data
import pandas as pd

from clean_data import clean_data


raw_df = pd.read_csv("data/raw_captures.csv", skipinitialspace=True)

df = clean_data(raw_df, -95)
df = pd.read_csv("data/out.csv")


X_train, X_test, y_train, y_test = get_train_and_test_data(df, 0.1)


gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)

print(metrics.confusion_matrix(y_test, y_pred))

print("Number of mislabeled points out of a total %d points : %d"
      % (X_test.shape[0], (y_test != y_pred).sum()))