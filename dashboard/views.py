from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leads.models import Lead

@login_required
def dashboard(request):
	leads = Lead.objects.filter(user=request.user)
	count = leads.count()
	return render(request, 'dashboard/dashboard.html', {'leads_count': count})
