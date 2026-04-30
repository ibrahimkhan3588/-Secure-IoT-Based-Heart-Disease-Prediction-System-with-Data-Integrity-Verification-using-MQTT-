# Load Datase
import pandas as pd


# In[2]:
df = pd.read_csv(r'C:\Users\Ibrahim khan\Desktop\project_FYP\datasets_4123_6408_framingham.csv')
df.head()
df = df.drop(columns=['education'])

# Check missing values
print(df.isnull().sum())

# ✅ ADD THIS LINE HERE (IMPORTANT)
df = df.fillna(df.median())

# Verify again
print(df.isnull().sum())



# In[5]:


df.shape


# # Fill Missing Values

# In[6]:


import pandas as pd


# Define the binary columns
bin_cols = ["male", "currentSmoker", "prevalentStroke", "prevalentHyp", "diabetes"]

# Fill missing values for binary features with the most frequent value (mode)
for col in bin_cols:
    mode_val = df[col].mode()[0]
    df[col].fillna(mode_val, inplace=True)

# Check if there are any remaining missing values
missing_values = df.isnull().sum()


# In[11]:


# Import necessary libraries
import numpy as np

# Fill missing values for numeric features
numeric_cols = ["cigsPerDay", "BPMeds", "totChol", "BMI", "heartRate", "glucose"]
for col in numeric_cols:
    median_val = df[col].median()
    df[col].fillna(median_val, inplace=True)


# Check if there are any remaining missing values
missing_values = df.isnull().sum()


# # Balance Dataset

# In[13]:


df['TenYearCHD'].value_counts()


# In[14]:


from sklearn.utils import resample

# Separate majority and minority classes
df_majority = df[df['TenYearCHD'] == 0]
df_minority = df[df['TenYearCHD'] == 1]

# Upsample minority class
df_minority_upsampled = resample(df_minority,
                                 replace=True,     # Sample with replacement
                                 n_samples=len(df_majority),    # To match majority class
                                 random_state=42) # Reproducible results

# Combine majority class with upsampled minority class
df_balanced = pd.concat([df_majority, df_minority_upsampled])


# In[15]:


df_balanced['TenYearCHD'].value_counts()


# # Train Test Split and Feature Scalling

# In[16]:


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Separate features (X) and target variable (y)
X = df_balanced.drop(columns=['TenYearCHD'])
y = df_balanced['TenYearCHD']

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# # Scaling (StandardScale)

# In[17]:


# Initialize StandardScaler
scaler = StandardScaler()

# Fit scaler to training data and transform both training and testing data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# # Training 10 Models With Different Metrics

# In[18]:


from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix


# Define a list of classifiers
classifiers = [
    RandomForestClassifier(),
    GradientBoostingClassifier(),
    LogisticRegression(),
    KNeighborsClassifier(),
    DecisionTreeClassifier(),
]

# Create a dictionary to store the results
results = {}


# Train and evaluate each classifier
for clf in classifiers:
    clf_name = clf.__class__.__name__
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{clf_name} Accuracy: {accuracy}")

    # Classification report
    print(f"Classification Report for {clf_name}:")
    print(classification_report(y_test, y_pred))

    # Confusion matrix
    print(f"Confusion Matrix for {clf_name}:")
    print(confusion_matrix(y_test, y_pred))
    print("="*50)



# # Show Each Model Results

# In[53]:


import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Define a list of classifiers
classifiers = [
    RandomForestClassifier(),
    AdaBoostClassifier(),
    GradientBoostingClassifier(),
    LogisticRegression(),
    SVC(),
    KNeighborsClassifier(),
    DecisionTreeClassifier(),
    GaussianNB(),
    XGBClassifier()
]

# Create a DataFrame to store the results
results_df = pd.DataFrame(columns=['Model', 'Accuracy', 'F1-Score', 'Precision', 'Recall'])

# Train and evaluate each classifier
for clf in classifiers:
    clf_name = clf.__class__.__name__
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    f1_score = report['weighted avg']['f1-score']
    precision = report['weighted avg']['precision']
    recall = report['weighted avg']['recall']

    # Append results to DataFrame
    results_df = pd.concat([results_df, pd.DataFrame([{
        'Model': clf_name,
        'Accuracy': accuracy,
        'F1-Score': f1_score,
        'Precision': precision,
        'Recall': recall
    }])], ignore_index=True)

