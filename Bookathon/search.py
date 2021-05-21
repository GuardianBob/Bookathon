import json
import requests
from googleapiclient.discovery import build
from django.conf import settings

def get_books_data(query):
    service = build('books', 'v1', developerKey=settings.BOOKS_API)   

    request = service.volumes().list(q=query)
    print(service)
    response = request.execute()
    
    book_list = [response['items'][item]['volumeInfo']for item in range(len(response['items']))]
    book_list2 = []
    for item in response['items']:
        authors = []
        for author in item['volumeInfo']['authors']:
            authors.append(author)
        book_list2.append(
            {'id' : item['id'], 
            'title': item['volumeInfo']['title'],
            'authors': authors,
            'posterImg': item['volumeInfo']['imageLinks']['thumbnail'],
            'link': item['selfLink'],
            # 'rating': item['volumeInfo']['averageRating'],
            }
        )
    return book_list2      

def search_filters(query):
    pass