import math
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def dfItf(documents):
    documentsString = []
    for document in documents:
        documentsString.append(" ".join(document))

    vectorizer = TfidfVectorizer(max_df=.65, min_df=1, stop_words=None, use_idf=True, norm=None, )
    transformed_documents = vectorizer.fit_transform(documentsString)
    transformed_documents_as_array = transformed_documents.toarray()
    docsWithRelevantWords = []
    for counter, doc in enumerate(transformed_documents_as_array):
        tf_idf_tuples = list(zip(vectorizer.get_feature_names(), doc))
        one_doc_as_df = pd.DataFrame.from_records(tf_idf_tuples, columns=['term', 'score']).sort_values(by='score', ascending=False).reset_index(drop=True)
        highestScore = one_doc_as_df.iloc[0]["score"]
        docRelevantWords = []
        for index, row in one_doc_as_df.iterrows():
            for i in range(math.floor(row["score"])):
                docRelevantWords.append(row["term"])
            if index > 300:
                break
        docsWithRelevantWords.append(docRelevantWords)

    return docsWithRelevantWords