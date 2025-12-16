from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from tasks.models import Task
from tasks.serializers import TaskSerializer, TaskUpdateSerializer 


class TaskViewSet(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'priority']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)