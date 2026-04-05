from rest_framework.routers import DefaultRouter

from event_management.views import EventViewSet

app_name = "event"

router = DefaultRouter()
router.register("event", EventViewSet, basename="events")

urlpatterns = router.urls
