import json, urllib.request
import requests
from googleapiclient.discovery import build
from django.conf import settings

def get_books_data(query):
    service = build('books', 'v1', developerKey=settings.BOOKS_API)   

    request = service.volumes().list(q=query)
    response = request.execute()
    service.close() # Close the service to avoid leaving sockets open - security risk
    # This next line returns the results but without each book's ID or individual info link
    # book_list = [response['items'][item]['volumeInfo']for item in range(len(response['items']))]
    
    # Solution to return book ID and info Link along with other details.
    book_list = []
    for item in response['items']:
        authors = []
        for author in item['volumeInfo']['authors']:
            authors.append(author)
        book_list.append(
            {'id' : item['id'], 
            'title': item['volumeInfo']['title'],
            'authors': authors,
            'posterImg': item['volumeInfo']['imageLinks']['thumbnail'],
            'link': item['selfLink'],
            # 'rating': item['volumeInfo']['averageRating'],
            }
        )
    return book_list   

def parse_book_info(url):
    with urllib.request.urlopen(f"{url}") as url:
        data = json.loads(url.read().decode())
        print(data)
    return data

def search_filters(query):
    pass
