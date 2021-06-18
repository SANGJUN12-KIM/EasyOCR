# EasyOCR for NIA-solution_for_social_issue
***
* 원본 소스: <https://github.com/JaidedAI/EasyOCR>
* 실행 코드: SANGJUN12-KIM/EasyOCR/run.py
***

## run.py를 통한 현재 구현 기능

1. 단일 페이지에 대한 OCR
```python
IMAGE_PATH = 'OCRtestImage.png'
reader = easyocr.Reader(['ko', 'en'], gpu=False)
result = reader.readtext(IMAGE_PATH, paragraph=True)
```

2. 인식률 체크
```python
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


result_for_test = reader.readtext(IMAGE_PATH, detail=0, paragraph=True)
recognition_rate_check(result_for_test)
```

3. 인식결과의 json화
```python
def create_json_file(extracted_data_list):
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


create_json_file(result)
```
***

## 추후 추가/변경 예정 사항
1. 인식률이 낮은 글꼴에 대한 학습
2. 다수의 페이지에 대한 OCR 및 결과에 대한 json화



