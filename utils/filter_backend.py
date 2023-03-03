from django_filters.rest_framework import DjangoFilterBackend
import copy


class FilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if view.action == "retrieve" or view.action == "partial_update":
            return queryset
        return super().filter_queryset(request, queryset, view)
