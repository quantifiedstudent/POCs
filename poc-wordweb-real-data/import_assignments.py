import json
import gensim
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
import re
from bs4 import BeautifulSoup
from tfidf import dfItf
from wordcloud import WordCloud
from nltk.stem import WordNetLemmatizer


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


def get_text_from_all_courses_assignments(json_file_name):
    with open(json_file_name, encoding="utf8") as json_file:
        parsed_json = json.load(json_file)
    assignments_all_text = []
    for course in parsed_json:
        for assignment in parsed_json[course]:
            hand_ins_list = parsed_json[course][assignment]
            if hand_ins_list["hand-ins"]:
                if hand_ins_list["hand-ins"][0] is not None:
                    hand_in_last = hand_ins_list["hand-ins"][len(hand_ins_list) - 1]
                    assignments_all_text.append(hand_in_last["text"])
    return assignments_all_text


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
    wordcloud = WordCloud(background_color="white", contour_width=3, contour_color='steelblue', repeat=False,
                          max_words=max_words, collocations=False)
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


def remove_verbs_from_documents(list_of_documents):
    lemmatizer = WordNetLemmatizer()
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    processed_list_of_documents = []
    for document in list_of_documents:
        document_string = document
        if isinstance(document, list):
            document_string = ""
            for sentence in document:
                document_string += sentence
        removed_verbs_document = ""
        words = nltk.word_tokenize(document_string)
        words_tagged = nltk.pos_tag(words)
        for word, tag in words_tagged:
            if word not in ["service", "name", "server", "document", "research", "date"]:
                if tag not in ["WP", "VBZ", "VBP", "VBN", "VBD", "VBG", "VB", "MD"]:
                    removed_verbs_document += word + " "
        processed_list_of_documents.append(removed_verbs_document)
    return processed_list_of_documents


assignment_list = extract_text_from_canvas_assignments_json("assignments.json")
assignments_all_courses_list = remove_verbs_from_documents(get_text_from_all_courses_assignments("test.json"))

generate_wordweb_from_assignments_list_with_tfidf(assignments_all_courses_list, "max-with-itf-submissions-filtered",
                                                  "png", 75)
generate_wordweb_from_assignments_list_without_tfidf(assignments_all_courses_list,
                                                     "max-without-itf-smaller-submissions-filtered", "png", 75)
