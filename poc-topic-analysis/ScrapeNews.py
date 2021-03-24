import http.client
import json
import os
import csv


class NewsArticleParts:
    title = ""
    content = ""
    categories = []
    url = ""

    def __init__(self, title, content, categories, url):
        self.title = title
        self.content = content
        self.categories = categories
        self.url = url

    def __iter__(self):
        return iter([self.title, self.content, self.url, self.categories])


if __name__ == "__main__":

    internalIds = []
    newsContents = []

    if not os.path.exists('newslist-truncated.txt'):
        # Write internal ID's to a file
        with open('data.json', encoding="utf8") as json_file:
            newsList = json.load(json_file)
            for stories in newsList["modules"]:
                for story in stories["stories"]:
                    internalIds.append(story["internalID"])
        print(internalIds)
        with open("newslist-truncated.txt", "w") as file:
            for internalId in internalIds:
                file.write('%s\n' % internalId)

    else:
        # If file with internal ID's already exists, read it and parse to list
        with open("newslist-truncated.txt", "r") as file:
            for line in file:
                currentPlace = line[:-1]
                internalIds.append(currentPlace)

    if not os.path.exists('newsContents.csv'):
        # Request complete article from internalID
        for internalId in internalIds:
            conn = http.client.HTTPSConnection("bloomberg-market-and-financial-news.p.rapidapi.com")
            headers = {
                'x-rapidapi-key': "e742c9502bmshac6c0aafce1871ap1b2ce7jsn267027f577df",
                'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com"
            }
            conn.request("GET", "/stories/detail?internalID={}".format(internalId), headers=headers)
            res = conn.getresponse()
            data = res.read()
            newsContentString = data.decode("utf8")
            newsContentObject = json.loads(newsContentString)

            # Extracting data
            title = newsContentObject["title"]
            url = newsContentObject["longURL"]
            content = ""
            for component in newsContentObject["components"]:
                if component["role"] == "p":
                    for componentPart in component["parts"]:
                        if componentPart["role"] == "text":
                            try:
                                content = content + " " + componentPart["text"]
                            except:
                                print("Couldnt add text")
                        if componentPart["role"] == "image":
                            content = content + " " + componentPart["caption"]
            categories = newsContentObject["contentTags"]
            newsContents.append(NewsArticleParts(title, content, categories, url))

        # Write list of news articles to CSV file
        with open("newsContents.csv", "w") as csvFile:
            writer = csv.writer(csvFile)
            for newsArticle in newsContents:
                writer.writerows({newsArticle.title, newsArticle.content, newsArticle.url, newsArticle.categories})