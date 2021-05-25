import json, urllib.request, ssl
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
    data_keys = {'title' : 'title', 'google_link':'previewLink', 'description':'description', 
    'categories':'categories', 'avg_rating':'averageRating', 'total_ratings':'ratingsCount'}    
    with urllib.request.urlopen(f"{url}") as url:
        data = json.loads(url.read().decode())
        # print(data['volumeInfo']['title'])
        authors = []
        if 'authors' in data['volumeInfo']:            
            for author in data['volumeInfo']['authors']:
                authors.append(author)
        book_info = {
            'id': data['id'],
            'authors': authors,
            'json_link': data['selfLink'],
        }
        if 'imageLinks' in data['volumeInfo']: book_info.update({'posterImg': data['volumeInfo']['imageLinks']['thumbnail'],})
        # Calling JSON keys causes errors if they don't exist: this solves that.
        for key, val in data_keys.items():
            if val in data['volumeInfo']:
                book_info.update({ f'{key}' : data['volumeInfo'][val], })
        # print('info here: ', book_info)
    return book_info

def search_filters(query):
    pass
