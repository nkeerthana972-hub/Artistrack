"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from dashboard.views import home,dashboard
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('', include('artists.urls')),
    path('', include('attendance.urls')),
    path('', include('injuries.urls')),
    path('', include('performances.urls')),
    path('captcha/', include('captcha.urls')),
    path('', include('trainings.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns += [
    path('admin-panel/', account_views.admin_panel, name='admin_panel'),
    # AJAX FILTER ENDPOINT (NO PAGE RELOAD)
    path('admin-panel/filter-logs/', account_views.filter_logs, name='filter_logs'),
]
