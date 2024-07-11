from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import joblib

load_dotenv()

model = joblib.load(os.getenv('seniority_model'))
vectorizer = joblib.load(os.getenv('seniority_vectorizer'))
encoder = joblib.load(os.getenv('seniority_encoder'))

class SeniorityClassifier:
    def encode(curriculum_job):
        encoded_job = encoder.transform([curriculum_job])
        return encoded_job[0]
        
    def vectorize(curriculum_text):
        curriculum_vector = vectorizer.transform([curriculum_text])
        return curriculum_vector.toarray()[0]
        
    def predict(curriculum_text:str, curriculum_job:str):
        encoded_job = SeniorityClassifier.encode(curriculum_job)
        curriculum_vector = SeniorityClassifier.vectorize(curriculum_text)
        
        X = np.hstack((curriculum_vector, encoded_job))

        seniority = model.predict(X.reshape(1,-1))
        probabilities = model.predict_proba(X.reshape(1,-1))
        
        converted_seniority = SeniorityClassifier.converte_seniority_predict(seniority[0])
        converted_probabilities = SeniorityClassifier.seniority_probability(probabilities)
        
        return converted_seniority, converted_probabilities
    
    def converte_seniority_predict(seniority):
        seniorities = {
            0: 'JUNIOR',
            1: 'MID-LEVEL',
            2: 'SENIOR'
        }
        return seniorities.get(seniority)
    
    def seniority_probability(probabilities):
        probability_dict = {
            'JUNIOR': probabilities[0][0],
            'MID-LEVEL': probabilities[0][1],
            'SENIOR': probabilities[0][2]
        }
        sorted_probabilities = dict(sorted(probability_dict.items(), key=lambda item: item[1], reverse=True))
        return sorted_probabilities