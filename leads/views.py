
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Lead
from .forms import LeadForm
from django.contrib.auth.decorators import login_required

def lead_capture(request, username):
	user = get_object_or_404(User, username=username)
	if request.method == 'POST':
		Lead.objects.create(
			user=user,
			name=request.POST.get('name'),
			email=request.POST.get('email'),
			message=request.POST.get('message')
		)
		return render(request, 'leads/thank_you.html', {'user': user})
	return render(request, 'leads/public_form.html', {'user': user})

@login_required
def lead_list(request):
	user = request.user
	leads = Lead.objects.filter(user=user).order_by('-created_at')
	# Analytics: count by status
	analytics = {
		'total': leads.count(),
		'new': leads.filter(status='new').count(),
		'contacted': leads.filter(status='contacted').count(),
		'done': leads.filter(status='done').count(),
	}
	# Status change (Pro/Premium only)
	tier = getattr(getattr(user, 'userprofile', None), 'tier', 'basic')
	if request.method == 'POST' and tier in ['pro', 'premium']:
		lead_id = request.POST.get('lead_id')
		new_status = request.POST.get('status')
		lead = Lead.objects.filter(id=lead_id, user=user).first()
		if lead and new_status in dict(Lead._meta.get_field('status').choices):
			lead.status = new_status
			lead.save()
		return redirect('lead_list')
	return render(request, 'leads/lead_list.html', {'leads': leads, 'analytics': analytics, 'tier': tier})