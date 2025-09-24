from rest_framework import viewsets
from .models import Monastery
from .serializers import MonasterySerializer
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Monastery


from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from .models import Monk, MonkSession, MonkSessionApplication
from .serializers import MonkSerializer, MonkSessionSerializer, MonkSessionApplicationSerializer


import requests
from django.http import HttpResponse
from django.conf import settings



from .models import Archive
from .serializers import ArchiveSerializer


import re
from io import BytesIO
from django.http import FileResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse

class MonasteryViewSet(viewsets.ModelViewSet):
    queryset = Monastery.objects.all()
    serializer_class = MonasterySerializer



@api_view(["GET"])
def monastery_weather(request, pk):
    try:
        monastery = Monastery.objects.get(pk=pk)
        api_key = settings.OPENWEATHER_API_KEY
        if not api_key:
            return Response({"error": "Missing OpenWeather API key"}, status=500)

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={monastery.latitude}&lon={monastery.longitude}&appid={api_key}&units=metric"
        r = requests.get(url)
        data = r.json()

        if "main" not in data:  # API error
            return Response({"error": data.get("message", "Invalid response from API")}, status=500)

        return Response({
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
        })
    except Monastery.DoesNotExist:
        return Response({"error": "Monastery not found"}, status=404)
    



class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

class MonasteryArchivesView(APIView):
    def get(self, request, pk):
        monastery = Monastery.objects.get(pk=pk)
        archives = monastery.archives.all()
        serializer = ArchiveSerializer(archives, many=True)
        return Response(serializer.data)




class MonkViewSet(viewsets.ModelViewSet):
    queryset = Monk.objects.all()
    serializer_class = MonkSerializer


class MonkSessionViewSet(viewsets.ModelViewSet):
    queryset = MonkSession.objects.all()
    serializer_class = MonkSessionSerializer

    # List sessions for a specific monk
    @action(detail=True, methods=["get"])
    def monk_sessions(self, request, pk=None):
        sessions = MonkSession.objects.filter(monk_id=pk)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)


class MonkSessionApplicationViewSet(viewsets.ModelViewSet):
    queryset = MonkSessionApplication.objects.all()
    serializer_class = MonkSessionApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # List only logged-in user's applications
    @action(detail=False, methods=["get"])
    def my_applications(self, request):
        apps = MonkSessionApplication.objects.filter(user=request.user)
        serializer = self.get_serializer(apps, many=True)
        return Response(serializer.data)

# monasteries/views.py

# monasteries/views.py (append this at the bottom)




# import requests
# from django.http import JsonResponse, HttpResponse
# from django.conf import settings
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from io import BytesIO
# from .models import Monastery


# def _strip_html(html_text):
#     """Utility to strip HTML tags from Google Directions instructions."""
#     import re
#     cleanr = re.compile('<.*?>')
#     return re.sub(cleanr, '', html_text)


# def monastery_route_pdf(request, monastery_id):
#     try:
#         monastery = Monastery.objects.get(pk=monastery_id)
#     except Monastery.DoesNotExist:
#         return JsonResponse({"error": "Monastery not found"}, status=404)

#     # Get origin from query params
#     origin = request.GET.get("origin")
#     if not origin:
#         return JsonResponse({"error": "Origin parameter required (lat,lng)"}, status=400)

#     # Destination = monastery coordinates
#     dest = f"{monastery.latitude},{monastery.longitude}"

#     # --- Directions API Call ---
#     directions_url = "https://maps.googleapis.com/maps/api/directions/json"
#     params = {
#         "origin": origin,
#         "destination": dest,
#         "mode": "driving",
#         "key": settings.GOOGLE_DIRECTIONS_API_KEY,
#     }

#     directions = requests.get(directions_url, params=params).json()

#     if directions.get("status") != "OK":
#         return JsonResponse(
#             {"error": directions.get("status"), "details": directions}, status=400
#         )

#     # Extract steps
#     leg = directions["routes"][0]["legs"][0]
#     steps = [
#         f"{_strip_html(s['html_instructions'])} ({s['distance']['text']})"
#         for s in leg["steps"]
#     ]

