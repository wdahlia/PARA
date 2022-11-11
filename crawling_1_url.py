from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
import os

# 크롤링 결과 담을 디렉토리("crawling/") 생성
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


createFolder("crawling/")


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

###### 링크 추출

######## 크롤링할 카테고리 선택: ["자켓", "니트", "셔츠", "티셔츠", "맨투맨", "팬츠", "슈즈"]#######
category_list = ["자켓", "코트", "니트", "셔츠", "팬츠"]
#################################################################################################

######################### 성별 선택: { 여자 : "WOMAN", 남자: "MAN" } #############################
gender = ["WOMAN", "MAN"]
#################################################################################################

data = {}

for g in gender:

    gender_data = {}

    for category in category_list:

        # 기본 주소
        URL = f"https://www.zara.com/kr/ko/search?searchTerm={category}&section={g}"
        driver.get(url=URL)

        # # 검색 창 포커싱
        # elem = driver.find_element(By.ID, "search-products-form-combo-input")

        # # 원하는 값 입력
        # elem.send_keys(category)
        # elem.send_keys(Keys.RETURN)

        driver.implicitly_wait(5)
        time.sleep(5)

        # 각 게시글이 <a></a>에 갖고 있는 URL 가져오기
        url_ = driver.find_elements(By.CLASS_NAME, "product-link")

        ###################### num = 가져올 상품 개수 * 2 ####################
        num = 10
        #####################################################################

        # url_ 반복
        # ERROR FIX: 링크가 2번씩 들어와서, 절반 제거하기 위함
        cnt = 0
        url_list = []
        for u in url_:
            if cnt % 2 == 0:
                url_list.append(u.get_attribute("href"))

            cnt += 1
            if cnt == num:
                break

        # 반복 종료, 데이터에 저장

        # gender_data에 저장
        gender_data[category] = url_list

        # 전체 데이터에 gender별로 저장
        data[g] = gender_data

    # json 파일 저장 위치
    BASE_DIR = "crawling/"

    with open(
        os.path.join(BASE_DIR, "crawling_1_url.json"), "w+", encoding="UTF-8"
    ) as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
