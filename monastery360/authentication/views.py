# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework import status
# # # from rest_framework.permissions import AllowAny
# # # from rest_framework_simplejwt.tokens import RefreshToken
# # # from .models import User
# # # from .serializers import UserSignupSerializer, UserLoginSerializer
# # #
# # #
# # # class SignupView(APIView):
# # #     permission_classes = [AllowAny]
# # #
# # #     def post(self, request):
# # #         serializer = UserSignupSerializer(data=request.data)
# # #         if serializer.is_valid():
# # #             user = serializer.save()
# # #             return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
# # #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # #
# # #
# # # class LoginView(APIView):
# # #     permission_classes = [AllowAny]
# # #
# # #     def post(self, request):
# # #         serializer = UserLoginSerializer(data=request.data)
# # #         if serializer.is_valid():
# # #             user = serializer.validated_data
# # #             refresh = RefreshToken.for_user(user)
# # #             return Response({
# # #                 "message": "Login successful",
# # #                 "refresh": str(refresh),
# # #                 "access": str(refresh.access_token),
# # #             }, status=status.HTTP_200_OK)
# # #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # #
# # #
# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework import status
# # # from rest_framework.permissions import IsAuthenticated
# # # from rest_framework.authentication import TokenAuthentication
# # # from rest_framework.authtoken.models import Token
# # #
# # # class TokenLogoutView(APIView):
# # #     authentication_classes = [TokenAuthentication]
# # #     permission_classes = [IsAuthenticated]
# # #
# # #     def post(self, request):
# # #         # Delete token of the logged-in user
# # #         Token.objects.filter(user=request.user).delete()
# # #         return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
# # #
# # #
# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework import status
# # # from rest_framework.permissions import IsAuthenticated
# # # from rest_framework.authentication import TokenAuthentication
# # # from rest_framework.authtoken.models import Token
# # #
# # # class TokenLogoutView(APIView):
# # #     authentication_classes = [TokenAuthentication]
# # #     permission_classes = [IsAuthenticated]
# # #
# # #     def post(self, request):
# # #         # Delete the logged-in user's token to log them out
# # #         Token.objects.filter(user=request.user).delete()
# # #         return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
# # #
# #
# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from rest_framework.permissions import AllowAny
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from .models import User
# # from .serializers import UserSignupSerializer, UserLoginSerializer
# #
# #
# # class SignupView(APIView):
# #     permission_classes = [AllowAny]
# #
# #     def post(self, request):
# #         serializer = UserSignupSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = serializer.save()
# #             return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # class LoginView(APIView):
# #     permission_classes = [AllowAny]
# #
# #     def post(self, request):
# #         serializer = UserLoginSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = serializer.validated_data
# #             refresh = RefreshToken.for_user(user)
# #             return Response({
# #                 "message": "Login successful",
# #                 "refresh": str(refresh),
# #                 "access": str(refresh.access_token),
# #             }, status=status.HTTP_200_OK)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# #
#
#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSignupSerializer, UserLoginSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)