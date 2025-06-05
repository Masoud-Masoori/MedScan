import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("diabetes.csv")
df.columns = df.columns.str.lower()

# Define target
target = "outcome"

df = df.dropna(axis=0)

# Features and Target
x = df.drop(target, axis=1)
y = df[target]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=100991)


over_sampling = RandomOverSampler(random_state=100)
x_train, y_train = over_sampling.fit_resample(x_train, y_train)


model_pipeline = Pipeline([
    ("scaling", StandardScaler()),
    ("model", RandomForestClassifier(random_state=100))
])

# Train model
model_pipeline.fit(x_train, y_train)

y_predict = model_pipeline.predict(x_test)
print(classification_report(y_test, y_predict))

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model_pipeline, f)


