from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Course

class CourseTests(APITestCase):
    
    def setUp(self):
        # 1. Setup runs before EVERY single test method.
        # We create two users: An Instructor and a Student.
        self.instructor = User.objects.create_user(username='instructor', password='password123')
        self.student = User.objects.create_user(username='student', password='password123')
        
        # Create a sample course owned by the instructor
        self.course = Course.objects.create(
            title="Intro to Python",
            description="Basics",
            price=20.00,
            instructor=self.instructor
        )
        
        # The URL for list/create actions
        self.list_url = reverse('course-list') # /api/courses/
        # The URL for detail actions (get/put/delete single item)
        self.detail_url = reverse('course-detail', args=[self.course.id]) # /api/courses/1/

    def test_create_course_with_modules(self):
        """
        Happy Path: Instructor creates a course with nested modules.
        """
        self.client.force_authenticate(user=self.instructor)
        
        payload = {
            "title": "Advanced DRF",
            "description": "Testing nested writes",
            "price": "50.00",
            "modules": [
                {
                    "title": "Module 1",
                    "order": 1,
                    "lessons": []
                }
            ]
        }
        
        response = self.client.post(self.list_url, payload, format='json')
        
        # Assertions: The computer checks if the result is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2) # Old one + New one
        self.assertEqual(Course.objects.last().modules.count(), 1) # Did module save?

    def test_student_cannot_delete_course(self):
        """
        Security Test: Student tries to delete Instructor's course.
        """
        self.client.force_authenticate(user=self.student)
        
        response = self.client.delete(self.detail_url)
        
        # Should be 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Course should still exist
        self.assertEqual(Course.objects.count(), 1)

    def test_price_validation(self):
        """
        Validation Test: Trying to create a course for $5.00.
        """
        self.client.force_authenticate(user=self.instructor)
        
        payload = {
            "title": "Cheap Course",
            "price": "5.00", # Too low!
            "modules": []
        }
        
        response = self.client.post(self.list_url, payload, format='json')
        
        # Should be 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check our custom error format (Level 3.7)
        self.assertIn("price", response.data['errors'])