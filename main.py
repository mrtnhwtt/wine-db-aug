import json
import uuid
from halo import Halo
from bs4 import BeautifulSoup
import urllib.request

def get_image_from_name(name):
    try:
        url = f'https://www.vivino.com/search/wines?q={urllib.parse.quote(name)}'
        with urllib.request.urlopen(url) as webPageResponse:
            outputHtml = webPageResponse.read()
        getpage_soup= BeautifulSoup(outputHtml, 'html.parser')
        all_class_topsection= getpage_soup.findAll('figure', {'class':'wine-card__image'})
        style = str(all_class_topsection[0]['style'])
        img = style.replace('background-image: url(', 'https:')[:-1]
        return img
    except:
        return None

spinner = Halo(text='', spinner='dots')
def parse_json():
    spinner.start()
    filename='winemag.json'
    content = ''
    with open(filename, 'r') as f:
        content = json.loads(f.read())
    for wine in content:
        spinner.text = f'Working on {wine["title"]}...'
        wine['id'] = str(uuid.uuid4())
        wine.pop('taster_name')
        wine.pop('taster_twitter_handle')
        wine.pop('points')
        wine.pop('region_2')
        wine['poster'] = 'https://butler-academy.com/wp-content/uploads/2019/03/vin2.png'
        vivino = get_image_from_name(wine["title"])
        if vivino:
            wine['poster'] = vivino
    with open('vin_db.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(content, ensure_ascii=False))
    spinner.text='Done.'
    spinner.succeed()

parse_json()