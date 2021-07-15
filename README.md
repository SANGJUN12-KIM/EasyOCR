# EasyOCR for NIA-solution_for_social_issue
***
* 원본 소스: <https://github.com/JaidedAI/EasyOCR>
* 실행 코드: SANGJUN12-KIM/EasyOCR/__ main __.py
***

## 변경사항
* 21년 7월 15일
    * 지정된 디렉토리에 다수 페이지에 대한 OCR

        => 기본경로: ./target_pages
    * OCR된 페이지의 정보를 json으로 변환

        => 기본경로: ./OCRresults/파일.이미지형식.json
    * 기능 모듈화(__ main__.py)


* 21년 7월 8일
    * 인식률 체크 기능 어절, 음절, 음소별 세분화
    * 학습모델(user_network/custom.pth) 적용 가능


* 21년 6월 18일
    * 단일 페이지에 대한 OCR
    * OCR된 페이지의 정보를 json 으로 변환
    * 성능 확인을 위한 인식률 체크 기능

## 추가 예정사항
* 기본 모델보다 인식률이 개선된 커스텀 모델 추가
* 인식 후 처리기(맞춤법, 띄어쓰기 검사)를 통한 인식 결과 개

##설치
```python
git clone https://github.com/SANGJUN12-KIM/EasyOCR
```
## 사용법

__ main __.py 에서 실행
```python
image2text(image_path, custom_model, create_json)
    # image_path = 'str'            -> 변환할 이미지가 저장된 경로(default: './target_pages/')
    # custom_model = 'True'/'False' -> 커스텀 모델의 사용 여부(default: 'False')
    # create_json = 'True'/'False'  -> OCR된 결과물에 대한 json화 여부(default: 'True', 저장경로: './OCRresults')
```



