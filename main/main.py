from sklearn.model_selection import train_test_split
from sklearn.metrics import (precision_score, 
                             recall_score, f1_score,
                             roc_auc_score, 
                             average_precision_score, confusion_matrix)
from sklearn.feature_selection import SelectFromModel
import xgboost as xgb
from xgboost.callback import EarlyStopping

from feature_extraction import *

# number of seconds
# wnd_size = 2

# df_raw = pd.read_excel("../data/denial_of_service/xlsx/AS1.xlsx")
# df_pt_raw = pd.read_excel("../data/SASMaker_data/xlsx/DOS_SASMaker.xlsx")
# df_pt = get_dos_features(df_pt_raw, wnd_size)
# df_pt.to_excel("../data/SASMaker_data/preprocessed/DOS_SASMaker.xlsx", index=False)

df_sasmaker = pd.read_excel("../data/SASMaker_data/preprocessed/DOS_SASMaker.xlsx")
df = pd.read_excel("../data/denial_of_service/preprocessed/AS1.xlsx")

corr = df_sasmaker.corr(numeric_only=True)['label'].abs().sort_values(ascending=False)
# print(corr)
corr_ref = df.corr(numeric_only=True)['label'].abs().sort_values(ascending=False)
# print(corr_ref)

# 2. Split into features (X) and target (y)
X_sasmaker = df_sasmaker.drop("label", axis=1)
# X_pt = df_pt.drop("wnd_goose_pkt_num_of_greater_than_current_sqNum", axis=1)
X_sasmaker = df_sasmaker.drop("wnd_goose_pkt_num_of_all_datSet", axis=1)
y_sasmaker = df_sasmaker["label"]

X = df.drop("label", axis=1)
# X = df.drop("wnd_goose_pkt_num_of_greater_than_current_sqNum", axis=1)
X = df.drop("wnd_goose_pkt_num_of_all_datSet", axis=1)
y = df["label"]


X_train_ref, X_test_ref, y_train_ref, y_test_ref = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)



desired_train_size = len(X_train_ref)
train_ratio = desired_train_size / len(X_sasmaker)

X_train_sasmaker, _, y_train_sasmaker, _ = train_test_split(
    X_sasmaker, y_sasmaker, train_size=train_ratio, random_state=42, shuffle=True
)

print("\nLEN_DF_ref = ", len(df))
print("benign(DF_ref) = ", len(df[df["label"]==False]))
print("malign(DF_ref) = ", len(df[df["label"]==True]))
print("benign(y_train_ref) = ", len(y_train_ref[y_train_ref==False]))
print("malign(y_train_ref) = ", len(y_train_ref[y_train_ref==True]))
print("length of y_train_ref =", len(y_train_ref))

print("\nLEN_DF_sasmaker = ", len(df_sasmaker))
print("benign(DF_sasmaker) = ", len(df_sasmaker[df_sasmaker["label"]==False]))
print("malign(DF_sasmaker) = ", len(df_sasmaker[df_sasmaker["label"]==True]))
print("benign(y_train_sasmaker) = ", len(y_train_sasmaker[y_train_sasmaker==False]))
print("malign(y_train_sasmaker) = ", len(y_train_sasmaker[y_train_sasmaker==True]))
print("length of y_train_sasmaker =", len(y_train_sasmaker))

# 4. Define XGBoost model (sklearn API)
model_sasmaker = xgb.XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, n_jobs=-1, random_state=42, eval_metric="logloss")
model_ref = xgb.XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, n_jobs=-1, random_state=42, eval_metric="logloss")

model_sasmaker.fit(X_train_sasmaker, y_train_sasmaker); model_ref.fit(X_train_ref, y_train_ref)

y_pred_ref = model_ref.predict(X_test_ref)
y_proba_ref = model_ref.predict_proba(X_test_ref)[:, 1]  # probability of positive class

y_pred_sasmaker = model_sasmaker.predict(X_test_ref)
y_proba_sasmaker = model_sasmaker.predict_proba(X_test_ref)[:, 1]  # probability of positive class
# print(y_test_ref[y_test_ref==True])
# print(y_test_ref[y_test_ref==False])
# print(confusion_matrix(y_test_ref, y_pred_ref))
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
# Basic metrics
# precision_pt = precision_score(y_test_ref, y_pred_pt)
# recall_pt = recall_score(y_test_ref, y_pred_pt)
# f1_pt = f1_score(y_test_ref, y_pred_pt)

# precision_ref = precision_score(y_test_ref, y_pred_ref)
# recall_ref = recall_score(y_test_ref, y_pred_ref)
# f1_ref = f1_score(y_test_ref, y_pred_ref)

# roc_auc_pt = roc_auc_score(y_test_ref, y_proba_pt)          # ROC AUC
# pr_auc_pt = average_precision_score(y_test_ref, y_proba_pt) # PR AUC

# roc_auc_ref = roc_auc_score(y_test_ref, y_proba_ref)          # ROC AUC
# pr_auc_ref = average_precision_score(y_test_ref, y_proba_ref) # PR AUC

# print(f"(PRETRAINED) Precision: {precision_pt:.10f}")
# print(f"(PRETRAINED) Recall:    {recall_pt:.10f}")
# print(f"(PRETRAINED) F1 score:  {f1_pt:.10f}")
# print(f"(PRETRAINED) ROC AUC:   {roc_auc_pt:.10f}")
# print(f"(PRETRAINED) PR AUC:    {pr_auc_pt:.10f}")
# print("\n")
# print(f"(REF) Precision: {precision_ref:.10f}")
# print(f"(REF) Recall:    {recall_ref:.10f}")
# print(f"(REF) F1 score:  {f1_ref:.10f}")
# print(f"(REF) ROC AUC:   {roc_auc_ref:.10f}")
# print(f"(REF) PR AUC:    {pr_auc_ref:.10f}")

# Optional detailed view
# print("\nClassification report:")
# print(classification_report(y_test, y_pred, digits=4))

# print("\nConfusion matrix:")
