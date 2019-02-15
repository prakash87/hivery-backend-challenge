from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from paranuara.models import Company, Person
from paranuara.serializers import CompanyDetailSerializer, CompanyListSerializer, \
    PersonListSerializer, PersonFoodDetailSerializer, PersonContactDetailSerializer


class CompanyList(generics.ListAPIView):
    """
    List all the companies
    """
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer


class CompanyDetail(generics.RetrieveAPIView):
    """
    Retrieve information of an individual company and their employees. If no employees found, return an empty list.
    It is up to the API clients how they want to handel this information.
    """
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer


class PersonList(generics.ListAPIView):
    """
    List all people
    """
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer


class PersonDetail(generics.RetrieveAPIView):
    """
    Retrieve information of a person including favorite fruits and vegetables in following format as required -
    {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}
    """
    queryset = Person.objects.all()
    serializer_class = PersonFoodDetailSerializer


class PersonCompare(APIView):
    """
    Retrieve information of two or more people, show their following in common.
    """
    def get(self, request, comma_separated_ids, format=None):
        person_ids = comma_separated_ids.split(',')
        filter_by = dict(request.GET.items())

        people = Person.objects.filter(id__in=person_ids)
        people_serializer = PersonContactDetailSerializer(people, many=True)

        queryset = Person.objects
        for person_id in person_ids:
            queryset = queryset.filter(followers=person_id)

        queryset = queryset.filter(**filter_by)

        common_in_following_serializer = PersonContactDetailSerializer(queryset, many=True)

        return Response({
            'people': people_serializer.data,
            'following_in_common': common_in_following_serializer.data
        })
