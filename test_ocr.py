import easyocr
import json
from difflib import SequenceMatcher
from collections import OrderedDict

def recognition_rate_check(extracted_detail0_list):
    #인식된 문장을 공백 단위로 슬라이싱
    slicedResult = "".join(extracted_detail0_list)
    slicedResult = slicedResult.split()
    print(slicedResult)

    #원본을 공백 단위로 슬라이싱, 가운뎃점 제거"
    with open("OriginalTXT.txt", "r") as tf:
        originalText = []
        for line in tf:
            originalText.append(line)

    dotConvOriginal = []
    for i in originalText:
        dotFind = i.replace("·", " ")
        dotConvOriginal.append(dotFind)

    slicedOriginal = "".join(dotConvOriginal)
    slicedOriginal = slicedOriginal.split()
    print(slicedOriginal)

    #OCR결과물과 원본의 예상 오차 비율(공백 무시)
    originalString = "".join(slicedOriginal)
    extractedString = "".join(slicedResult)

    print("OCR결과물과 원본의 예상 오차 비율(공백 무시): ", SequenceMatcher(lambda x: x == " ", originalString, extractedString).ratio())


def json_file_creation(extracted_data_list):
    file_data = OrderedDict()
    file_data['page'] = 1
    item_list = []
    for id, (area, text) in enumerate(extracted_data_list):
        item = {}
        item['id'] = id + 1
        item['type'] = 'text'
        item['area'] = area
        item['content'] = text
        item_list.append(item)
    file_data['object'] = item_list
    with open('page_.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")


IMAGE_PATH = 'OCRtestImage.png'
reader = easyocr.Reader(['ko', 'en'], gpu=False)  # need to run only once to load model into memory
result = reader.readtext(IMAGE_PATH, paragraph=True)
result_for_test = reader.readtext(IMAGE_PATH, detail=0, paragraph=True)

recognition_rate_check(result_for_test)
json_file_creation(result)



