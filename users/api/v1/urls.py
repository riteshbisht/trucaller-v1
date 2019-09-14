from django.conf.urls import url
from django.contrib import admin
from .views import (
	UserCreateAPIView, RerieveProfileApiView,
	MarkNumberSpamApiView, SearchApiView, AddContactForUserApiView

)

urlpatterns = [
    url(r'^users/$', UserCreateAPIView.as_view(), name='create-user'),
    url(r'^me/$', RerieveProfileApiView.as_view(), name='get-user'),
    url(r'^mark-spam/$', MarkNumberSpamApiView.as_view(), name='mark-spam'),
    url(r'^search/$', SearchApiView.as_view(), name='search'),
    url(r'^add-contact/$', AddContactForUserApiView.as_view(), name='search'),

]
	