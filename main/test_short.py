from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import xgboost as xgb
import pandas as pd

# Import preprocessed data
df_sasmaker = pd.read_excel("./data/denial_of_service_SASMaker/preprocessed/DOS_SASMaker.xlsx")
df = pd.read_excel("./data/denial_of_service_reference/preprocessed/AS1.xlsx")

# Feature selection
corr_sasmaker = df_sasmaker.corr(numeric_only=True)['label'].abs().sort_values(ascending=False)
corr = df.corr(numeric_only=True)['label'].abs().sort_values(ascending=False)
X_sasmaker = df_sasmaker.drop("label", axis=1)
X_sasmaker = df_sasmaker.drop("wnd_goose_pkt_num_of_all_datSet", axis=1)
y_sasmaker = df_sasmaker["label"]
X = df.drop("label", axis=1)
X = df.drop("wnd_goose_pkt_num_of_all_datSet", axis=1)
y = df["label"]

# Train/test split
X_train_ref, X_test_ref, y_train_ref, y_test_ref = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True)
desired_train_size = len(X_train_ref)
train_ratio = desired_train_size / len(X_sasmaker)
X_train_sasmaker, _, y_train_sasmaker, _ = train_test_split(
    X_sasmaker, y_sasmaker, train_size=train_ratio, random_state=42, shuffle=True
)

# Initiate models
model_sasmaker = xgb.XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, n_jobs=-1, random_state=42, eval_metric="logloss")
model_ref = xgb.XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, n_jobs=-1, random_state=42, eval_metric="logloss")

# Train models
model_sasmaker.fit(X_train_sasmaker, y_train_sasmaker) 
model_ref.fit(X_train_ref, y_train_ref)

# Predict test set
y_pred_ref = model_ref.predict(X_test_ref)
y_proba_ref = model_ref.predict_proba(X_test_ref)[:, 1]
y_pred_sasmaker = model_sasmaker.predict(X_test_ref)
y_proba_sasmaker = model_sasmaker.predict_proba(X_test_ref)[:, 1]

# Build confusion matrices
tn, fp, fn, tp = confusion_matrix(y_test_ref, y_pred_ref).ravel().tolist()
print("\nREFERENCE: ")
print("TP = ", tp)
print("FP = ", fp)
print("FN = ", fn)
print("TN = ", tn)
tn, fp, fn, tp = confusion_matrix(y_test_ref, y_pred_sasmaker).ravel().tolist()
print("\nSASMaker: ")
print("TP = ", tp)
print("FP = ", fp)
print("FN = ", fn)
print("TN = ", tn)