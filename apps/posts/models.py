from django.db import models
from ..account.models import User
from jsonfield import JSONField
# Create your models here.

class Post(models.Model):
    created_at =models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='posts/post',null=True,blank=True,verbose_name='Imagen del post')
    text=models.TextField(blank=True,null=True,verbose_name='Texto del post')
    likes =JSONField(default=[],verbose_name='likes',null=True,blank=True)
    is_enable=models.BooleanField(default=False)
    user=models.ForeignKey(User,related_name='posts',verbose_name='Usuario')

    class Meta:
        verbose_name_plural="Posts"
        verbose_name="Post"
        ordering=['-created_at',]

    def __str__(self):
        return u'Post de {} {}'.format(self.user.first_name,self.user.last_name)


class Comment(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    text=models.TextField(verbose_name='Texto del comentario')
    user=models.ForeignKey(User,related_name='comments',verbose_name='Usuario')
    post=models.ForeignKey(Post,related_name='comments',verbose_name='Post')

    class Meta:
        verbose_name_plural="Comentarios"
        verbose_name="Comentario"
        ordering=['-created_at',]

    def __str__(self):
        return u'Comentario de {} {} '.format(self.user.first_name,self.user.last_name)