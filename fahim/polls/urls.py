from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blogList/', views.BlogList.as_view(), name='blogList'),
    path('blogList/write/', views.CreateBlog.as_view(), name='create_blog'),
    path('gallery/', views.gallery, name='gallery'),
    # path('form/', views.form, name='form'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_profile/', views.user_change, name='user_change'),
    path('password/', views.pass_change, name='pass_change'),
    path('add-picture/', views.add_pro_pic, name='add_pro_pic'),
    path('change-picture/', views.change_pro_pic, name='change_pro_pic'),
    path('detail/<slug:slug>', views.blog_detail, name='blog_detail'),
    path('liked/<pk>/', views.liked, name='liked_post'),
    path('unliked/<pk>/', views.unliked, name='unliked_post'),
    path('my-blogs/', views.MyBlog.as_view(), name='my-blogs'),
    path('edit-blog/<pk>/', views.UpdateBlog.as_view(), name='edit_blog'),


]