import easyocr
import json
import os
from collections import OrderedDict
from os.path import join

def create_json_file(extracted_data, image_name):
    file_name = image_name
    file_data = OrderedDict()
    file_data['page'] = 1
    item_list = []
    for id, (area, text) in enumerate(extracted_data):
        item = {}
        item['id'] = id + 1
        item['type'] = 'text'
        item['area'] = area
        item['content'] = text
        item_list.append(item)
    file_data['object'] = item_list

    root_dir = join('./', 'OCRresults')
    if os.path.isdir(root_dir) == False:
        os.mkdir(root_dir)
    os.chdir(root_dir)
    with open(file_name + '.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
    os.chdir(os.path.join(os.pardir))

def image2text(image_path = './target_pages/', custom_model = 'False', create_json = 'True'):
    for image_file in os.listdir(image_path):
        IMAGE_PATH = image_path + image_file
        if custom_model =='True':
            reader = easyocr.Reader(['ko', 'en'], gpu=True, model_storage_directory='user_network',
                        user_network_directory='user_network', recog_network='custom')
        else:
            reader = easyocr.Reader(['ko', 'en'], gpu=True)
        result = reader.readtext(IMAGE_PATH, paragraph=True)
        if create_json == 'True':
            create_json_file(result, image_file)

if __name__ == '__main__':
    image2text()
    image2text(custom_model='True', create_json='False')