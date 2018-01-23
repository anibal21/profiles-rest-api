from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('feed', views.UserProfileFeedViewSet)
router.register('image-upload', views.ImageUploadViewSet)
router.register('file-upload', views.FileUploadViewSet)
router.register('multi-upload', views.MultiUploadViewSet)
router.register('plan', views.PlanViewSet)
router.register('user_plan', views.UserPlanViewSet, base_name='user_plan')
router.register('delete_file', views.DeleteFileViewSet, base_name='delete_file')
router.register('user-process-history', views.UserProcessHistoryViewSet)
router.register('collector_login', views.LoginCollectorViewSet, base_name='collector_login')
router.register('add_code', views.AddCodeViewSet, base_name='add_code')
router.register('list_codes', views.ListCodesViewSet, base_name='list_codes')
router.register('collector_register', views.RegisterCollectorViewSet, base_name='collector_register')

urlpatterns = [
    url(r'^hello-view/', views.HelloApiView.as_view()),
    url(r'', include(router.urls))
]
