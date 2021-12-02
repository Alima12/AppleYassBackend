from .serializers import UserSerializer, RegisterSerializer, AddressSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from utils.base_permissions import AdminRequired, IsNotAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import  Response
from .models.Address import Address
from rest_framework.permissions import IsAuthenticated
from .models.images import Images


User = get_user_model()


class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminRequired)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminRequired)


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return user

    def put(self, request):
        user = request.user
        data = request.POST
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.national_code = data['national_code']
        user.save()
        if 'image' in request.FILES.keys():
            image = Images.objects.create(
                image=request.FILES['image'],
                owner=user
            )
            image.save()


        return Response(UserSerializer(user).data)


class RegisterUser(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsNotAuthenticated]


class AddressActionsView(APIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id, *args, **kwargs):
        user = request.user
        address = get_object_or_404(Address, owner__id=user.id, id=id)
        address.delete()
        return Response(status=204)

    def post(self, request, data=None):
        user = request.user
        data = request.POST
        address = Address.objects.create(
            city=data['city'],
            rest_of=data['rest_of'],
            owner=user
        )
        address.save()
        return Response(AddressSerializer(address).data)


