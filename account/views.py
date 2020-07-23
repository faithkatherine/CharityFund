from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AuthenticationForm, UpdateForm

# Create your views here.
def registration_view(request):
	context={}
	if request.POST:
		form = RegistrationForm(request.POST)

		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password')
			account = authenticate(email=email, password=raw_password)
			return redirect('base')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, '../Templates/Register.html', context)


def logout_view(request):
	logout(request)
	return redirect('base')


			

def login_view(request):
	context = {}
	user = request.user

	if user.is_authenticated:
		return redirect ('base')

	if request.POST:
		form= AuthenticationForm(request.POST)
		if form.is_valid():
			email= request.POST['email']
			password= request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				return redirect('base')
		
		else:
			context['login_form']= form
	else:
		 form= AuthenticationForm()
	context['login_form']= form
	return render(request, '../Templates/login.html', context)



def account_view(request):

	if not request.user.is_authenticated:
		return redirect('login')

	context = {}

	if request.POST:
		form = UpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()

	else:
		form = UpdateForm(
			initial ={
			"email": request.user.email,
			"username": request.user.username,
			}
		  )
	context['update_form'] = form
	return render(request, '../Templates/account.html', context)
