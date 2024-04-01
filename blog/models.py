from django.db import models

NULL_PARAM = {'null': True, 'blank': True}


class Blog(models.Model):

    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=170, verbose_name='URL')
    content = models.TextField(verbose_name='содержимое', **NULL_PARAM)
    preview = models.ImageField(upload_to='blog/', verbose_name='превью', **NULL_PARAM)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='факт публикации')
    views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f' {self.title} - {self.slug}, views: {self.views}, date: {self.date_created}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
