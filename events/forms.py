from django import forms
from .models import Updates, Event
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class UpdatesForm(forms.ModelForm):

	class Meta:
		model = Updates
		fields = ('title', 'content', 'access', 'end')


class EventsForm(forms.ModelForm):
	information = forms.CharField(widget=CKEditorUploadingWidget())
	class Meta:
		model = Event
		fields = ('title','event_image','headline','information')
