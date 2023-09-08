import requests
from bs4 import BeautifulSoup

def get_article_details(id='29284222'):
    #Scraping setup
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    cited_url = "https://pubmed.ncbi.nlm.nih.gov/?linkname=pubmed_pubmed_citedin&from_uid="
    #article_id = '29284222'

    # HTTP request
    response_article = requests.get(f'{base_url}{str(id)}')
    response_cited = requests.get(f'{cited_url}{str(id)}')

    # HTML parser
    soup_article = BeautifulSoup(response_article.text, "html.parser")
    soup_cited = BeautifulSoup(response_cited.text, "html.parser")

    # getting the header
    header = soup_article.find("header", class_="heading")

    # check there's data, if not return an empty dictionnaire
    if header == None:
        return {'title':'', 'publication date':'', 'cited count': '' ,'authors':''}

    # Article Title
    try:
        article_title = header.find('h1', class_="heading-title").get_text().strip()
    except:
        article_title = ''

    # publication date with expcetiong for error handling due to different format
    try:
        pub_date = header.find("span", class_="secondary-date").get_text().strip()
    except:
        pub_date = header.find("span", class_="cit").get_text().strip()
    finally:
        pub_date = None

    #getting article cited count
    try:
        article_cited = soup_cited.find("span", class_="value").get_text()
    except:
        article_cited = 0

    # Authors
    try:
        authors_list = header.find("div", class_="authors-list").find_all("span", class_="authors-list-item")
    except:
        authors_list = None

    # looping throug the authors list to extarct each author
    list = []
    if not authors_list == None:
        for a in authors_list:
            author_name = a.find("a", class_="full-name").attrs['data-ga-label']
            try:
                author_title= a.find("a", class_="affiliation-link").attrs['title']
            except:
                author_title = None
            list.append({'author':author_name,'title':author_title})
    else:
        list.append({'author':None,'title':None})

    article_details = {'article_title':article_title, 'article_pub_date':pub_date, 'article_cited': article_cited ,'authors':list}

    return article_details
