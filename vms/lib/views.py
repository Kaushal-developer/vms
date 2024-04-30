import logging

from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from . import constants, mixins
from .helpers import get_response_message
from .renderer import CustomJSONRenderer

logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    renderer_classes = [CustomJSONRenderer]


class BaseGenericViewSet(mixins.ViewSetMixin, viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter)

    model = None
    filterset_class = None

    class Meta:
        abstract = True

    @action(methods=[constants.Method.GET], detail=False)
    def choices(self, queryset, *args, **kwargs):
        response = BaseViewSet.get_choices_for_model_fields(self.model)
        return Response(data=response, status=status.HTTP_200_OK)

'''
Custom View set which have all the customize CRUD methods With custom response message benefits
'''
class BaseViewSet(mixins.ViewSetMixin, viewsets.ModelViewSet):
    model = None
    filterset_class = None
    view_serializers = {}
    http_method_names = [
        constants.Method.GET,
        constants.Method.HEAD,
        constants.Method.OPTIONS,
        constants.Method.POST,
        constants.Method.PATCH,
        constants.Method.PUT,
        constants.Method.DELETE
    ]

    def get_serializer_class(self):
        serializer_dict = self.view_serializers

        if not serializer_dict:
            return self.serializer_class

        request_action = self.action
        if request_action == constants.Action.LIST:
            return serializer_dict[request_action]
        return serializer_dict[constants.Action.RETRIEVE]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response = {
            "response_data": response_data,
            "message": get_response_message(response_data, self.model, self.action)
        }
        return Response(data=response, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        response_data = serializer.data
        response = {
            "response_data": response_data,
            "message": get_response_message(response_data, self.model, self.action)
        }
        return Response(data=response, status=status.HTTP_200_OK)

    @action(methods=[constants.Method.GET], detail=True)
    def view(self, queryset, *args, **kwargs):
        obj = self.get_object()
        serializer = self.view_serializers[self.action](obj, context={"request": self.request})
        return Response(serializer.data)

    @action(methods=[constants.Method.GET], detail=False)
    def select(self, queryset, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset=queryset)

        paginated_queryset = self.paginate_queryset(filtered_queryset)
        if paginated_queryset is not None:
            serializer = self.view_serializers[self.action](paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(self.view_serializers[self.action](filtered_queryset, many=True).data)

    @action(methods=[constants.Method.GET], detail=False)
    def choices(self, queryset, *args, **kwargs):
        response = BaseViewSet.get_choices_for_model_fields(self.model)
        return Response(data=response, status=status.HTTP_200_OK)

    def destroy(self, queryset, *args, **kwargs):
        try:
            instance = self.get_object()
            obj_name = str(instance)
            instance  # Get the object to delete
            instance.delete()  # Delete the object
            return Response(data= {
            "response_data": {},
            "message": obj_name + ' Removed Successfully'
        },status=status.HTTP_204_NO_CONTENT)  # Return a successful response
        except Exception as e:
            return Response({'error': 'No Data Found'}, status=status.HTTP_400_BAD_REQUEST)  # Return an error response if deletion fails
        
