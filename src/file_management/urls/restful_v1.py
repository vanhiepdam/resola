from rest_framework.routers import DefaultRouter

from file_management.restful.v1.file import FileViewSetV1

router = DefaultRouter(trailing_slash=False)

router.register(r"^files", FileViewSetV1, basename="file")

urlpatterns = router.urls
