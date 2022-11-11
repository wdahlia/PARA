from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
import os

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 디테일 이미지 추출
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# json 파일 저장 위치
BASE_DIR = "crawling/"

# crawling_1_url에서 추출한 URL 가져오기
with open(
    os.path.join(BASE_DIR, "crawling_1_url.json"), "r", encoding="UTF-8"
) as json_file:
    json_file = json.load(json_file)


# 전체 데이터 받을 딕셔너리
data = {}

# json_file = { 성별 : { "카테고리" : [URL1, URL2, URL3 ...] } }

# g = 성별, url_dict = { "카테고리" : [URL1, URL2, URL3 ...] }
for g, url_dict in json_file.items():

    # URL 1개 데이터 받을 리스트
    gender_data = []

    # category = "카테고리", url_list = [URL1, URL2, URL3 ...]
    for category, url_list in url_dict.items():

        # 카테고리 하나에 포함된 모든 URL을 각각 접속하여, 게시글이 갖고 있는 데이터 (사진, 상품명, 가격 등) 추출
        for url in url_list:

            # url 1개의 데이터를 받을 딕셔너리
            tmp_data = {}

            URL = url
            driver.get(url=URL)

            driver.implicitly_wait(5)

            # 이름 데이터 가져오기
            name = driver.find_element(
                By.CLASS_NAME,
                "product-detail-info__header-name",
            )

            # 콘텐츠 데이터 가져오기 (다른 부분은 전처리 용도)
            content = driver.find_element(
                By.XPATH,
                '//*[@id="main"]/article/div/div[1]/div[2]/div[1]/div[2]/div/div/div/p',
            ).text

            content = content.split("\n")[0]

            # 색상 데이터 가져오기
            color = driver.find_element(
                By.CLASS_NAME,
                "product-detail-selected-color",
            )

            # 가격 데이터 가져오기
            price = driver.find_element(
                By.CLASS_NAME,
                "money-amount__main",
            )

            # 사이즈 데이터 가져오기 (리스트X)
            sizes = driver.find_elements(
                By.CLASS_NAME,
                "product-size-info__size",
            )

            # 이미지 데이터 가져오기 (리스트)
            images = driver.find_elements(
                By.CLASS_NAME,
                "media-image",
            )

            # 딕셔너리 저장: 상품명
            tmp_data["name"] = name.text

            # 딕셔너리 저장: 상품 내용
            tmp_data["content"] = content

            # 딕셔너리 저장: 색상
            tmp_data["color"] = color.text

            # 딕셔너리 저장: 가격
            tmp_data["price"] = price.text

            # 딕셔너리 저장: 사이즈
            tmp_size = ""
            for size in sizes:
                st = size.text.replace("\nComing soon", "")
                tmp_size += st + "\n"
            tmp_data["size"] = tmp_size

            # 딕셔너리 저장: 카테고리
            tmp_data["category"] = category

            # 딕셔너리 저장: 이미지 URL 리스트
            tmp = []
            for img in images:
                img = img.find_element(By.TAG_NAME, "source")
                img_list = img.get_attribute("srcset").split()
                tmp.append(img_list[-2])

                tmp_data["img_list"] = tmp

            # 상품 1개 데이터 수집 완료.

            # gender_data에 저장
            gender_data.append(tmp_data)

            # 전체 데이터에 gender별로 저장
            data[g] = gender_data


# json 파일 저장 위치
BASE_DIR = "crawling/"

with open(
    os.path.join(BASE_DIR, "crawling_2_metadata.json"), "w+", encoding="UTF-8"
) as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)
