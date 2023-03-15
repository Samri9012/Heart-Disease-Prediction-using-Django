from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

df = pd.read_csv(r"dataset.csv")

X = df[['Patient_ID','Patient_Age','Patient_Gender','Patient_Blood_Pressure','Patient_Heartrate']]
y = df['Heart_Disease']

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state=1)

model = RandomForestClassifier()
X_train = X_train.values
model.fit(X_train, Y_train)

model.predict(X_test)

pd.to_pickle(model,r'new_model.pickle')
model = pd.read_pickle(r'new_model.pickle')

Patient_ID = int(input("Enter Patient_ID: "))
Patient_Age = int(input("Enter Patient_Age: "))
Patient_Gender = int(input("Enter Patient_Gender: "))
Patient_Blood_Pressure = int(input("Enter Patient_Blood_Pressure: "))
Patient_Heartrate = int(input("Enter Patient_Heartrate: "))

result = model.predict([[Patient_ID,Patient_Age,Patient_Gender,Patient_Blood_Pressure,Patient_Heartrate]])  # input must be 2D array
print(result)




# <button type="button" class="close" data-dismiss="modal" aria-label="Close" >
#                     <span aria-hidden="true">&times;</span>
#                 </button>