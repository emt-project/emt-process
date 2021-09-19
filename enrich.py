import glob
import os
import pandas as pd

from PIL import Image

IMG_GLOB = os.environ.get('IMG', '/home/csae8092/Documents/kem_img/kem-img-process/*/*.jpg')
IMG_LIST = glob.glob(IMG_GLOB)
GESAMT_DF = pd.read_csv('gesamt_liste.csv')


def yield_img_dict(images):
    for x in images:
        item = {}
        item['Dateiname'] = os.path.basename(x)
        item['folder'] = os.path.basename(os.path.split(x)[0])
        with Image.open(x) as image:
            item['width'], item['height'] = image.width, image.height
        yield item


images = sorted(IMG_LIST)
size_df = pd.DataFrame(yield_img_dict(images), columns=['Dateiname', 'folder', 'width', 'height'])
new = pd.merge(GESAMT_DF, size_df)
new.to_csv('enriched_gesamt.csv', index=False)
