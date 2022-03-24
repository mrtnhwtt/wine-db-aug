import json
import uuid
import subprocess
from halo import Halo

spinner = Halo(text='', spinner='dots')
def parse_json():
    spinner.start()
    filename='test.json'
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
        vivino = get_vivino_info(wine["title"])
        if vivino:
            wine['price'] = vivino['price']
            wine['poster'] = vivino['img']
    with open('vin_db.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(content, ensure_ascii=False))
    spinner.text='Done.'
    spinner.succeed()

def get_vivino_info(name):
    subprocess.check_output(['node', 'vivino.js', '--name="' + name + '"'])
    with open('vivino-out.json', 'r') as f:
        content = json.loads(f.read())
        try:
            return {'img': content['vinos'][0]['thumb'], 'price': content['vinos'][0]['price']}
        except:
            return None
parse_json()