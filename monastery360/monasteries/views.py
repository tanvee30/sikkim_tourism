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
from django.shortcuts import get_object_or_404, render

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

# views.py - 360° Virtual Tour API

import requests
import json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Monastery

def monastery_360_tour(request, monastery_id):
    """
    API to get 360° virtual tour data for a monastery
    Returns Street View panorama data and multiple viewing angles
    """
    try:
        monastery = get_object_or_404(Monastery, pk=monastery_id)
        
        # Get radius parameter (default 100m)
        radius = request.GET.get('radius', '100')
        
        # Street View Static API for panorama images
        base_url = "https://maps.googleapis.com/maps/api/streetview"
        
        # Multiple viewing angles for 360° experience
        viewing_angles = [0, 45, 90, 135, 180, 225, 270, 315]  # 8 directions
        
        tour_data = {
            "monastery": {
                "id": monastery.id,
                "name": monastery.name,
                "latitude": monastery.latitude,
                "longitude": monastery.longitude,
                "description": getattr(monastery, 'description', ''),
            },
            "panoramas": [],
            "metadata": {
                "total_views": len(viewing_angles),
                "radius": radius,
                "generated_at": "2024-01-01T00:00:00Z"
            }
        }
        
        # Generate panorama data for each angle
        for i, angle in enumerate(viewing_angles):
            panorama_url = (
                f"{base_url}?"
                f"location={monastery.latitude},{monastery.longitude}&"
                f"size=800x600&"
                f"heading={angle}&"
                f"pitch=0&"
                f"fov=90&"
                f"radius={radius}&"
                f"key={settings.GOOGLE_STREET_VIEW_API_KEY}"
            )
            
            # Check if Street View data is available at this location
            metadata_url = (
                "https://maps.googleapis.com/maps/api/streetview/metadata?"
                f"location={monastery.latitude},{monastery.longitude}&"
                f"radius={radius}&"
                f"key={settings.GOOGLE_STREET_VIEW_API_KEY}"
            )
            
            try:
                metadata_response = requests.get(metadata_url).json()
                
                if metadata_response.get('status') == 'OK':
                    panorama_data = {
                        "view_id": i + 1,
                        "heading": angle,
                        "direction": get_direction_name(angle),
                        "image_url": panorama_url,
                        "status": "available",
                        "pano_id": metadata_response.get('pano_id'),
                        "location": {
                            "lat": metadata_response.get('location', {}).get('lat'),
                            "lng": metadata_response.get('location', {}).get('lng')
                        },
                        "copyright": metadata_response.get('copyright', ''),
                        "date": metadata_response.get('date', '')
                    }
                else:
                    panorama_data = {
                        "view_id": i + 1,
                        "heading": angle,
                        "direction": get_direction_name(angle),
                        "image_url": panorama_url,
                        "status": "not_available",
                        "error": metadata_response.get('status')
                    }
                    
                tour_data["panoramas"].append(panorama_data)
                
            except requests.RequestException as e:
                return JsonResponse({
                    "error": "Failed to fetch Street View data",
                    "details": str(e)
                }, status=500)
        
        return JsonResponse(tour_data)
        
    except Monastery.DoesNotExist:
        return JsonResponse({"error": "Monastery not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_direction_name(angle):
    """Convert angle to direction name"""
    directions = {
        0: "North", 45: "Northeast", 90: "East", 135: "Southeast",
        180: "South", 225: "Southwest", 270: "West", 315: "Northwest"
    }
    return directions.get(angle, f"{angle}°")

def monastery_360_viewer(request, monastery_id):
    """
    Return HTML viewer for 360° tour
    """
    try:
        monastery = get_object_or_404(Monastery, pk=monastery_id)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>360° Tour - {monastery.name}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ 
                    margin: 0; 
                    font-family: Arial, sans-serif; 
                    background: #000;
                }}
                .viewer-container {{
                    width: 100vw;
                    height: 100vh;
                    position: relative;
                    overflow: hidden;
                }}
                .panorama-image {{
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transition: opacity 0.5s ease;
                }}
                .controls {{
                    position: absolute;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    display: flex;
                    gap: 10px;
                    background: rgba(0,0,0,0.7);
                    padding: 15px;
                    border-radius: 10px;
                }}
                .control-btn {{
                    background: #4285f4;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                }}
                .control-btn:hover {{
                    background: #3367d6;
                }}
                .control-btn.active {{
                    background: #0f9d58;
                }}
                .monastery-info {{
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    background: rgba(0,0,0,0.8);
                    color: white;
                    padding: 15px;
                    border-radius: 8px;
                    max-width: 300px;
                }}
                .loading {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: white;
                    font-size: 18px;
                }}
            </style>
        </head>
        <body>
            <div class="viewer-container">
                <div class="loading" id="loading">Loading 360° Tour...</div>
                
                <div class="monastery-info">
                    <h2>{monastery.name}</h2>
                    <p>📍 Lat: {monastery.latitude}, Lng: {monastery.longitude}</p>
                    <p>🌐 360° Virtual Tour</p>
                </div>
                
                <img id="panoramaImage" class="panorama-image" style="display: none;" />
                
                <div class="controls" id="controls" style="display: none;">
                    <button class="control-btn active" onclick="changeView(0)">N</button>
                    <button class="control-btn" onclick="changeView(1)">NE</button>
                    <button class="control-btn" onclick="changeView(2)">E</button>
                    <button class="control-btn" onclick="changeView(3)">SE</button>
                    <button class="control-btn" onclick="changeView(4)">S</button>
                    <button class="control-btn" onclick="changeView(5)">SW</button>
                    <button class="control-btn" onclick="changeView(6)">W</button>
                    <button class="control-btn" onclick="changeView(7)">NW</button>
                    <button class="control-btn" onclick="autoRotate()">🔄 Auto</button>
                </div>
            </div>

            <script>
                let tourData = null;
                let currentView = 0;
                let autoRotating = false;
                let rotateInterval = null;

                // Load tour data
                async function loadTourData() {{
                    try {{
                        const response = await fetch('/monastery/1/360-tour/');

                        tourData = await response.json();
                        
                        if (tourData.panoramas && tourData.panoramas.length > 0) {{
                            document.getElementById('loading').style.display = 'none';
                            document.getElementById('controls').style.display = 'flex';
                            changeView(0);
                        }} else {{
                            document.getElementById('loading').innerHTML = 'No Street View data available for this location';
                        }}
                    }} catch (error) {{
                        document.getElementById('loading').innerHTML = 'Error loading tour data';
                        console.error('Error:', error);
                    }}
                }}

                function changeView(viewIndex) {{
                    if (!tourData || !tourData.panoramas[viewIndex]) return;
                    
                    currentView = viewIndex;
                    const panorama = tourData.panoramas[viewIndex];
                    const img = document.getElementById('panoramaImage');
                    
                    if (panorama.status === 'available') {{
                        img.src = panorama.image_url;
                        img.style.display = 'block';
                    }}
                    
                    // Update active button
                    document.querySelectorAll('.control-btn').forEach((btn, i) => {{
                        if (i === viewIndex) {{
                            btn.classList.add('active');
                        }} else {{
                            btn.classList.remove('active');
                        }}
                    }});
                }}

                function autoRotate() {{
                    if (autoRotating) {{
                        clearInterval(rotateInterval);
                        autoRotating = false;
                    }} else {{
                        autoRotating = true;
                        rotateInterval = setInterval(() => {{
                            currentView = (currentView + 1) % 8;
                            changeView(currentView);
                        }}, 2000);
                    }}
                }}

                // Load data on page load
                loadTourData();
            </script>
        </body>
        </html>
        """
        
        return HttpResponse(html_content, content_type='text/html')
        
    except Monastery.DoesNotExist:
        return HttpResponse("Monastery not found", status=404)

# def monastery_streetview_embed(request, monastery_id):
#     """
#     Generate Google Street View embed URL for iframe integration
#     """
#     try:
#         monastery = get_object_or_404(Monastery, pk=monastery_id)
        
#         # Parameters
#         fov = request.GET.get('fov', '90')  # Field of view
#         heading = request.GET.get('heading', '0')  # Direction
#         pitch = request.GET.get('pitch', '0')  # Up/down angle
        
#         embed_url = (
#             "https://www.google.com/maps/embed/v1/streetview?"
#             f"key={settings.GOOGLE_STREET_VIEW_API_KEY}&"
#             f"location={monastery.latitude},{monastery.longitude}&"
#             f"heading={heading}&"
#             f"pitch={pitch}&"
#             f"fov={fov}"
#         )
        
#         return JsonResponse({
#             "monastery_id": monastery_id,
#             "monastery_name": monastery.name,
#             "embed_url": embed_url,
#             "iframe_html": f'<iframe src="{embed_url}" width="600" height="400" frameborder="0"></iframe>'
#         })
        
#     except Monastery.DoesNotExist:
#         return JsonResponse({"error": "Monastery not found"}, status=404)





