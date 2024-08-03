import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from symptom_mapping import map_symptoms
from sklearn.base import BaseEstimator, TransformerMixin
from symptom_mapping import map_symptoms

# Load the trained model and label encoder
model = joblib.load('models/dis_pred_model.pkl')
le = joblib.load('models/label_encoder.pkl')
disease_mapping = joblib.load('models/disease_mapping.pkl')





class SymptomMapper(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return pd.DataFrame([map_symptoms(x['symptoms']) for x in X])

# Define the pipeline
pipeline = Pipeline([
    ('symptom_mapping', SymptomMapper()),
    ('disease_classification', model)
])