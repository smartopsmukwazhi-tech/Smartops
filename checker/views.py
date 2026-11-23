import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import CheckinSLA


@login_required
def index(request):
	return render(request, 'checker/index.html')


@login_required
def checkin_analyser(request):
	rules = list(CheckinSLA.objects.values('airline', 'aircraft_type', 'minimum_agents'))
	return render(request, 'Checkin_analyser.html', {'sla_rules_json': json.dumps(rules)})


@login_required
def ramp_analyser(request):
	return render(request, 'Ramp_analyser.html')


@login_required
def checkin_sla(request):
	if request.method == 'POST':
		airline = str(request.POST.get('airline', '')).strip().upper()
		aircraft_type = str(request.POST.get('aircraft_type', '')).strip().upper()
		try:
			minimum_agents = int(request.POST.get('minimum_agents', ''))
		except (TypeError, ValueError):
			minimum_agents = -1

		if airline and aircraft_type and minimum_agents >= 0:
			CheckinSLA.objects.update_or_create(
				airline=airline,
				aircraft_type=aircraft_type,
				defaults={'minimum_agents': minimum_agents},
			)
			request.session['sla_message'] = f'Saved SLA for {airline} / {aircraft_type}: {minimum_agents} agents.'

	message = request.session.pop('sla_message', '')
	rules = CheckinSLA.objects.all()
	return render(request, 'checker/sla.html', {'rules': rules, 'message': message})


@login_required
@require_http_methods(['GET', 'POST'])
def checkin_sla_api(request):
	if request.method == 'GET':
		rules = list(CheckinSLA.objects.values('airline', 'aircraft_type', 'minimum_agents'))
		return JsonResponse({'rules': rules})

	try:
		payload = json.loads(request.body or '{}')
		airline = str(payload.get('airline', '')).strip().upper()
		aircraft_type = str(payload.get('aircraft_type', '')).strip().upper()
		minimum_agents = int(payload.get('minimum_agents'))
	except (json.JSONDecodeError, TypeError, ValueError):
		return JsonResponse({'error': 'Invalid SLA values.'}, status=400)

	if not airline or not aircraft_type:
		return JsonResponse({'error': 'Airline and aircraft type are required.'}, status=400)
	if minimum_agents < 0:
		return JsonResponse({'error': 'Minimum agents cannot be negative.'}, status=400)

	rule, _ = CheckinSLA.objects.update_or_create(
		airline=airline,
		aircraft_type=aircraft_type,
		defaults={'minimum_agents': minimum_agents},
	)
	return JsonResponse({
		'airline': rule.airline,
		'aircraft_type': rule.aircraft_type,
		'minimum_agents': rule.minimum_agents,
	})