#     # --- Create PDF ---
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=letter)
#     p.setFont("Helvetica", 12)

#     # Title
#     p.drawString(100, 750, f"Route to {monastery.name}")
#     p.drawString(100, 730, f"From: {origin}")
#     p.drawString(100, 715, f"To: {dest}")

#     # Directions
#     y = 690
#     for step in steps:
#         if y < 50:  # new page if needed
#             p.showPage()
#             p.setFont("Helvetica", 12)
#             y = 750
#         p.drawString(100, y, step)
#         y -= 20

#     p.showPage()
#     p.save()

#     buffer.seek(0)
#     return HttpResponse(buffer, content_type="application/pdf")

#     # 2) Static map snapshot still needs the Static Maps API key
#     poly = directions["routes"][0]["overview_polyline"]["points"]
#     static_url = (
#         "https://maps.googleapis.com/maps/api/staticmap"
#         f"?size=800x400&scale=2&path=enc:{poly}"
#         f"&markers=color:green|label:S|{origin}"
#         f"&markers=color:red|label:D|{dest}"
#         f"&key={settings.GOOGLE_STATIC_MAPS_API_KEY}"
#     )
#     map_img = requests.get(static_url).content

#     # 3) PDF building (same as your code)...


#     # 3) Build PDF
#     buf = BytesIO()
#     c = canvas.Canvas(buf, pagesize=A4)
#     width, height = A4

#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(40, height - 40, f"Route to {monastery.name}")

#     # draw map
#     img = ImageReader(BytesIO(map_img))
#     c.drawImage(img, 40, height - 300, width=width - 80, height=200)

#     # add steps
#     y = height - 320
#     c.setFont("Helvetica", 10)
#     for step in steps:
#         for line in [step[i:i+90] for i in range(0, len(step), 90)]:
#             if y < 60:
#                 c.showPage()
#                 y = height - 40
#             c.drawString(50, y, line)
#             y -= 14

#     c.save()
#     buf.seek(0)

#     filename = f"{monastery.name}_route.pdf".replace(" ", "_")
#     return FileResponse(buf, as_attachment=True, filename=filename)



# def static_map(request):
#     base_url = "https://maps.googleapis.com/maps/api/staticmap"
#     params = {
#         "center": "Rumtek Monastery,Sikkim,India",
#         "zoom": "14",
#         "size": "600x400",
#         "markers": "color:red|Rumtek Monastery,Sikkim",
#         "key": settings.GOOGLE_STATIC_MAPS_API_KEY,
#     }
#     response = requests.get(base_url, params=params)
#     return HttpResponse(response.content, content_type="image/png")
    

import requests
from django.http import JsonResponse, HttpResponse, FileResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from .models import Monastery
import textwrap

def _strip_html(html_text):
    """Utility to strip HTML tags from Google Directions instructions."""
    import re
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', html_text)

def _wrap_text(text, width=80):
    """Wrap text to specified width"""
    return textwrap.fill(text, width=width)

