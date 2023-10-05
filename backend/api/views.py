import json

from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer


# Create your views here.

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View.
    """
    # Passing the Received data to the serializer
    serializer = ProductSerializer(data=request.data)
    print("Request Data : ", request.data)
    print("Request Params : ", request.GET)
    # Serializer checks if the data is valid or not.
    # Adding a raise_exception here will help us better with our
    # exception handling as it will handle the backend validation.
    if serializer.is_valid(raise_exception=True):
        # We are saving instance of the Product Object
        # a like we do with forms for that -> Instance = ProductForm.save()
        instance = serializer.save()
        print("Instance : ", instance)
        return Response(serializer.data)

    return Response({"invalid": "Please Enter a valid data!"})

# @api_view(["POST"])
# def api_home(request, *args, **kwargs):
#     """
#     DRF API View.
#     """
#     instance = Product.objects.all().order_by("?").first()
#     data = {}
#     if instance:
#         data = ProductSerializer(instance).data
#     return Response(data)
