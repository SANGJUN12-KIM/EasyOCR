import easyocr
import json
import time
import os
from difflib import SequenceMatcher
from collections import OrderedDict
from jamo import h2j, j2hcj
from os.path import join

def recognition_rate_check(extracted_detail0_list):
    #인식된 문장을 공백 단위로 슬라이싱
    slicedResult = "".join(extracted_detail0_list)
    slicedResult = slicedResult.split()
    print("추출된 텍스트: \n", slicedResult)

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
    #print("인식률 비교를 위한 원본 텍스트: \n", slicedOriginal)

    #OCR결과물과 원본의 예상 오차 비율(공백 무시)
    originalString = "".join(slicedOriginal)
    extractedString = "".join(slicedResult)

    print("\nSequenceMatcher를 통한 어절단위 일치도: ", SequenceMatcher(lambda x: x == " ", originalString, extractedString).ratio())

    #print("\n어절 단위 OCR결과물 중 원본과의 불일치 요소 출력")
    differenceOCR = []
    differenceOriginal = []
    for i in slicedResult:
        if i not in slicedOriginal:
            differenceOCR.append(i)
    for i in slicedOriginal:
        if i not in slicedResult:
            differenceOriginal.append(i)
    #print("원본", differenceOriginal)
    #print("추출본", differenceOCR)

    #print("원본의 전체 어절 수: ", len(slicedOriginal))
    #print("추출본의 전체 어절 수: ", len(slicedResult))

    #print("\n어절 단위 OCR결과물 중 원본과의 불일치 요소 출력")
    syllableOriginalString = "".join(differenceOriginal)
    syllableExtractedString = "".join(differenceOCR)

    syllableDifferenceOCR=[]
    syllableDifferenceOriginal=[]
    syllableCorrectOCR = []
    for i in syllableOriginalString:
        if i not in syllableExtractedString:
            syllableDifferenceOriginal.append(i)
    for i in syllableExtractedString:
        if i not in syllableOriginalString:
            syllableDifferenceOCR.append(i)
    for i in syllableOriginalString:
        if i in syllableExtractedString:
            syllableCorrectOCR.append(i)
    #print('음절 단위 일치요소: ', syllableCorrectOCR)
    #print('\n원본 전체 음절 수(originalString): ', len(originalString))
    #print('추출본 전체 음절 수(extractedString):', len(extractedString))
    #print('\n원본 음절 단위 불일치 요소:', syllableDifferenceOriginal)
    #print('추출본 음절 단위 불일치 요소', syllableDifferenceOCR)

    syllableRecall = (len(syllableCorrectOCR)/len(syllableOriginalString)) * 100
    syllablePrecision = (len(syllableCorrectOCR)/len(syllableExtractedString)) * 100

    print("\n음절 단위 recall: ", syllableRecall, "%")
    print("음절 단위 precision: ", syllablePrecision, "%")

    #print("\n음소 단위 OCR결과물 중 원본과의 불일치 요소 출력")
    phonemeOriginalString = j2hcj(h2j(syllableOriginalString))
    phonemeExtractedString = j2hcj(h2j(syllableExtractedString))

    phonemeDifferenceOCR = []
    phonemeDifferenceOriginal = []
    phonemeCorrectOCR = []
    for i in phonemeOriginalString:
        if i not in phonemeExtractedString:
            phonemeDifferenceOriginal.append(i)
    for i in phonemeExtractedString:
        if i not in phonemeOriginalString:
            phonemeDifferenceOCR.append(i)
    for i in phonemeOriginalString:
        if i in phonemeExtractedString:
            phonemeCorrectOCR.append(i)

    #print('음소 단위 일치요소: ', phonemeCorrectOCR)
    #print('원본 음소 단위 불일치 요소:', phonemeDifferenceOriginal)
    #print('추출본 음소 단위 불일치 요소', phonemeDifferenceOCR)

    phonemeRecall = (len(phonemeCorrectOCR) / len(phonemeOriginalString)) * 100
    phonemePrecision = (len(phonemeCorrectOCR) / len(phonemeExtractedString)) * 100

    print("\n음소 단위 recall: ", phonemeRecall, "%")
    print("음소 단위 precision: ", phonemePrecision, "%")

def create_json_file(extracted_data_list, image_name):
    file_name = image_name
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

    root_dir = join('./', 'OCRresults')
    if os.path.isdir(root_dir) == False:
        os.mkdir(root_dir)
    os.chdir(root_dir)
    with open(file_name + '.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
    os.chdir(os.path.join(os.pardir))


for image_file in os.listdir('./target_pages/'):
    start = time.time()

    IMAGE_PATH = './target_pages/'+ image_file
    print("\n\n파일 명: ", IMAGE_PATH)

    reader = easyocr.Reader(['en', 'ko'], gpu=False)
    result = reader.readtext(IMAGE_PATH, paragraph=True)
    result_for_test = reader.readtext(IMAGE_PATH, detail=0, paragraph=True)
    print(result_for_test)
    recognition_rate_check(result_for_test)
    create_json_file(result, image_file)
    print("수행시간 :", time.time() - start, "초\n\n")
    
    print("학습모델 적용")
    start = time.time()

    reader = easyocr.Reader(['ko', 'en'], gpu=False, model_storage_directory='user_network',
                        user_network_directory='user_network', recog_network='custom')
    result = reader.readtext(IMAGE_PATH, paragraph=True)
    result_for_test = reader.readtext(IMAGE_PATH, detail=0, paragraph=True)
    recognition_rate_check(result_for_test)
    create_json_file(result, image_file)

    print("수행시간 :", time.time() - start, "초")
