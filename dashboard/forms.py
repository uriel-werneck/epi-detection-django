from django import forms
from dashboard.constants import MEDIA_TYPE_CHOICES


class ImageUploadForm(forms.Form):
    image = forms.ImageField(required=True)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        return image


class VideoUploadForm(forms.Form):
    video = forms.FileField(required=True)

    def clean_video(self):
        video = self.cleaned_data.get('video')
        return video


class ReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False, input_formats=['%Y-%m-%d'])
    end_date = forms.DateField(required=False, input_formats=['%Y-%m-%d'])
    show_all = forms.BooleanField(required=False)
    media_type = forms.ChoiceField(
        required=False,
        choices=[('all', 'All'), ('image', 'Image'), ('video', 'Video')],
        initial='all'
    )