from rest_framework import serializers
from django.db import transaction
from .models import Course,Module,Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id','title','content', 'order']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many = True)

    class Meta:
        model = Module
        fields = ['id','title', 'order', 'lessons']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many = True)
    instructor = serializers.PrimaryKeyRelatedField(read_only = True)
    total_lessons = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'total_lessons', 'price', 'created_at', 'instructor', 'modules']

    def validate_price(self, value):
        if value< 10.00:
            raise serializers.ValidationError("Price must be at least $10.00.")
        return value
    
    def create(self, validated_data):

        modules_data = validated_data.pop('modules')

        request  = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['instructor'] = request.user
        else:
            raise serializers.ValidationError("Instructor  is required")

        with transaction.atomic():
            course = Course.objects.create(**validated_data)

            for module_data in modules_data:
                lessons_data = module_data.pop('lessons')

                module = Module.objects.create(course = course,**module_data)

                for lesson_data in lessons_data:
                    Lesson.objects.create(module=module, **lesson_data)

        return course            


