import pandas as pd
import csv
import re
from wordcloud import WordCloud
import gensim
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
import gensim.corpora as corpora
from tfidf import dfItf
import pyLDAvis.gensim_models


def remove_whitespace_and_punct(articles_df, column_to_make, column_input):
    articles_df[column_to_make] = articles_df[column_input].map(lambda x: re.sub('[,\.!?]', '', x))
    articles_df[column_to_make] = articles_df[column_to_make].map(lambda x: x.lower())


def create_wordcloud_to_png(articles_df, column, file_name):
    long_string = ','.join(list(articles_df[column].values))
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
    wordcloud.generate(long_string)
    wordcloud.to_file(file_name)


def sent_to_words(sentences):
    for sentence in sentences:
        yield gensim.utils.simple_preprocess(str(sentence), deacc=True)


def remove_stopwords(text_stopwords):
    return [[word for word in simple_preprocess(str(doc))
             if word not in stop_words] for doc in text_stopwords]


if __name__ == '__main__':
    nltk.download('stopwords')

    articlesListOfDicts = []
    with open('newsContents.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            row_len = len(row)
            if row_len != 0:
                articlesListOfDicts.append({"title": row[0], "content": row[1]})

    articlesDF = pd.DataFrame(articlesListOfDicts)

    remove_whitespace_and_punct(articlesDF, 'title_processed', 'title')
    remove_whitespace_and_punct(articlesDF, 'content_processed', 'content')

    create_wordcloud_to_png(articlesDF, 'content_processed', 'wordcloud-content.png');
    create_wordcloud_to_png(articlesDF, 'title_processed', 'wordcloud-title.png');

    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

    data = articlesDF.content_processed.values.tolist()
    data_words = list(sent_to_words(data))
    data_words = remove_stopwords(data_words)
    scoredDocs = dfItf(data_words)
    id2word = corpora.Dictionary(scoredDocs)
    texts = scoredDocs
    corpus = [id2word.doc2bow(text) for text in texts]

    num_topics = 5
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_topics)
    topics = lda_model.print_topics()
    print(topics)
    lda_models = lda_model[corpus[0]]


    visualisation = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
    pyLDAvis.save_html(visualisation, './test-' + str(num_topics) + '.html')

