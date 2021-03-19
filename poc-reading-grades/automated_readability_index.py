import nltk
from nltk import SyllableTokenizer
from nltk.tokenize.repp import ReppTokenizer
from nltk.translate.bleu_score import sentence_bleu
import json
import requests
nltk.download('punkt')

# Key for getting 10k words a day translated
key = "337a9b202ed852fe8636"

url = 'https://api.mymemory.translated.net/get?'

def ARI(text):
    """
    Automated Readability Index
    Returns an approximation fo the grade required to comprehend the text
    with a grade between 1-14, where 1 is kindergarten and 14 is university graduate
    """
    words  = sum(c.isspace() for c in text) + 1
    characters = sum(c.isalpha() or c.isdigit() for c in text)
    sentences = len(nltk.sent_tokenize(text))
    print("{words} words and {chars} characters in {sent} sentences".format(words=words, chars=characters, sent=sentences))
    pt1 = 4.71*float(characters/words)
    pt2 = 0.5*float(words/sentences)
    pt3 = -21.43
    return pt1 + pt2 + pt3

def flesch_kincaid_grade(text):
    """
    Flesch-kincaid grade level
    Returns a level between 0 and 18, seperated in
    levels of 3 
    """
    words = sum(c.isspace() for c in text) + 1
    sentences = len(nltk.sent_tokenize(text))
    syllables = _syllables(text)
    pt1 = 0.39*float(words/sentences)
    pt2 = 11.8*(syllables/words) - 15.59
    return pt1 + pt2

def flesch_reading_ease(text):
    """ 
    Flesch reading-ease score (FRES) 
    Scores between 0-100, where 100 is 
    easily understood and 0 is university graduate level
    """
    words = sum(c.isspace() for c in text) + 1
    sentences = len(nltk.sent_tokenize(text))
    syllables = _syllables(text)

    pt1 = -1.015*float(words/sentences)
    pt2 = -84.6*float(syllables/words)
    return 206.835 + pt1 + pt2

def translate(totranslate, lang1, lang2):
    """
    Translates the translate value
    from lang1 to lang2, 
    which have to be noted according to ISO 639-1
    """
    translated = requests.get(url,  params = {'q': totranslate, 'source': lang1, 'target': lang2, 'langpair': lang1 + '|' + lang2, 'key': key})
    print(translated.text)
    result = json.loads(translated.text)['responseData']['translatedText']
    total = 0
    for word in result.split(' '):
        total = total + _syllables(word)
    return _syllables(result)

# ENGLISH ONLY
def _syllables(word):
    """
    Counts the syllables which are present in this word 
    """
    syllable_count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith('e'):
        syllable_count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count += 1
    return syllable_count

# # Dutch input sentences
# to_translate = ""

# # Convert to english for easier calculations and preprocessing
# translated = translate(to_translate, 'nl', 'en')

test = "This paper covers the measuring of proficiency levels by comparing the linguistic complexity to that of a textbook at the given level. The language used in the textbooks is recorded per proficiency level , measured by the CEFR (Common European Framework of Reference for languages). This level goes from A to C, respectively being ranked from basic to proficient user. These grades can further be subdivided according to the needs of the local context. The idea behind this research method is that the model can read the input data from the student, normalize it to its basal form and compare the formatted text to the proficiency level. The main focus within this research paper was put on the correcting and normalizing of grammar mistakes, which led to greater performance within the network. This is not something which I think we should be focussing on right now, as this is mainly supposed to be a secondary feature, not something which we should direct all our time and resources towards. However, it is good to keep in mind that these things can still improve performance within NLP as a whole."
print(ARI(test))
print(flesch_reading_ease(test))
print(flesch_kincaid_grade(test))
