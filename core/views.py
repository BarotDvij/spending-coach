from django.http import JsonResponse

def hello_world(request):
    return JsonResponse({"message": "Hello, Spending Coach!"})

# Create your views here.
