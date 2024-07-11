import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer, SnowballStemmer, LancasterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer  #criar tf-idf
nltk.download("stopwords")


nltk.download('words')
nltk.download('maxent_ne_chunker')
import pandas as pd

spam = pd.read_csv('output.csv')
spam.dropna(axis=0, inplace=True)

def cleanResume(resumeText):
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[]^`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) # remove non-ascii characters
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    resumeText = re.sub(r'[0-9]+', '', resumeText)  #remove numbers
    return resumeText.lower()

nltk.download('stopwords')
import string

len(stopwords.words('english'))

spam["text"] = spam["text"].apply(lambda x: cleanResume(x))
len(spam["text"][1])

previ = spam['text']
classe = spam['job']

vetorizador = TfidfVectorizer()
previsores = vetorizador.fit_transform(previ)

X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(previsores, classe, test_size=0.3)

floresta = RandomForestClassifier(n_estimators=100)
floresta.fit(X_treinamento, y_treinamento) #identifica de acordo com o x_treinamento qual o y_treinamento vai vir

previsoes = floresta.predict(X_teste)
from sklearn import metrics
import joblib

from sklearn.metrics import accuracy_score
print(accuracy_score(y_teste, previsoes))
joblib.dump(floresta, 'model.pkl')
joblib.dump(vetorizador, 'vetorizador.pkl')