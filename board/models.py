from django.db import models
from django.utils import timezone

# Create your models here.

class para(models.Model):
    title = models.CharField('제목', max_length=126)
    content = models.TextField('내용')
    author = models.CharField('작성자', max_length=16)
    date = models.DateTimeField('일자', default=timezone.now)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)