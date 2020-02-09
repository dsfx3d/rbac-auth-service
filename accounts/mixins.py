from django.http import Http404
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


class RelatedModelMixin:
    related_field = None
    related_model_class = None
    related_model_serializer_class = None
    payload_serializer_class = None

    def get_object(self):
        pk = self.kwargs.get('pk')
        return super().get_queryset().get(pk=pk)

    def get_related_field(self):
        if self.related_field is not None:
            return self.related_field
        raise NotImplementedError(
            f'''[RelatedModelMixin][{self.__class__.__name__}] either include a class property
             `related_field` or implement class method `get_related_field`'''
        )

    def get_payload_serializer_class(self):
        if self.payload_serializer_class is not None:
            return self.payload_serializer_class
        raise NotImplementedError(
            f'''[RelatedModelMixin][{self.__class__.__name__}] either include a class property
             `payload_serializer_class` or implement class method `get_payload_serializer_class`'''
        )

    def get_serializer_context(self):
        return dict(view=self.__class__)

    def get_payload_serializer(self):
        SerializerClass = self.get_payload_serializer_class()
        return SerializerClass(data=self.request.data, context=self.get_serializer_context())

    def get_related_model_class(self):
        if self.related_model_class is not None:
            return self.related_model_class
        raise NotImplementedError(
            f'''[RelatedModelMixin][{self.__class__.__name__}] either include a class property
             `related_model_class` or implement class method `get_related_model_class`'''
        )

    def process_related_model_instance(self, instance, *args, **kwargs):
        raise NotImplementedError(
            f'[RelatedModelMixin][{self.__class__.__name__}] `process_related_model_instance` not implemented'
        )

    def prepare_response(self, *args, **kwargs):
        raise NotImplementedError(
            f'[RelatedModelMixin][{self.__class__.__name__}] `prepare_response` not implemented'
        )

    def process_related_model(self, *args, **kwargs):
        payload_serializer = self.get_payload_serializer()

        if not payload_serializer.is_valid():
            raise ValueError(payload_serializer.errors)

        RelatedModel = self.get_related_model_class()
        related_instances = RelatedModel.objects.filter(
            id__in=payload_serializer.data.get(self.get_related_field())
        )
        for related_instance in related_instances:
            self.process_related_model_instance(related_instance, *args, **kwargs)

        return self.prepare_response(*args, **kwargs)


class AddRelatedEntityMixin(RelatedModelMixin):

    def patch(self, request, pk):
        return self.process_related_model()


class RemoveRelatedEntityMixin(RelatedModelMixin):

    def delete(self, request, pk):
        return self.process_related_model()


class RelatedEntityAPIView(AddRelatedEntityMixin, RemoveRelatedEntityMixin, ListAPIView):
    serializer_class = None

    def __init__(self, *args, **kwargs):
        self.processed = []

    def get_payload_serializer_class(self):
        return self.PayloadSerializer

    def get_queryset(self):
        queryset = super(ListAPIView, self).get_queryset()
        if self.request.method == 'GET':
            try:
                return self.get_related_queryset()
            except queryset.model.DoesNotExist:
                raise Http404
        return queryset

    def get_related_queryset(self):
        view_object = self.get_object()
        return getattr(view_object, self.get_related_field())

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return super(ListAPIView, self).get_serializer_class()
        else:
            return self.get_payload_serializer_class()

    def process_related_model_instance(self, instance):
        related_queryset = self.get_related_queryset()
        object_exists = related_queryset.filter(pk=instance.id).exists()

        if object_exists and self.request.method == 'DELETE':
            related_queryset.remove(instance)
        elif not object_exists and self.request.method == 'PATCH':
            related_queryset.add(instance)

        self.processed.append(instance.id)

    def prepare_response(self):
        PayloadSerializer = self.get_serializer_class()
        payload = {self.get_related_field(): self.processed}
        serializer_context = self.get_serializer_context()
        payload_serializer = PayloadSerializer(data=payload, context=serializer_context)
        if payload_serializer.is_valid():
            return Response(payload_serializer.data, status=status.HTTP_200_OK)
        return Response(payload_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    class PayloadSerializer(serializers.Serializer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            View = self.context.get('view')
            payload_field = getattr(View, 'related_field')
            self.fields[payload_field] = serializers.ListField(child=serializers.IntegerField())
