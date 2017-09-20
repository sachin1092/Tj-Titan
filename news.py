from constants import news_creds

import requests

def get_news():
	r = requests.get(news_creds.get('url'))
	data = r.json()
	news = [item.get('source', {}).get('enriched', {}).get('url', {}).get('title', "") for item in data.get('docs', [])]
	return ",".join(news)


if __name__ == '__main__':
	print get_news()