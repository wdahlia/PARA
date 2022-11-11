import json
import os

# django를 다루기 위해 경로 설정 (정확하지 않음)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# django 모델 다루기 위해 import (정확하지 않음)
import django

django.setup()

# 모델 DB를 다루기 위해 import
from products.models import Product, Image, Category

# json 파일 저장 위치
BASE_DIR = "crawling/"

# crawling_2_metadata에서 생성한 데이터 가져오기
with open(
    os.path.join(BASE_DIR, "crawling_2_metadata.json"), "r", encoding="UTF-8"
) as json_file:
    json_file = json.load(json_file)

for g, data in json_file.items():

    # Category 테이블 먼저 생성
    for j in data:
        if __name__ == "__main__":

            # 같은 카테고리 이름을 갖고 있는 객체가 있으면 pass, 없으면 새로 생성
            if len(Category.objects.filter(sort=j.get("category"))):
                pass
            else:
                Category(sort=j.get("category")).save()

    # Product, Image 테이블 생성
    for j in data:
        if __name__ == "__main__":

            # Product 모델 형식에 맞춰서 입력
            p = Product(
                name=j.get("name"),
                content=j.get("content"),
                color=j.get("color"),
                price=j.get("price"),
                size=j.get("size"),
                gender=g,
                # 카테고리는 Product -> Category 정참조 관계이므로, Category 객체를 할당하여 ID값을 넣어줌
                category=Category.objects.get(sort=j.get("category")),
            )
            p.save()  # 저장

            for img in j.get("img_list"):
                Image(
                    # 카테고리는 Image -> Product 정참조 관계이므로, Product 객체를 할당하여 ID값을 넣어줌
                    product=p,
                    product_image=img,
                ).save()  # 저장
