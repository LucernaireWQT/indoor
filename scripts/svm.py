from sklearn import metrics
from sklearn.svm import SVC
import pandas as pd
from clean_data import clean_data
from utils import get_train_and_test_data

raw_df = pd.read_csv("data/raw_captures.csv", skipinitialspace=True)
df = clean_data(raw_df, -95)
X_train, X_test, y_train, y_test = get_train_and_test_data(df, 0.2)


C = 10.0
gamma = 1.0

clf = SVC(C=C, gamma=gamma)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(metrics.confusion_matrix(y_test, y_pred))