from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import LoginSerializer, RegistrationSerializer, StudentSerializer, UserProfileSerializer
from apps.payments.serializers import RegisterRequestSerializer


class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = CustomUser.objects.filter(
            email=email,
            activation_code=activation_code
        ).first()
        msg_ = (
            "User does not exist",
            "Activated!"
        )
        if not user:
            return Response(msg_, 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response(msg_[-1], 200)

    
class StudentsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = StudentSerializer


class RegisterCourseView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'register-request-data': serializer.data, 'payment-data': payment_data}, status=status.HTTP_201_CREATED, headers=headers)


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'

