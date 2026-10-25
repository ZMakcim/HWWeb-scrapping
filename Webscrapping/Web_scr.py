import requests
from bs4 import BeautifulSoup

# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = 'https://habr.com/ru/articles/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0 Safari/537.36'
}

response = requests.get(URL, headers=HEADERS)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Находим все превью статей на странице
articles = soup.find_all('article')

for article in articles:
    # Заголовок и ссылка
    title_tag = article.find('h2')
    if not title_tag:
        continue
    link_tag = title_tag.find('a')
    if not link_tag:
        continue
    title = link_tag.get_text(strip=True)
    link = link_tag.get('href')
    if link and link.startswith('/'):
        link = 'https://habr.com' + link

    # Дата публикации
    date_tag = article.find('time')
    date = date_tag.get('datetime', '') if date_tag else ''

    # Вся доступная preview-информация (заголовок + текст превью)
    preview_text = article.get_text(separator=' ', strip=True).lower()

    # Проверяем, встречается ли хотя бы одно ключевое слово
    if any(keyword.lower() in preview_text for keyword in KEYWORDS):
        print(f'{date} – {title} – {link}')