def monastery_route_pdf(request, monastery_id):
    try:
        monastery = Monastery.objects.get(pk=monastery_id)
    except Monastery.DoesNotExist:
        return JsonResponse({"error": "Monastery not found"}, status=404)

    # Get origin from query params
    origin = request.GET.get("origin")
    if not origin:
        return JsonResponse({"error": "Origin parameter required (lat,lng)"}, status=400)

    # Destination = monastery coordinates
    dest = f"{monastery.latitude},{monastery.longitude}"

    # --- Directions API Call ---
    directions_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": dest,
        "mode": "driving",
        "key": settings.GOOGLE_DIRECTIONS_API_KEY,
    }
    
    directions = requests.get(directions_url, params=params).json()
    if directions.get("status") != "OK":
        return JsonResponse(
            {"error": directions.get("status"), "details": directions}, status=400
        )

    # Extract steps
    leg = directions["routes"][0]["legs"][0]
    steps = [
        f"{_strip_html(s['html_instructions'])} ({s['distance']['text']})"
        for s in leg["steps"]
    ]

    # Get polyline for static map
    poly = directions["routes"][0]["overview_polyline"]["points"]
    
    # --- Static Map API Call ---
    static_url = (
        "https://maps.googleapis.com/maps/api/staticmap"
        f"?size=800x400&scale=2&path=enc:{poly}"
        f"&markers=color:green|label:S|{origin}"
        f"&markers=color:red|label:D|{dest}"
        f"&key={settings.GOOGLE_STATIC_MAPS_API_KEY}"
    )
    
    try:
        map_response = requests.get(static_url)
        map_response.raise_for_status()
        map_img = map_response.content
    except requests.RequestException:
        return JsonResponse({"error": "Failed to generate map image"}, status=500)

    # --- Create PDF with Map and Directions ---
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 40, f"Route to {monastery.name}")
    
    # Origin and destination info
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 65, f"From: {origin}")
    c.drawString(40, height - 85, f"To: {dest}")
    
    # Add total distance and duration if available
    total_distance = leg.get('distance', {}).get('text', 'N/A')
    total_duration = leg.get('duration', {}).get('text', 'N/A')
    c.drawString(40, height - 105, f"Total Distance: {total_distance}")
    c.drawString(40, height - 125, f"Estimated Time: {total_duration}")
    
    # Draw map image
    try:
        img = ImageReader(BytesIO(map_img))
        # Position map below the header info
        map_y = height - 350  # Adjusted position
        map_height = 200
        c.drawImage(img, 40, map_y, width=width - 80, height=map_height)
    except Exception as e:
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 200, "Map image could not be loaded")
    
    # Add directions below the map
    c.setFont("Helvetica-Bold", 12)
    y = map_y - 30
    c.drawString(40, y, "Directions:")
    
    # Add step-by-step instructions with proper text wrapping
    c.setFont("Helvetica", 10)
    y -= 25
    step_number = 1
    
    for step in steps:
        # Check if we need a new page
        if y < 80:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 40
        
        # Add step number
        step_text = f"{step_number}. {step}"
        
        # Wrap long text to fit within margins
        wrapped_lines = textwrap.wrap(step_text, width=85)  # Adjust width as needed
        
        for line in wrapped_lines:
            if y < 60:  # Check again for page break
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40
            
            c.drawString(50, y, line)
            y -= 14
        
        y -= 5  # Add small gap between steps
        step_number += 1
    
    c.save()
    buffer.seek(0)
    
    # Create filename
    filename = f"{monastery.name}_route.pdf".replace(" ", "_")
    
    return FileResponse(buffer, as_attachment=True, filename=filename)

def static_map(request):
    """Standalone static map function"""
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": "Rumtek Monastery,Sikkim,India",
        "zoom": "14",
        "size": "600x400",
        "markers": "color:red|Rumtek Monastery,Sikkim",
        "key": settings.GOOGLE_STATIC_MAPS_API_KEY,
    }
    
    response = requests.get(base_url, params=params)
    return HttpResponse(response.content, content_type="image/png")


import requests
from django.conf import settings
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Market
from .serializers import MarketSerializer


# List all markets
class MarketListView(generics.ListAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


# Single market detail
class MarketDetailView(generics.RetrieveAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


# Get route to market
@api_view(["GET"])
def get_route_to_market(request, pk):
    try:
        market = Market.objects.get(pk=pk)
    except Market.DoesNotExist:
        return Response({"error": "Market not found"}, status=404)

    user_lat = request.query_params.get("latitude")
    user_lng = request.query_params.get("longitude")

    if not user_lat or not user_lng:
        return Response({"error": "User latitude and longitude required"}, status=400)

    directions_url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={user_lat},{user_lng}&destination={market.latitude},{market.longitude}"
        f"&key={settings.GOOGLE_DIRECTIONS_API_KEY}"
    )

    response = requests.get(directions_url)
    data = response.json()

    return Response({
        "market": MarketSerializer(market).data,
        "route": data
    })
