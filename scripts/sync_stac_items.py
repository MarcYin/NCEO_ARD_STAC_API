import os
import json
import requests
from retry import retry
import concurrent.futures

STAC_API_URL = 'https://gws-access.jasmin.ac.uk/public/nceo_ard/NCEO_ARD_STAC_API/UK-sentinel-2/'
STAC_DIR = './STAC/'

def download_collection_info():
    """
    Download the collection information from the STAC API and write it into a file
    """
    response = requests.get(os.path.join(STAC_API_URL, 'collection.json'))
    collection = response.json()
    
    with open(os.path.join(STAC_DIR, 'collection.json'), 'w') as file:
        json.dump(collection, file)

@retry(tries=10, delay=1, backoff=2)
def download_tile(tile):
    """
    Download a tile if it doesn't exist already and return its path
    Arguments:
    tile -- tile information from the STAC API
    """
    item_path = os.path.join(STAC_DIR, tile['href'])
    
    if not os.path.exists(item_path):
        response = requests.get(os.path.join(STAC_API_URL, tile['href'][1:]))
        item = response.json()
        print(tile)
        
        item_path = os.path.join(STAC_DIR, f"{item['id']}.json")
        with open(item_path, 'w') as file:
            json.dump(item, file)

        return item_path
    
    else:
        print('Item exists.')
        return None

def download_tiles(tiles):
    """
    Download the specified tiles using a ThreadPoolExecutor
    Arguments:
    tiles -- list of tiles to be downloaded
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        return list(filter(None, executor.map(download_tile, tiles)))

if __name__ == "__main__":
    download_collection_info()
    collection_file_path = os.path.join(STAC_DIR, 'collection.json')
    
    with open(collection_file_path) as collection_file:
        collection = json.load(collection_file)
        
    tiles = collection['links'][1:100]
    new_items = download_tiles(tiles)
