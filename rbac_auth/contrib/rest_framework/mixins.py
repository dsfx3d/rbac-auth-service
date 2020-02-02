from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rbac_auth.utils import is_sequence


class DestroyModelMixin(mixins.DestroyModelMixin):
    """
    Destroy a model instance with soft delete support.
    """
    soft_delete_field = None

    def get_soft_delete_field(self):
        if self.soft_delete_field is None:
            raise ValueError('[error][DestroyModelMixin] soft_delete_field is not set')

        if is_sequence(self.soft_delete_field):
            if len(self.soft_delete_field) > 1:
                return self.soft_delete_field
            else:
                raise ValueError(
                    '[error][DestroyModelMixin] soft_delete_field must be in this template (field, value)'
                )

        return self.soft_delete_field

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        soft_delete = request.GET.get('soft', False) == '1'

        if not soft_delete:
            return super(DestroyModelMixin, self).destroy(request, *args, **kwargs)

        try:
            soft_delete_field = self.get_soft_delete_field()
            if is_sequence(soft_delete_field):
                soft_delete_field, value = soft_delete_field
            else:
                value = False
        except ValueError as e:
            return Response({'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(instance, soft_delete_field):
            setattr(instance, soft_delete_field, value)
            instance.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {'details': f'invalid soft_delete_field: {self.soft_delete_field}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class SummarySerializerMixin:
    summary_serializer_class = None
    summary_query_param = 'summary'

    def get_summary_serializer_class(self):
        return self.summary_serializer_class

    def get_summary_query_param(self):
        return self.summary_query_param

    def get_serializer_class(self):
        serializer_class = super(SummarySerializerMixin, self).get_serializer_class()

        summary = self.request.GET.get(self.get_summary_query_param(), False)

        if summary:
            summary_serializer = self.get_summary_serializer_class()
            if summary_serializer is not None:
                return summary_serializer

        return serializer_class
