&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://user-images.githubusercontent.com/83069560/183309220-95260e52-0e86-4181-b82a-03c25486a27f.png" alt="image" width="150"/>

# Tatilsepeti Turkish Chatbot

Tatilsepeti Chatbot is created by utilizing Telegram API via python-telegram-bot. The main purpose of the bot is to answer the questions of the users and get feedback from the dialog. To achieve this, the bot needs to understand the semantic of the question as good as possible. <br />
In order to understand the questions, the bot processes the asked questions by using Natural Language Processing methods.
  * [Normalization](#normalization)
  * [Semantic Similarity](#semantic-similarity)
  * [Sentimental Analysis](#sentimental-analysis)
## Normalization
The bot normalizes the texts sent by the users by using [***VNLP: Turkish NLP Tools***](https://github.com/vngrs-ai/vnlp) developed by [***VNGRS***](https://vngrs.com).<br />
Normalization consists of:<br />
- Removing punctuations
- Removing accent marks
- Decapitalization
- DeASCIIfication
- Typo corrections
```python
def normalize_message(text: str) -> str:
    ''' Remove punctuations and accent marks, 
    decapitalize and deasciify the text, correct typos.'''
    text = text.lower()
    text = normalizer.remove_punctuations(text)
    text = normalizer.remove_accent_marks(text)
    text = " ".join(normalizer.deasciify(text.split()))
    text = " ".join(normalizer.correct_typos(text.split()))
    return text
```
<img src="https://user-images.githubusercontent.com/83069560/183315656-a6472615-893b-4a99-aaeb-8c7ea51a792c.png" alt="normalization" width="800"/><br />
## Semantic Similarity
The bot cross-checks the asked question with the predetermined questions in the database according to their similarity level. The similarity is computed by encoding sentences into embeddings vectors and taking inner product of them. Google's [***Universal Sentence Encoder***](https://tfhub.dev/google/universal-sentence-encoder-multilingual/3) multilingual extension is used to get sentence embeddings.<br />
<br />
_Example embeddings:_<br />
<img src="https://user-images.githubusercontent.com/83069560/183314101-3dfc9be5-fa40-41d5-a49e-b339be059f1b.png" alt="embeddings"/><br />
<br />
_Semantic Textual Similarity by inner products:_<br />
<img src="https://user-images.githubusercontent.com/83069560/183314131-75ff7114-01c8-4c4a-8eb4-24614819feba.png" alt="similarity"/><br />

## Sentimental Analysis
The bot does the sentimental analysis by using [Bert-base Turkish Sentiment Model](https://huggingface.co/savasy/bert-base-turkish-sentiment-cased) based on [BERTurk](https://huggingface.co/dbmdz/bert-base-turkish-cased) for Turkish Language.<br />
<br />
_Usage of the model:_
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

model = AutoModelForSequenceClassification.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-sentiment-cased")
sentiment = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model)
```
<br />
<p align="center">
  <img src="https://user-images.githubusercontent.com/83069560/183315038-4512061c-0dc2-4a89-b275-bd500c7cd0e1.png" alt="positive" width="45%">
  &nbsp; &nbsp; &nbsp; &nbsp;
  <img src="https://user-images.githubusercontent.com/83069560/183315036-dcec32f2-b7ef-4bae-8959-62adb39cabd2.png" alt="negative" width="45%">
</p>
<br />
Although the bot does not use the sentiments while answering the questions, it is very useful data to evaluate customer happiness.
