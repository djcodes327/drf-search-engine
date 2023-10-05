from rest_framework import generics, mixins, authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin


class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # If we are having user we can also use below method.
        # serializer.save(user=self.request.user)
        title = serializer.validated_data['title']
        content = serializer.validated_data['content'] or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     user = self.request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=user)


class ProductDetailAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    """Product Detail API view."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = pk


class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    """Product Update API view."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


class ProductDeleteAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    """Product Delete API view."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


# class ProductCreateAPIView(generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def perform_create(self, serializer):
#         # If we are having user we can also use below method.
#         # serializer.save(user=self.request.user)
#         title = serializer.validated_data['title']
#         content = serializer.validated_data['content'] or None
#         if content is None:
#             content = title
#         serializer.save(content=content)

class ProductMixinView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):
    """Generic API View for Product."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, **args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, **args, **kwargs)


@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    """
    Function Based view for API requests.
    """
    method = request.method

    if method == "GET":
        """
        GET Product data.
        LIST Product data.
        url_args ? -> for filtering the data
        """
        if pk is not None:
            # Details View
            obj = get_object_or_404(Product, pk=pk)  # Raises 404 if not found
            data = ProductSerializer(obj, many=False).data
            return Response(data)

        # List View
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        """
        Create an Item/Product
        """
        # Passing the Received data to the serializer
        serializer = ProductSerializer(data=request.data)
        # Serializer checks if the data is valid or not.
        # Adding a raise_exception here will help us better with our
        # exception handling as it will handle the backend validation.
        if serializer.is_valid(raise_exception=True):
            # We are saving instance of the Product Object
            # a like we do with forms for that -> Instance = ProductForm.save()
            title = serializer.validated_data['title']
            content = serializer.validated_data['content'] or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)

        return Response({"invalid": "Please Enter a valid data!"}, status=400)
