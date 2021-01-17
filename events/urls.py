from django.urls import path
from . import views as event_views


urlpatterns = [
	path('', event_views.EventListView.as_view(), name='Kiet-Events'),
	path('<int:pk>/',event_views.EventDetailView.as_view(), name='Event-Info'),
	path('addEvent/', event_views.AddEvent.as_view(), name='add-Event'),
    path('updateEvent/<int:pk>', event_views.UpdateEvent.as_view(), name='update-Event'),
    path('addUpdate/', event_views.AddUpdate.as_view(), name='add-update'),
    path('changeUpdate/<int:pk>', event_views.UpdateUpdate.as_view(), name='change-update'),
]