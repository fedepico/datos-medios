from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import GeeksForm, EditProfileForm 

def profile(request):

	if request.method == 'GET':
		formulario = EditProfileForm(instance=request.user)
	else:
		formulario = EditProfileForm(request.POST, instance=request.user)
		if formulario.is_valid():
			formulario.save()
			#update_session_auth_hash(request,formulario.user)
			return redirect(reverse('profile'))
	return render(request, 'accounts/profile.html', {'formulario':formulario})

# Create your views here. 
def home_view(request): 
	context = {} 
	form = GeeksForm(request.POST or None) 
	context['form']= form 
	if request.POST: 
		if form.is_valid(): 
			temp = form.cleaned_data.get("geeks_field") 
			print(temp) 
	return render(request, "accounts/home.html", context) 
