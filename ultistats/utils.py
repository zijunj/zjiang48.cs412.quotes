# ultistats/utils.py

# utils.py

import requests
from bs4 import BeautifulSoup

def scrape_college_news():
    url = 'https://usaultimate.org/college/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Each article is inside a <article> tag with class like 'news-article-0', etc.
    articles = soup.select('div.news-grid article')

    news_items = []

    for article in articles[:5]:  # Limit to top 5
        a_tag = article.select_one('a.article-link')
        title_tag = article.select_one('.headline h4')

        if a_tag and title_tag:
            title = title_tag.get_text(strip=True)
            link = a_tag['href']
            news_items.append({
                'title': title,
                'link': link
            })

    return news_items
