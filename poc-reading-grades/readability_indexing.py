import nltk
from nltk import SyllableTokenizer
from nltk.tokenize.repp import ReppTokenizer
from nltk.translate.bleu_score import sentence_bleu
import json
import requests
nltk.download('punkt')



url = 'https://api.mymemory.translated.net/get?'

def ARI(text: str) -> float:
    """
    Automated Readability Index
    Returns an approximation fo the grade required to comprehend the text
    with a grade between 1-14, where 1 is kindergarten and 14 is university graduate
    """
    words  = sum(c.isspace() for c in text) + 1
    characters = sum(c.isalpha() or c.isdigit() for c in text)
    sentences = len(nltk.sent_tokenize(text))
    pt1 = 4.71*float(characters/words)
    pt2 = 0.5*float(words/sentences)
    pt3 = -21.43
    return pt1 + pt2 + pt3

def flesch_kincaid_grade(text: str, dutch: bool)  -> float:
    """
    Flesch-kincaid grade level
    Returns a level between 0 and 18, seperated in
    levels of 3 
    """
    words = sum(c.isspace() for c in text) + 1
    sentences = len(nltk.sent_tokenize(text))
    syllables = count_syllables(text, dutch)  
    pt1 = 0.39*float(words/sentences)
    pt2 = 11.8*(syllables/words) - 15.59
    return pt1 + pt2

def flesch_reading_ease(text: str, dutch: bool)  -> float:
    """ 
    Flesch reading-ease score (FRES) 
    Scores between 0-100, where 100 is 
    easily understood and 0 is university graduate level
    """
    words = sum(c.isspace() for c in text) + 1
    sentences = len(nltk.sent_tokenize(text))
    syllables = count_syllables(text, dutch)
    pt1 = -1.015*float(words/sentences)
    pt2 = -84.6*float(syllables/words)
    return 206.835 + pt1 + pt2
    
def gunning_fog_index(text: str, dutch: bool) -> float:
    """
    Readability test for English writing
    Returns a score between 6 and 17, where 6 is sixth grade
    and 17 is a college graduate
    """ 
    words = sum(c.isspace() for c in text) + 1
    sentences = len(nltk.sent_tokenize(text))
    complex_syllables = count_syllables(text, dutch, 3)
    pt1 = (words/sentences)
    pt2 = 100+(complex_syllables/words)
    return 0.4*float(pt1+pt2)

def translate(totranslate: str, lang1: str, lang2: str):
    """
    Translates the translate value
    from lang1 to lang2, 
    which have to be noted according to ISO 639-1
    """
    translated = requests.get(url,  params = {'q': totranslate, 'source': lang1, 'target': lang2, 'langpair': lang1 + '|' + lang2, 'key': key})
    result = json.loads(translated.text)['responseData']['translatedText']
    return result


def count_syllables(text: str, dutch: bool, complexity = 0):
    """
    Counts the total syllables given 
    """
    syllables = 0
    for word in text.split(' '):
        if dutch:
            if nl_syllables(word) >= complexity:
                syllables += nl_syllables(word)
        else:
            if _syllables(word) >= complexity:
                syllables += _syllables(word)
    return syllables


# ENGLISH ONLY
def _syllables(word: str) -> int:
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


def nl_syllables(word: str) -> int:
    syllables = []
    syllable_count = 0
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    previouscut = 0
    if len(word) == 2: return 1
    for index in range(2, len(word)):
        if word[index-1] in consonants:
            if word[index-2] in vowels and word[index] in vowels:
                syllables.append(word[previouscut:index-1])
                previouscut = index-1
            if word[index-2] in vowels and word[index] in consonants:
                syllables.append(word[previouscut:index])
                previouscut = index
        if index == len(word)-1:
            syllables.append(word[previouscut:])
    return len(syllables)

def run_comparison(text1, text2):
    print("ARI: {ARI}".format(ARI=ARI(text1)))
    print("ARI (EN): {ARI}".format(ARI=ARI(text2)))
    print("FRE: {FRE}".format(FRE=flesch_reading_ease(text1, True)))
    print("FRE (EN): {FRE}".format(FRE=flesch_reading_ease(text2, False)))
    print("FKG: {FKG}".format(FKG=flesch_kincaid_grade(text1, True)))
    print("FKG (EN): {FKG}".format(FKG=flesch_kincaid_grade(text2, False)))
    print("GFI: {GFI}".format(GFI=gunning_fog_index(text1, True)))
    print("GFI (EN): {GFI}".format(GFI=gunning_fog_index(text2, False)))
    print("------------------------------------------")

if __name__ == '__main__':
    test_1 = "Ik ben makelaar in koffi, en woon op de Lauriergracht. Het is mijn gewoonte niet, romans te schrijven, of zulke dingen, en het heeft dan ook lang geduurd, voor ik er toe overging een paar riem papier extra te bestellen, en het werk aan te vangen, dat gij, lieve lezer, in de hand hebt genomen, en dat ge lezen moet als ge makelaar in koffie zijt, of als ge wat anders zijt. Niet alleen dat ik nooit iets schreef wat naar een roman geleek, maar ik houd er zelfs niet van, iets dergelijks te lezen."
    translated_1 = "I am a coffee broker and live on the Lauriergracht. It is not my habit to write novels or such things, and it took a long time before I proceeded to order a few extra reams of paper, and begin the work that you, dear reader, have in the hand, and that you should read if you are a broker in coffee, or if you are something else. Not only that I never wrote anything that looked like a novel, but I don't even like to read something like that."

    test_2 =  "De volle maan, tragisch dien avond, was reeds vroeg, nog in den laatsten dagschemer opgerezen als een immense, bloedroze bol, vlamde als een zonsondergang laag achter de tamarindeboomen der Lange Laan en steeg, langzaam zich louterende van hare tragische tint, in een vagen hemel op. Een doodsche stilte spande alom als een sluier van zwijgen, of, na de lange middagsiësta, de avondrust zonder overgang van leven begon."
    translated_2 = "The full moon, tragic that evening, had risen early in the last twilight as an immense, blood-pink sphere, blazed like a sunset low behind the tamarind trees of Lange Laan and rose, slowly purifying itself of its tragic hue, in a vague heaven. A dead silence stretched all over like a veil of silence, or, after the long afternoon siesta, the evening rest began without a transition of life." 

    test_3 = "Onbegrijpelijk veel mensen hebben familiebetrekkingen, vrienden of kennissen te Amsterdam. Het is een verschijnsel dat ik eenvoudig toeschrijf aan de veelheid der inwoners van die hoofdstad. Ik had er voor een paar jaren nog een verre neef. Waar hij nu is, weet ik niet. Ik geloof dat hij naar de West gegaan is. Misschien heeft de een of ander van mijn lezers hem wel brieven meegegeven. In dat geval hebben zij een nauwgezette, maar onvriendelijke bezorger gehad, als uit de inhoud van deze weinige bladzijden waarschijnlijk duidelijk worden zal." 
    translated_3 = "Incomprehensibly many people have family relationships, friends or acquaintances in Amsterdam. It is a phenomenon that I simply attribute to the multitude of inhabitants of that capital. I had a distant cousin there for a few years. I don't know where he is now. I believe he went to the West. Maybe some of my readers gave him letters. In that case they have had a conscientious but unfriendly delivery person, as will probably become apparent from the contents of these few pages."

    run_comparison(test_1, translated_1)
    run_comparison(test_2, translated_2)
    run_comparison(test_3, translated_3)