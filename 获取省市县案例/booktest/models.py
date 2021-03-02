from django.db import models

# Create your models here.

class AreaInfo(models.Model):
    '''地区模型类'''
    # 地区名称
    atitle = models.CharField(verbose_name='地区', max_length=20) #  verbose_name 修改属性的表的表名
    # 自关联属性
    aParent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        '''重写表的地区名'''
        return self.atitle

    # 类方法
    def title(self):
        return self.atitle
    # 指定方法对应的列的排序
    title.admin_order_field = 'atitle' # 根据atitle排序
    # 指定方法对应的列的标题
    title.short_description = '地区名称' # 修改自定义方法的表的表名

    def parent(self):
        '''父级地区'''
        if self .aParent is None:
            return ''
        return self.aParent.atitle
    parent.short_description = '父级地区名称'
    

class PicTest(models.Model):
    '''上传图片'''
    goods_pic = models.ImageField(upload_to='booktest')
    