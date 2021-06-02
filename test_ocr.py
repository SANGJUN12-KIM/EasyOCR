import easyocr
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image

IMAGE_PATH = 'OCRtestImage.png'
print("\nOCR로 인식된 내용리스트")
reader = easyocr.Reader(['ko', 'en'])  # need to run only once to load model into memory
result = reader.readtext(IMAGE_PATH, detail=0, paragraph=True)
print(result)

print("\n인식된 문장을 공백 단위로 슬라이싱")
slicedResult = "".join(result)
slicedResult = slicedResult.split()
print(slicedResult)

print("\n원본을 공백 단위로 슬라이싱")
with open("OriginalTXT.txt", "r") as tf:
    originalText = []
    for line in tf:
        originalText.append(line)

dotConvOriginal =[]
for i in originalText:
    dotFind = i.replace("·", " ")
    dotConvOriginal.append(dotFind)

slicedOriginal = "".join(dotConvOriginal)

slicedOriginal = slicedOriginal.split()
print(slicedOriginal)

print("\n OCR결과물 중 원본과의 불일치 요소 출력")
difference = []
for i in slicedResult:
    if i not in slicedOriginal:
        difference.append(i)

print(difference)

"""
print("\nOCR 결과물 띄어쓰기 제거")
RemoveBlank = [i.replace(' ', '') for i in result]
print(RemoveBlank)

print("\n띄어쓰기 제거된 원본")
with open("OriginalTXT.txt", "r") as tf:
    originalText = []
    for line in tf:
        originalText.append(line)
    originalText = [i.replace(' ', '') for i in originalText]
    originalText = [i.replace('\n', '') for i in originalText]
print(originalText)

print("\n OCR결과물과 원본의 비교")
ocrString = np.array(RemoveBlank)
print(ocrString)

originString = np.array(originalText)
print(originString)

print(ocrString == originString)
"""


"""
img = cv2.imread(IMAGE_PATH)

img = Image.fromarray(img)
font = ImageFont.truetype("fonts/D2Coding-Ver1.3.2-20180524.ttc", 8)
draw = ImageDraw.Draw(img)

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(255, 3), dtype="uint8")

for i in result:
    x = i[0][0][0]
    y = i[0][0][1]
    w = i[0][1][0] - i[0][0][0]
    h = i[0][2][1] - i[0][1][1]

    color_idx = random.randint(0, 255)
    color = [int(c) for c in COLORS[color_idx]]

    #    cv2.putText(img, str(i[1]), (int((x + x + w) / 2) , y-2), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    #    img = cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
    draw.rectangle(((x, y), (x + w, y + h)), outline=tuple(color), width=1)
    draw.text((int((x + x + w) / 2), y - 3), str(i[1]), font=font, fill=tuple(color), )

plt.imshow(img)
plt.show()
# cv2.imshow("test",img)
# cv2.waitKey(0)
"""""

