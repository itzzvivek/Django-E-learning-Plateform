from rest_framework import generics
from ..models import Subject,Course
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SubjectSerializer
from rest_framework.authentication import BasicAuthentication

class CourseEnrollView(APIView):
    authentication_classes = (BasicAuthentication)

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CourseEnrollView(APIView):
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        course.studets.add(request.user)
        return Response({'enrolled':True})