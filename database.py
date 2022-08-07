import sqlite3
from vnlp import Normalizer
from similarity import get_similarity
from sentiment import get_sentiment

# Constants
UNIDENTIFIED_DIALOG = "Lütfen daha fazla ayrıntı veriniz."
SIMILARITY_THRESHOLD = 0.3 # Similarity score must be greater than threshold to dialog to be returned.

# Connection of database
PATH_TO_DATABASE = r'.\bot.db'
con = sqlite3.connect(PATH_TO_DATABASE, check_same_thread=False)
cur = con.cursor()

# Normalizer from vnlp module
normalizer = Normalizer()
def normalize_message(text: str) -> str:
    ''' Remove punctuations and accent marks, 
    lower and deasciify the text, correct typos.'''
    text = text.lower()
    text = normalizer.remove_punctuations(text)
    text = normalizer.remove_accent_marks(text)
    text = " ".join(normalizer.deasciify(text.split()))
    text = " ".join(normalizer.correct_typos(text.split()))
    return text

def add_dialog(dialog: tuple) -> None:
    '''Add a dialog tuple into the database.'''
    user_input, bot_output = dialog[0], dialog[1]
    cur.execute(f"INSERT INTO dialogs VALUES ('{user_input}', '{bot_output}')")

def get_dialog_by_message(user_input: str) -> tuple:
    '''Return the most similar dialog with the user input.'''
    cur.execute(f"SELECT * FROM dialogs")
    dialogs = cur.fetchall()
    similarity_dict = get_similarity(user_input, dialogs)
    return list(similarity_dict.items())[0]

def get_dialog_by_id(id: int) -> tuple:
    '''Return the dialog with the given ID in the database.'''
    cur.execute(f"SELECT * FROM dialogs WHERE id = {id}")
    dialog = cur.fetchone()
    return dialog

def get_response(user_input: str) -> str:
    '''Return the 'bot output' of the most similar dialog with the user input.'''
    normalized_user_input = normalize_message(user_input)
    dialog, similarity_score = get_dialog_by_message(normalized_user_input)
    sentiment, sentiment_score = get_sentiment(normalized_user_input)
    
    # Information about normalization, similarity and sentiment can be viewed in the terminal.
    print_message_info(
        normalized=normalized_user_input,
        similarity=dialog[1], similarity_score=similarity_score,
        sentiment=sentiment, sentiment_score=sentiment_score
    )
    if similarity_score > SIMILARITY_THRESHOLD:
        return dialog[2]
    else:
        return UNIDENTIFIED_DIALOG

def get_dialog_suggestions(user_input: str) -> list:
    '''Return the four dialogs most similar to the user input'''
    cur.execute(f"SELECT * FROM dialogs")
    dialogs = cur.fetchall()
    similarity_dict = get_similarity(user_input, dialogs)
    return list(similarity_dict.keys())[:4]

def get_api_key() -> str:
    '''Return API Key'''
    cur.execute(f"SELECT * FROM constants WHERE id = 1")
    api_key = cur.fetchone()
    return api_key[1]

def print_message_info(normalized, similarity, similarity_score, sentiment, sentiment_score) -> None:
    print(f'''
                        Message INFO
|-----------------------------------------------------------
|    Normalized message: {normalized}
|-----------------------------------------------------------
|    Similar: {similarity} -> Score: {similarity_score}
|-----------------------------------------------------------
|    Sentiment: {sentiment} -> Score: {sentiment_score}
|-----------------------------------------------------------
    ''')

#add_dialog(("user_input", "bot_output"))
#con.commit()