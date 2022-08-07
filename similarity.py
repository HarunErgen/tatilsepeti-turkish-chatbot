'''
Universal Sentence Encoder is a model for encoding sentences into embedding vectors.
https://tfhub.dev/google/universal-sentence-encoder-multilingual/3 is used.
'''
# Libraries
import tensorflow_hub as hub
import tensorflow_text
import numpy as np

# Universal Sentence Encoder Multilingual path
PATH_TO_ENCODER = r'.\universal_sentence_encoder'

# Embedding
embed = hub.load(PATH_TO_ENCODER)

def get_similarity(main_sentence:str, dialogs) -> dict:
    '''The semantic similarity of two sentences can be 
    trivially computed as the inner product of the encodings.'''
    user_inputs = [dialog[1] for dialog in dialogs]
    
    # Inner product of the encodings
    inner_product = np.inner(embed(main_sentence), embed(user_inputs))
    
    dialog_score = {dialogs[i]: inner_product[0][i] for i in range(len(user_inputs))}
    sorted_dict = dict(sorted(dialog_score.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict