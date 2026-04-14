
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Lead
from .forms import LeadForm
from django.contrib.auth.decorators import login_required

def lead_capture(request, username):
	user = get_object_or_404(User, username=username)
	if request.method == 'POST':
		form = LeadForm(request.POST)
		if form.is_valid():
			lead = form.save(commit=False)
			lead.user = user
			lead.save()
			return render(request, 'leads/thank_you.html', {'user': user})
	else:
		form = LeadForm()
	return render(request, 'leads/lead_form.html', {'form': form, 'user': user})

@login_required
def lead_list(request):
	leads = Lead.objects.filter(user=request.user).order_by('-created_at')
	return render(request, 'leads/lead_list.html', {'leads': leads})