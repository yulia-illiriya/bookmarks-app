from django.db import models
from user_profile.models import User

   
class Collection(models.Model):
    collection_title = models.CharField("Название коллекции", max_length=120)
    collection_description = models.CharField("Краткое описание", max_length=255)
    created_at = models.DateTimeField("Создана в", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена в", auto_now=True)
    user = models.ForeignKey(
        User, 
        verbose_name="Владелец", 
        on_delete=models.CASCADE, 
        related_name="collections"
        )
    
    def __str__(self):
        return self.collection_title
    
    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
    
    
class Bookmark(models.Model):
    TYPE_CHOICES = (
        ('website', 'Website'),
        ('book', 'Book'),
        ('article', 'Article'),
        ('music', 'Music'),
        ('video', 'Video'),
    )
    
    page_header = models.CharField("Заголовок страницы", max_length=100)
    page_description = models.CharField("Краткое описание страницы", max_length=255)
    page_link = models.CharField("Ссылка на страницу", max_length=255)
    type_of_link = models.CharField("Тип ссылки", max_length=8, choices=TYPE_CHOICES, default='website')
    preview = models.ImageField("Превью")
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено в", auto_now=True)
    user = models.ForeignKey(
        User, 
        verbose_name="Владелец", 
        on_delete=models.CASCADE, 
        related_name="bookmarks"
        )
    collection = models.ManyToManyField(Collection, through='BookmarkInCollection')
    
    def __str__(self):
        return self.page_header
    
    
    
class BookmarkInCollection(models.Model):
    bookamrk = models.ForeignKey(Bookmark, on_delete=models.CASCADE, verbose_name="Закладка")
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name="Коллекция")