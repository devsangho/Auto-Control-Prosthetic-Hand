import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.model_selection import train_test_split
import joblib

date = "220309"
subject = "lhr"
samplingrate = 500

kernel_type = "linear"
SVM_C_coefficient = 1
gamma_val = "auto"

class0_result, class1_result, class2_result = [], [], []
acc_result = []


train_0RE = np.loadtxt(
    "dataset/train_abs_{}_{}_6Feature_ch1_ch2_0RE_{}Hz.csv".format(
        subject, date, samplingrate
    ),
    np.float32,
    delimiter=",",
)
train_1WF = np.loadtxt(
    "dataset/train_abs_{}_{}_6Feature_ch1_ch2_1WF_{}Hz.csv".format(
        subject, date, samplingrate
    ),
    np.float32,
    delimiter=",",
)
train_2WE = np.loadtxt(
    "dataset/train_abs_{}_{}_6Feature_ch1_ch2_2WE_{}Hz.csv".format(
        subject, date, samplingrate
    ),
    np.float32,
    delimiter=",",
)
# train_3FI = np.loadtxt('train_abs_{}_{}_6Feature_ch1_ch2_3FI_{}Hz.csv'.format(subject,date,samplingrate), np.float32,
#                        delimiter=',')

test_0RE = np.loadtxt(
    "dataset/test_abs_{}_{}_6Feature_ch1_ch2_0RE_{}Hz.csv".format(
        subject, date, samplingrate
    ),
    np.float32,
    delimiter=",",
)
test_1WF = np.loadtxt(
    "dataset/test_abs_{}_{}_6Feature_ch1_ch2_1WF_{}Hz.csv".format(
        subject, date, samplingrate
    ),
    np.float32,
    delimiter=",",
)
test_2WE = np.loadtxt(
    "dataset/test_abs_{}_{}_6Feature_ch1_ch2_2WE_{}Hz.csv".format(
        subject, date, samplingrate
    ),
    np.float32,
    delimiter=",",
)
# test_3FI = np.loadtxt('test_abs_{}_{}_6Feature_ch1_ch2_3FI_{}Hz.csv'.format(subject,date,samplingrate), np.float32,
#                        delimiter=',')


PRINT_CLFreport = 1


train = np.concatenate((train_0RE, train_1WF, train_2WE), axis=0)
test = np.concatenate((test_0RE, test_1WF, test_2WE), axis=0)

x_train = train[:, 1:]
y_train = train[:, 0]

x_test = test[:, 1:]
y_test = test[:, 0]

svclassifier = OneVsRestClassifier(
    SVC(C=SVM_C_coefficient, kernel=kernel_type, gamma=gamma_val, probability=True)
)
svclassifier.fit(x_train, y_train)

y_pred = svclassifier.predict(x_test)
result_matrix = confusion_matrix(y_test, y_pred)
# predict=svclassifier.predict_proba(x_test)

print(result_matrix)

if PRINT_CLFreport == 1:
    print("*****************************************************")
    print("Case :")
    print(
        classification_report(
            y_test, y_pred, target_names=["Rest", "Flexion", "Extension"]
        )
    )

class0_result = result_matrix[0, 0]
class1_result = result_matrix[1, 1]
class2_result = result_matrix[2, 2]

acc_result = result_matrix[0, 0] + result_matrix[1, 1] + result_matrix[2, 2]
total = result_matrix[0] + result_matrix[1] + result_matrix[2]
total = total[0] + total[1] + total[2]

print("Result of accuracy :", acc_result, "/", total)

print(f"Test Set Accuracy : {accuracy_score(y_test, y_pred) * 100} %\n\n")

res = np.c_[y_test, y_pred]
# result=np.c_[res,predict]
# print(np.round(result,2))
file_name = "{}_svm_0.25_{}_with_{}Hz.pkl".format(date, subject, samplingrate)
joblib.dump(svclassifier, file_name)
