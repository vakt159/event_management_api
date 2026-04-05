import django_filters

from event_management.models import Event


class EventFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="date", lookup_expr="date")
    description = django_filters.CharFilter(field_name="description",
                                            lookup_expr="icontains")
    title = django_filters.CharFilter(field_name="title",
                                      lookup_expr="icontains")
    location = django_filters.CharFilter(field_name="location",
                                      lookup_expr="icontains")


    class Meta:
        model = Event
        fields = ["date", "description", "title", "location"]
