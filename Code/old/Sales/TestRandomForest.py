# Load Libraries
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import pandas as pd

# Read Data
binary= pd.read_csv('http://dni-institute.in/blogs/wp-content/uploads/2017/07/dt_data.csv')
# Explore Data
print binary.describe()

# Data Manipulations
 
# Columns
binary.dtypes.index
# Drop a column
binary.drop('Unnamed: 3', axis=1, inplace=True)
# Target Variable to be made {-1, 1}
binary.Spend_Drop_over50pct.replace([0, 1], ['A', 'B'], inplace=True)
 
# Print a few rows
#binary.head()
 
# Count Target Variable Values
binary.Spend_Drop_over50pct.value_counts()
# Find % Values of Target Variable Levels
#round(binary.Spend_Drop_over50pct.value_counts()*100/len(binary.axes[0]),2)

# Split sample into Train and Test
from sklearn.cross_validation import train_test_split
Train,Test = train_test_split(binary, test_size = 0.3, random_state = 176)
# Print a few rows
#Train.head()

# Split Target and Feature Set
# Keep Target and Independent Variable into different array
Train_IndepentVars = Train.values[:, 3:5]
Train_TargetVar = Train.values[:,5]


# Random Forest Model
rf_model =  RandomForestClassifier(max_depth=10,n_estimators=10)
rf_model.fit(Train_IndepentVars,Train_TargetVar)

# Scoring based on the train RF Model
predictions = rf_model.predict(Train_IndepentVars)
print Train
print predictions

from sklearn.metrics import confusion_matrix
# Confusion Matrix
print(" Confusion matrix ", confusion_matrix(Train_TargetVar, predictions))

importance =  rf_model.feature_importances_

importance = pd.DataFrame(importance, index=Train.columns[3:5], 
                          columns=["Importance"])

print importance
