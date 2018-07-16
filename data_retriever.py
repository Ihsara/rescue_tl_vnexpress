from bs4 import BeautifulSoup as bs
import urllib
import pandas as pd


query_str = 'https://vnexpress.net/category/day/page/{}.html?cateid=1001002&fromdate=1529964000&todate=1531517760&allcate=1001002|1001002|'
#query_str = "https://vnexpress.net/chien-dich-giai-cuu/tag-810752-1.html"

def get_articles(query):
    return bs(urllib.request.urlopen(query), 'html.parser').find("section", attrs={"class":"sidebar_1"}).find_all("article",attrs={"class":"list_news"})

def distribute_articles(articles, return_type='df'):
    article_dict = {'title': [],
             'link': [],
               'description': [],
               'id' : []}

    for article in articles:
        #article_dict['title'].append(article.a.get('title')) # if this does not work, use the one below
        article_dict['title'].append(article.img.get('alt'))
        article_dict['link'].append(article.a.get('href'))
        article_dict['description'].append(article.h4.get_text())
        article_dict['id'].append(article.a.get('href').split('-')[-1][:-5])
    if return_type == 'df':
        return pd.DataFrame(data=article_dict)

    elif return_type == 'dict':
        return article_dict

df_list = []

for page in range(1, 23):
    page_url = query_str.format(str(page))
    articles = get_articles(page_url)
    df_list.append( distribute_articles(articles))

result = pd.concat(df_list).reset_index(drop=True)

kws = ['Thái Lan', 'đội bóng', 'Đội bóng', 'hang', 'mắc kẹt', 'thiếu niên']
temp = []
kw_filtered = []

for kw in kws:
    for title in result.title:
        if kw in title:
            temp.append(title)

    kw_filtered.append(pd.concat([result[result.title == tmp] for tmp in temp]))
    temp =[ ]#pd.DataFrame(columns = ['title', 'link','description','id'])

filtered_result = pd.concat(kw_filtered).drop_duplicates().reset_index(drop = True)