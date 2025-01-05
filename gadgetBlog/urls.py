"""
URL configuration for gadgetBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static
from Home import views as homeViews
from Blog import views as blogViews
from movies import views as moviesViews

admin.site.site_header ='gadgetBlog Admin'
admin.site.site_title='gadgetBlog Admin Panel'
admin.site.index_title='Welcome to gadgetBlog Admin Panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeViews.home,name="home"),
    path('about/', homeViews.about,name="about"),
    path('writer/', homeViews.writer,name="writer"),
    path('contact/', homeViews.contact,name="contact"),
    path('search/', homeViews.search,name="search"),
    path('signUp/', homeViews.handelSignup,name='handelSignup'),
    path('login/', homeViews.handellogin,name='handellogin'),
    path('logout/', homeViews.handellogout,name='handellogout'),
    path('blog/', blogViews.blogHome,name="blogHome"),
    path('blog/<slug:slug>', blogViews.blogPost, name='blogDetail'),
    path('postComment/',blogViews.postComment,name='postComment'),
    path('movies/', moviesViews.anime_list, name='anime_list'),
    path('movie/<int:movie_id>/', moviesViews.movie_detail, name='movie_detail'),    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
