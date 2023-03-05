from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    teacher = "T"
    student = "S"

    ROLE_CHOICES = (
        (teacher, "teacher"),
        (student, "student"),
    )

    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=student,
        verbose_name="نقش کاربری",
    )
    phone_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name="شماره موبایل",
    )
    ssn = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        verbose_name="کد پرسنلی",
    )
    national_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        verbose_name="کد ملی",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Thesis(models.Model):
    class Meta:
        verbose_name = "پایان‌نامه"
        verbose_name_plural = "پایان‌نامه‌ها"

    pending = "PEN"
    accepted = "ACC"
    rejected = "REJ"

    STATUS_CHOICES = (
        (accepted, "تایید شده"),
        (rejected, "رد شده"),
        (pending, "در حال بررسی"),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_thesises",
        verbose_name="دانشجو",
    )
    refree = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_thesises",
        verbose_name="داور",
    )
    title = models.TextField(
        verbose_name="عنوان",
    )
    description = models.TextField(
        verbose_name="توضیحات",
    )
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=pending,
        verbose_name="وضعیت",
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    class Meta:
        verbose_name = ("پیام",)
        verbose_name_plural = "پیام‌ها"

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sended_messages",
        verbose_name="فرستنده",
    )
    reciever = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recieved_messages",
        verbose_name="گیرنده",
    )
    text = models.TextField(
        verbose_name="متن پیام",
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
