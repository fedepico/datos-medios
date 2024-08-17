from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    #template_name='/something/else'

    class Meta:
        model = User
        fields = (
        	'username',
            'first_name',
            'last_name',
            'email',  
        )

DEMO_CHOICES =( 
	("1", "Naveen"), 
	("2", "Pranav"), 
	("3", "Isha"), 
	("4", "Saloni"), 
) 
class GeeksForm(forms.Form): 
	geeks_field = forms.MultipleChoiceField(choices = DEMO_CHOICES) 
	
