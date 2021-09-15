import re
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_image_file_extension

from users.models import OurUser, Supplier, Regular
from utils.models_utils import model_image_directory_path

# Create your models here.
User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="دسته")
    sub_category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name="زیر مجموعه")

    class Meta:
        verbose_name = "دسته بندی ها"
        verbose_name_plural = "گروه بندی"

    def __str__(self):
        return f"{self.title}"


class Brand(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30, blank=True, null=True, verbose_name="کشور دفتر مرکزی")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="شهر دفتر مرکزی")
    phone_number = models.IntegerField(blank=True, null=True, verbose_name="تلفن دفتر مرکزی")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل دفتر مرکزی")

    def __str__(self):
        return f"{self.name}"


class Media(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    image_product = models.ImageField(upload_to=model_image_directory_path, null=True, blank=True,
                                      validators=[validate_image_file_extension], default=None)
    video_product = models.FileField(upload_to=model_image_directory_path, null=True, blank=True,default=None)
    description = models.CharField(max_length=100, default=None)

    def __str__(self):
        return f'{self.description}'


class Product(models.Model):
    Not_Exist, Active, Will_not_be_produced, Ordered = "N", "A", "W", "O"
    status_choices = [("N", "Not_Exist"), ("A", "Active"), ("W", "Will_not_be_produced"), ("O", "Ordered")]

    supplier = models.ForeignKey(to=Supplier, on_delete=models.RESTRICT, null=True, blank=True)
    ### FK ###
    filed = models.ForeignKey("Attribute", on_delete=models.CASCADE, null=True, blank=True, verbose_name="فیلد اضافی")
    cat = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey("Brand", on_delete=models.SET_NULL, null=True, blank=True)
    #### Product ####
    name = models.CharField(max_length=50, )
    upc = models.PositiveBigIntegerField(help_text="بارکد ۱۲ رقمی")
    count = models.IntegerField("تعداد", default=0)
    status = models.CharField("وضعیت موجودی", choices=status_choices, max_length=1, default="N")
    size = models.CharField(max_length=30, null=True, blank=True)
    wat = models.IntegerField("wat", null=True, blank=True)
    voltage = models.IntegerField("Voltage", null=True, blank=True)
    description = models.TextField("توضیحات اضافی", max_length=30, null=True, blank=True)
    catalog = models.FileField("کاتالوگ", upload_to="", null=True, blank=True)  ### How to connerct CDN??
    is_acrive = models.BooleanField("فعال/غیرفعال", default=False)
    ## Price ###  set Temp price for this product (( if (end - start) > (end - now) ==> cost = temporary_price
    price = models.FloatField(default=0, help_text="﷼")  # ex:10 000
    set_time = models.DateTimeField(auto_now_add=True)  # ex: 1400/06/10
    ## set Temp and start & end date
    date_start = models.DateTimeField("زمان شروع تخفیف", null=True, blank=True)  # ex: 1400/06/12
    date_end = models.DateTimeField("زمان پایان تخفیف", null=True, blank=True)  # ex: 1400/06/14
    Temporary_price = models.FloatField(verbose_name="قیمت مموقت", null=True, blank=True)  # ex: 15 000
    cost = models.FloatField("قیمت محصول", null=True, blank=True)  # last Price
    slug = models.SlugField(unique=True, null=True, blank=True, allow_unicode=True)

    @property
    def original_price(self):
        if self.date_start < timezone.now() < self.date_end:
            return True
        else:
            return False

    def save(self, force_insert=True, *args, **kwargs):
        if self.status == "N" and self.count > 0:
            raise Exception("تعداد کالا با وضعیت همخوانی ندارد ")
        if self.count < 0:
            raise Exception("تعداد کالا نمیتواند منفی باشد")
        if not self.date_start < self.date_end:
            raise Exception("تاریخ شروع از تاریخ پایان کمتر است ")

        if self.original_price:
            self.cost = self.Temporary_price
        else:
            self.cost = self.price

        if self.slug:
            slugify(self.slug, allow_unicode=True)
        return super().save()

    class Meta:
        verbose_name = "محصولات"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f" {self.name}, {self.cost}, {self.id}"


class Attribute(models.Model):
    att_fk = models.ForeignKey("Attribute", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    numeric_value = models.IntegerField(null=True, blank=True)
    string_value = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f" {self.title}"


##################################################################
# Create your models here.
class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(Log):
    status_choices = (('on_cart', 'on_cart'), ('ready_to_pay', 'ready_to_pay'))
    # FK
    # sth = models.ForeignKey(Regular, on_delete=models.CASCADE, null=True, blank=True)

    # Attrs
    cart_uuid = models.UUIDField("شماره کارت ساخته شده", unique_for_date=1, default=None)
    cart_status = models.CharField(max_length=100, choices=status_choices, default=status_choices[0])
    active = models.BooleanField(default=True)
