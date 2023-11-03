from PIL import Image,ImageOps
from pathlib import Path
from os import listdir,remove
from uuid import uuid1
import warnings
import random
from json import load
warnings.filterwarnings('ignore')


def loadimages2() -> list:
    with open(r'config.json', 'r', encoding='utf-8') as f:
        configs = load(f)
    excludelist = configs['中獎人員名單']
    folderpath = Path('Photos')
    for imgfilename in listdir(folderpath):
        imgfilepath = folderpath / imgfilename

        if imgfilepath.suffix != '.JPEG':
            try:
                im = Image.open(imgfilepath)
            except Exception as e:
                print(imgfilepath,repr(e))
            else:
                im = im.convert(mode='RGB')
                old_height = im.height
                old_width = im.width
                if old_height > old_width or old_width <3840 or old_height <2160:
                    im.close()
                    remove(imgfilepath)
                    continue
                new_height = int(old_height * (3840/old_width))
                new_width = int(old_width * (2160/old_height))
                if new_width > 3840:
                    im = im.resize((new_width,2160))
                    im = im.crop(box=(int((new_width - 3840)/2),0,3840,2160))
                    im.save(folderpath / f'{uuid1().hex}.JPEG', 'JPEG')
                elif new_height >2160:
                    im = im.resize((3840, new_height))
                    im = im.crop(box=(0,int((new_height - 2160) / 2), 3840, 2160))
                    im.save(folderpath / f'{uuid1().hex}.JPEG', 'JPEG')
                else:
                    im = im.resize((3840, int(old_height *(3840/old_width))))
                    im = im.crop(box=(0,int((im.height - 2160) / 2),3840,2160))
                    im.save(folderpath / f'{uuid1().hex}.JPEG','JPEG')
                im.close()
                remove(imgfilepath)

    pictures =[str(folderpath / _) for _ in listdir(folderpath)]
    for exclude in excludelist:
        if exclude in pictures:
            pictures.remove(exclude)
    random.shuffle(pictures)
    return pictures

def loadimages() -> list:
    with open(r'config.json', 'r', encoding='utf-8') as f:
        configs = load(f)
    excludelist = configs['中獎人員名單']
    folderpath = Path('Photos')
    pictures =[str(folderpath / _) for _ in listdir(folderpath)]
    for exclude in excludelist:
        if exclude in pictures:
            pictures.remove(exclude)
    random.shuffle(pictures)
    return pictures


if __name__ == '__main__':
    loadimages2()

