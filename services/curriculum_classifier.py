from dotenv import load_dotenv
import joblib
from services.pdf_process import PdfProcess
from services.seniority_classifier import SeniorityClassifier
import os
import yake
import numpy as np

load_dotenv()
pdf_path = os.getenv('pdf_path')

model = joblib.load(os.getenv('job_model'))
vectorizer = joblib.load(os.getenv('job_vectorizer'))

class CurriculumClassifier:

    async def yake_calculator(texto):
        kw_extractor = yake.KeywordExtractor(lan="en")
        keywords = kw_extractor.extract_keywords(texto)
        yake_weights = {kw: score for kw, score in keywords}
        
        return yake_weights

    async def tfidf_calculator(texto):
        tfidf_matrix = vectorizer.transform([texto])
        words = vectorizer.get_feature_names_out()
        tfidf_weights = tfidf_matrix.toarray()[0]
        
        return words, tfidf_weights

    async def vet_yake_integration():
        processed_text = PdfProcess.curriculum
        yake_weights = await CurriculumClassifier.yake_calculator(processed_text)
        words, tfidf_weights = await CurriculumClassifier.tfidf_calculator(processed_text)
        
        return CurriculumClassifier.combine_weights(words, yake_weights, tfidf_weights)

    def combine_weights(words, yake_weights, tfidf_weights):
        num_words = len(words)
        words_index = {word: idx for idx, word in enumerate(words)}
        combined_weights = np.zeros(num_words)
        
        for word, idx in words_index.items():
            tfidf_score = tfidf_weights[idx]
            yake_score = yake_weights.get(word, 0)
            combined_weights[idx] = tfidf_score + (1 - yake_score)
        
        return combined_weights.reshape(1, -1)
    
    def class_probability(combined_weights):
        prediction = model.predict(combined_weights)
        probabilities = model.predict_proba(combined_weights)
        class_probabilities = {classe: prob for classe, prob in zip(model.classes_, probabilities[0])}
        top_3_probabilities = {classe: round(prob, 2) for classe, prob in sorted(class_probabilities.items(), key=lambda item: item[1], reverse=True)[:3]}
        return prediction, top_3_probabilities
    
    async def predict():
        await PdfProcess.wait_processing()
        if not PdfProcess.curriculum:
            return None
        
        combined_weights = await CurriculumClassifier.vet_yake_integration()
        prediction, top_3_probabilities = CurriculumClassifier.class_probability(combined_weights)
        seniority, seniority_probabilities = SeniorityClassifier.predict(PdfProcess.curriculum, prediction)
        
        return {
            "classification": prediction[0],
            "classification probabilities": top_3_probabilities,
            "seniority": seniority,
            "seniority probabilities": seniority_probabilities
        }
