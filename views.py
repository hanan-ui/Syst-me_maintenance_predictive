from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Reading
from .forms import ReadingForm

@login_required
def dashboard(request):
    # Récupérer les 200 derniers relevés
    readings_qs = Reading.objects.order_by("-timestamp")[:200]

    # Préparer les données pour le template
    readings = [
        {
            "id": r.id,
            "sensor_id": r.sensor_id or "Unknown",
            "temperature_c": r.temperature_c,
            "is_anomaly": r.is_anomaly,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for r in readings_qs
    ]

    form = ReadingForm()
    return render(request, "tempmon/dashboard.html", {"readings": readings, "form": form})

@login_required
def add_reading(request):
    if request.method == "POST":
        form = ReadingForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("tempmon:dashboard")

@csrf_exempt
def api_create_reading(request):
    """
    Endpoint pour recevoir un POST JSON:
    { "sensor_id": "A1", "temperature_c": 85.4 }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        temp = float(data.get("temperature_c"))
        sensor_id = data.get("sensor_id", "Unknown")
    except (ValueError, TypeError, json.JSONDecodeError):
        return HttpResponseBadRequest("Invalid JSON or missing field 'temperature_c'")

    reading = Reading(sensor_id=sensor_id, temperature_c=temp)
    reading.save()

    return JsonResponse({
        "id": reading.id,
        "sensor_id": reading.sensor_id,
        "temperature_c": reading.temperature_c,
        "is_anomaly": reading.is_anomaly,
        "timestamp": reading.timestamp.isoformat(),
    }, status=201)

@login_required
def graph_page(request):
    readings_qs = Reading.objects.order_by("timestamp")
    # Convertir en liste JSON serializable
    readings = list(readings_qs.values('id', 'sensor_id', 'temperature_c', 'is_anomaly', 'timestamp'))
    return render(request, "tempmon/graph.html", {"readings": readings})
