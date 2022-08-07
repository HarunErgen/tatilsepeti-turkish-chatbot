'''https://github.com/savasy/TurkishSentimentAnalysis'''

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

model = AutoModelForSequenceClassification.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
sentiment = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model)

def get_sentiment(sentence:str) -> tuple:
    '''Return the label of the sentiment and its score between 0 and 1.'''
    pipe = sentiment(sentence)
    return pipe[0]['label'], pipe[0]['score']