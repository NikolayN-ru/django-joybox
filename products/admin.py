from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from PIL import Image


class ImageAdminForm(ModelForm):
    MIN_RESOLUTION = (400, 400)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe('<span style="color: red">допустимое разрешение {}x{}<span>'.format(
            *self.MIN_RESOLUTION
        ))

    # def clean_image(self):
    #     image = self.clean_image['image']
    #     img = Image.open(image)
    #     min_height, min_width = self.MIN_RESOLUTION
        # if img.height < min_height or img.width < min_height:
        #     raise ValidationError('недопустимое разрешение')
        # return image


class NotebookAdmin(admin.ModelAdmin):
    form = ImageAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    form = ImageAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartfones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