results_df


# # Best Model

# In[19]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Instantiate the RandomForestClassifier
rf_classifier = RandomForestClassifier()

# Train the RandomForestClassifier
rf_classifier.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred_rf = rf_classifier.predict(X_test_scaled)

# Calculate accuracy
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print("Random Forest Classifier Accuracy:", accuracy_rf)

# Classification report
print("Classification Report for Random Forest Classifier:")
print(classification_report(y_test, y_pred_rf))

# Confusion matrix
print("Confusion Matrix for Random Forest Classifier:")
print(confusion_matrix(y_test, y_pred_rf))


# # Single prediction

# In[20]:


# test 1:
print("predcted class ",rf_classifier.predict(X_test_scaled[10].reshape(1,-1))[0])
print("actual class ", y_test.iloc[10])


# In[21]:


# test 2:
print("predcted class ",rf_classifier.predict(X_test_scaled[200].reshape(1,-1))[0])
print("actual class ", y_test.iloc[200])


# In[22]:


# test 3:
print("predcted class ",rf_classifier.predict(X_test_scaled[110].reshape(1,-1))[0])
print("actual class ", y_test.iloc[110])


# # Save Models

# In[23]:


import pickle
pickle.dump(rf_classifier,open("rf_classifier.pkl",'wb'))
pickle.dump(scaler,open("scaler.pkl",'wb'))


# # Load models to test1

# In[24]:


import pickle

# Load the RandomForestClassifier model
with open("rf_classifier.pkl", "rb") as file:
    rf_classifier = pickle.load(file)

# Load the scaler
with open("scaler.pkl", "rb") as file:
    scaler = pickle.load(file)


# # Predictive System

# In[33]:


import numpy as np

def predict(model, scaler, male, age, currentSmoker, cigsPerDay, BPMeds, prevalentStroke, prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose):
    # Encode categorical variables
    male_encoded = 1 if male.lower() == "male" else 0
    currentSmoker_encoded = 1 if currentSmoker.lower() == "yes" else 0
    BPMeds_encoded = 1 if BPMeds.lower() == "yes" else 0
    prevalentStroke_encoded = 1 if prevalentStroke.lower() == "yes" else 0
    prevalentHyp_encoded = 1 if prevalentHyp.lower() == "yes" else 0
    diabetes_encoded = 1 if diabetes.lower() == "yes" else 0

    # Prepare features array
    features = np.array([[male_encoded, age, currentSmoker_encoded, cigsPerDay, BPMeds_encoded, prevalentStroke_encoded, prevalentHyp_encoded, diabetes_encoded, totChol, sysBP, diaBP, BMI, heartRate, glucose]])

    # scalling
    scaled_features = scaler.transform(features)

    # predict by model
    result = model.predict(scaled_features)

    return result[0]


# In[35]:


# test 1:
male = "female"
age = 56.00
currentSmoker = "yes"
cigsPerDay = 3.00
BPMeds = "no"
prevalentStroke = "no"
prevalentHyp = "yes"
diabetes = 'no'
totChol = 285.00
sysBP = 145.00
diaBP = 100.00
BMI = 30.14
heartRate = 80.00
glucose = 86.00


result = predict(rf_classifier, scaler, male, age, currentSmoker, cigsPerDay, BPMeds, prevalentStroke, prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose)


if result == 1:
    print("Heart Disease")
else:
    print("No Heart Disease")


# In[36]:


male = 'female'
age = 63.0
currentSmoker = 'yes'
cigsPerDay = 3.0
BPMeds = 'no'
prevalentStroke = 'no'
prevalentHyp = 'yes'
diabetes = 'no'
totChol = 267.0
sysBP = 156.5
diaBP = 92.5
BMI = 27.1
heartRate = 60.0
glucose = 79.0
result = 1.0



result = predict(rf_classifier, scaler, male, age, currentSmoker, cigsPerDay, BPMeds, prevalentStroke, prevalentHyp, diabetes, totChol, sysBP, diaBP, BMI, heartRate, glucose)


if result == 1:
    print("Heart Disease")
else:
    print("No Heart Disease")


# In[37]:


import sklearn
sklearn.__version__


# In[ ]:




