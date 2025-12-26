from rest_framework import viewsets, permissions, filters
from django.db.models import Count
from .serializers import CourseSerializer
from .models import Course
from .permissions import IsInstructorOrReadOnly
from .pagination import Pagination
from django_filters.rest_framework import DjangoFilterBackend


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsInstructorOrReadOnly]

    queryset = (
        Course.objects.select_related('instructor').prefetch_related
    ('modules', 'modules__lessons').annotate
    (total_lessons=Count('modules__lessons')).all()
    )

    pagination_class = Pagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = {
        'price': ['gte', 'lte'],  
        'instructor': ['exact'], 
    }
    search_fields = ['title', 'description'] 
    ordering_fields = ['price', 'created_at']


    def perform_create(self, serializer):
        serializer.save()
