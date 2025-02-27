from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task, Project
from .serializers import UserSerializer, TaskSerializer, ProjectSerializer
from .permissions import IsSuperUser  

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=400)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "is_staff": user.is_staff,  
                "is_superuser": user.is_superuser 
            })
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.request.method == "POST":  # Creating a task
    #         return [permissions.IsAuthenticated(), IsSuperUser()]  # Only superusers can create
    #     return [permissions.IsAuthenticated()]  # Normal users can view

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:  
            return [permissions.IsAuthenticated(), IsSuperUser()]  
        return [permissions.IsAuthenticated()] 

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST": 
            return [permissions.IsAuthenticated(), IsSuperUser()]  
        return [permissions.IsAuthenticated()]  

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer