from django.utils import timezone
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core import serializers
from .models import Post, Seller
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def index(request: HttpRequest):
    if request.method == "GET":
        posts_list = serializers.serialize("json", Post.objects.all())
        return HttpResponse(posts_list, content_type="application/json")
    elif request.method == "POST":
        body = json.loads(request.body)
        try:
            seller = Seller.objects.get(name=body["seller"])
        except Seller.DoesNotExist:
            return HttpResponse("Seller not found", content_type="application/json", status=404)
 
        p = Post(title=body["title"],
                    description=body["description"],
                    seller=seller,
                    image_url=body["image_url"],
                    pub_date=timezone.now())
        p.save()
        p_json = serializers.serialize("json", [p])
        return HttpResponse(p_json, content_type="application/json")

    # response = json.dumps(posts_list)
    # return HttpResponse(f"Welcome to olx API \n{posts_list}")

@csrf_exempt
def sellers(request: HttpRequest):
    if request.method == "GET":
        seller_list = serializers.serialize("json", Seller.objects.all())
        return HttpResponse(seller_list, content_type="application/json")
    elif request.method == "POST":
        body = json.loads(request.body)
        s = Seller(name=body["name"],
                    email=body["email"])
        s.save()
        s_json = serializers.serialize("json", [s])
        return HttpResponse(s_json, content_type="application/json")


def seller_details(request: HttpRequest, id: int):
    if request.method == "GET":
        try:
            seller = Seller.objects.get(id=id)
            seller_json = serializers.serialize("json", [seller])
            return HttpResponse(seller_json, content_type="application/json")
        except Seller.DoesNotExist:
            return HttpResponse("Seller not found", content_type="application/json", status=404)


def details(request, id: int):
    post = Post.objects.filter(pk=id)
    response = serializers.serialize("json", post)
    if not post:
        return HttpResponse("No post found with this id.", status=404)
    return HttpResponse(response, content_type="application/json")


def init(request):
    for p in Post.objects.all():
        p.delete()
    for s in Seller.objects.all():
        s.delete()

    
    s = Seller(name="Stefan Vieru", email="stefan.vieru@student.tuiasi.ro")
    p = Post(title="Vand bicicleta", description="vand bicicleta cumparata in 2015",
              seller=s, image_url='s3_placeholder', pub_date=timezone.now())
    s.save()
    p.save()

    return HttpResponse("success")