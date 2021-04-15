import json
import gensim
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
import re
from bs4 import BeautifulSoup
from tfidf import dfItf
from wordcloud import WordCloud


def remove_whitespace_and_punct(list_assignments_text):
    processed = []
    for assignment in list_assignments_text:
        processed.append(re.sub('[,.!?]', '', assignment))
    return processed


def doc_to_words(docs):
    for doc in docs:
        yield gensim.utils.simple_preprocess(str(doc), deacc=True)


def remove_stopwords(text_stopwords):
    nltk.download('stopwords')
    stop_words = stopwords.words('dutch')
    return [[word for word in simple_preprocess(str(doc))
             if word not in stop_words] for doc in text_stopwords]


def extract_text_from_canvas_assignments_json(json_file_name):
    with open(json_file_name, encoding="utf8") as json_file:
        parsedJson = json.load(json_file)
    assignmentsAllText = []
    for assignment in parsedJson:
        assignmentAllText = ""
        if "name" in assignment:
            assignmentAllText += " " + assignment["name"]
        if "description" in assignment:
            if assignment["description"]:
                assignmentAllText += " " + BeautifulSoup(assignment["description"], "lxml").get_text()
        if "rubric" in assignment:
            for criteria in assignment["rubric"]:
                assignmentAllText += " " + criteria["description"]

                if "ratings" in criteria:
                    for rating in criteria["ratings"]:
                        assignmentAllText += " " + rating["long_description"]
            assignmentsAllText.append(assignmentAllText)
    return assignmentsAllText


def scored_assignments_with_tfidf(assignments_list):
    processed_assignments = doc_to_words(assignments_list)
    processed_assignments = remove_stopwords(remove_stopwords(processed_assignments))
    processed_assignments = dfItf(processed_assignments)
    all_words_scored = []
    for document in processed_assignments:
        string_document = ' '.join(document)
        all_words_scored.append(string_document)
    all_words_scored = " ".join(all_words_scored)
    return all_words_scored


def create_wordcloud(words, file_name, file_extension, max_words):
    wordcloud = WordCloud(background_color="white", max_words=max_words, contour_width=3, contour_color='steelblue')
    wordcloud.generate(words)
    wordcloud.to_file(file_name + "." + file_extension)


def generate_wordweb_from_assignments_list_with_tfidf(assignments_list, file_name, file_extension, max_words):
    words = scored_assignments_with_tfidf(assignments_list)
    create_wordcloud(words, file_name, file_extension, max_words)

def generate_wordweb_from_assignments_list_without_tfidf(assignments_list, file_name, file_extension, max_words):
    processed_assignments = doc_to_words(assignments_list)
    processed_assignments = remove_stopwords(remove_stopwords(processed_assignments))
    all_words_scored = []
    for document in processed_assignments:
        string_document = ' '.join(document)
        all_words_scored.append(string_document)
    all_words_scored = " ".join(all_words_scored)
    create_wordcloud(all_words_scored, file_name, file_extension, max_words)


assignment_list = extract_text_from_canvas_assignments_json("assignments.json")

generate_wordweb_from_assignments_list_with_tfidf(assignment_list, "max-with-itf", "png", 20)
generate_wordweb_from_assignments_list_without_tfidf(assignment_list, "max-without-itf-smaller", "png", 20)
