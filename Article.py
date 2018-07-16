from bs4 import BeautifulSoup as bs
import urllib
import pandas as pd


def get_article(query):
    return bs(urllib.request.urlopen(query), 'html.parser').find("section", attrs={"class":"sidebar_1"})

class Article(object)  :
    def __init__(self, article_soup):
        self.article = article_soup
        self.author = self.get_author()
        self.datetime = self.get_datetime()
        self.text = self.get_text()
        self.synopsis = self.get_synopsis()
        self.imgs = self.get_imgs() #This is a tuple of (alt, src)
        self.videos = self.get_videos()
        self.title = self.article.title[1]

    def get_author(self):
        return self.article.strong.get_text()

    def get_datetime(self):
        return self.article.span.get_text()

    def get_text(self):
        article_text = ''
        for text in self.article.find_all('p', attrs={'class':'Normal'}):
            article_text+= text.get_text()
        return article_text.replace('\t', '').replace(u'\xa0', u' ').replace('\n','')

    def get_synopsis(self):
        return self.article.h2.get_text()

    def get_imgs(self):
        return {'alt': [img['alt'] for img in self.article.find_all('img')], 'src': [img['src'] for img in self.article.find_all('img')]}

    def get_videos(self):
        return [video['data-src'] for video in self.article.find_all('video')]


class Articles(object):
    def __init__(self, articles_list):
        self.articles_list = articles_list

        self.titles = []
        self.links = []
        self.ids = []
        self.authors = []
        self.datetime = []
        self.text = []
        self.synopses = []
        self.img_alts = []
        self.img_links = []
        #current_article
        self.video_links = []

    def generate_articles_content(self):

        for link in self.articles_list.link:
            current_art = Article(get_article(link))

            self.titles.append(self.articles_list.title[self.articles_list.link == link].values[0])
            self.links.append(link)
            self.ids.append(self.articles_list.loc[self.articles_list.link == link].values[0])
            self.authors.append(current_article.author)
            self.datetime.append(current_article.datetime)
            self.text.append(current_article.text)
            self.synopses.append(current_article.synopses)
            self.img_alts.append(current_article.imgs['alt'])
            self.img_links.append(current_article.imgs['src'])
            self.video_links.append(current_article.videos)

        return len(self.titles) == len(self.links) == len(self.ids) == len(self.authors) == len(self.datetime) == len(self.text) == len(self.synopses) == len(self.img_alts) == len(self.img_links) == len(self.video_links)


    def generate_articles_content_dict(self):

        if self.generate_articles_content():

            return {'title': self.titles, #From filtered_result object
                     'link':self.links, #in Articles object
                     'id': self.ids, #from filtered_result object
                     'author': self.authors, #attr of Article Object
                     'datetime': self.datetime,
                     'text': self.text,
                     'synopsis': self.synopses,
                     'img_alt': self.img_alts,
                     'img_link': self.img_links,
                     #'video_alt': self.video_alts,
                     'video_link': self.video_links}

        else: return {}