import requests
from bs4 import BeautifulSoup

# def extract_page_info(page_link):
#     try:
#         response = requests.get(page_link)
#         response.raise_for_status()
        
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         og_title = soup.find('meta', property='og:title')
#         og_description = soup.find('meta', property='og:description')
        
#         if og_title and og_description:
#             page_title = og_title['content']
#             page_description = og_description['content']
#         else:
#             page_title = soup.title.string if soup.title else ''
#             meta_description = soup.find('meta', {'name': 'description'})
#             page_description = meta_description['content'] if meta_description else ''
        
#         return page_title, page_description
#     except Exception as e:
#         return None, None


def extract_page_info(page_link):
    try:
        response = requests.get(page_link)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        og_data = {}
        for tag in soup.find_all('meta', property=True):
            property_name = tag['property']
            if property_name.startswith('og:'):
                og_property = property_name[3:]
                og_data[og_property] = tag['content']
                
        if og_data:
            return og_data

        meta_description = soup.find('meta', {'name': 'description'})
        title = soup.find('title')
        
        data = {}
        
        meta_description = meta_description['content']
        title = title.string
        
        data = {
            'description': meta_description,
            'title': title
            }

        return data
    except Exception as e:
        return None