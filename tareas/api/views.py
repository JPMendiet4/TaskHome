from rest_framework import generics, status
from rest_framework.response import Response
from tareas.models import User, Homework
from tareas.api.serializer import UserSerializer, HomeworkSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        # POST method to create a new user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserReadAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(status=True)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'status': 'No se han agregado usuarios'})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer()
        response_data = serializer.delete(instance)
        return Response(response_data, status=status.HTTP_200_OK)


class HomeworkCreateAPIView(generics.CreateAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HomeworkReadAPIView(generics.ListAPIView):
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        return Homework.objects.filter(status='C' or 'P')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'status': 'No se han agregado usuarios'})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HomeworkUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class HomeworkDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer()
        response_data = serializer.delete(instance)
        return Response(response_data, status=status.HTTP_200_OK)