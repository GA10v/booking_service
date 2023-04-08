from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ReviewInfo, Task, Template

admin.site.site_title = _('My site name')
admin.site.site_header = _('My site header')
admin.site.index_title = _('My index title')


class TemplateAdminForm(forms.ModelForm):
    """Form to use with cleanup extra tinymce stuff."""

    class Meta:
        """Just regular Meta class."""

        model = Template
        fields = '__all__'


class TaskAdminForm(forms.ModelForm):
    """Form to use with cleanup extra tinymce stuff."""

    class Meta:
        """Just regular Meta class."""

        model = Task
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    """Form to use with cleanup extra tinymce stuff."""

    class Meta:
        """Just regular Meta class."""

        model = ReviewInfo
        fields = '__all__'


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """General class ot work with model."""

    form = TemplateAdminForm
    save_as = True


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """General class ot work with model."""

    form = TaskAdminForm
    save_as = True


@admin.register(ReviewInfo)
class ReviewInfoAdmin(admin.ModelAdmin):
    """General class ot work with model."""

    form = ReviewForm
    save_as = True
