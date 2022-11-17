from django.db import models
from products.models import Product, Image
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    # 수량은 -1 과 같은 수량이 없기 때문에 아래의 필드로 선언하여 최소값을 1 로 설정
    quantity = models.PositiveSmallIntegerField(
        null=True, default=1, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "장바구니"
        verbose_name_plural = f"{verbose_name} 목록"
        ordering = ["-pk"]

    def sub_total(self):
        # 템플릿에서 사용하는 변수로 장바구니에 담긴 각 상품의 합계
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.nam
