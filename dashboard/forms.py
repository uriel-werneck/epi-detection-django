from django import forms


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