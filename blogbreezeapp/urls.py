from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpageloader, name='home'),
    path('blog', views.bloglistingloader, name='blog'),
    path('contact', views.contactpageloader, name='contact'),
    path('blog/<int:id>', views.blogsingle, name='blogsingle'),
    path('login', views.login_view, name='login'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('signup', views.signup_view, name="signup"),
    path('dashboard-blog', views.dashboardbloglist, name="dashboardblog"),
    path('add-blog', views.addblogpageloader, name="addblog"),
    path('edit-blog/<int:id>', views.editblogpageloader, name="editblog"),
    path('delete-blog/<int:id>', views.deleteblogpage, name="delblog"),
    path('dashboard-cat', views.dashboardcatlist, name="dashboardcat"),
    path('dashboard-addcat', views.addcatloader, name="addcat"),
    path('dashboard-editcat/<int:id>', views.editcategorypage, name="editcat"),
    path('dashboard-delcat/<int:id>', views.deletecategorypage, name="deletecat"),
    path('dashboard-user', views.userlistpage, name="dashboarduser"),
    path('dashboard-adduser', views.adduserpage, name="dashboardadduser"),
    path('category/<int:id>', views.categorylistingpageloader, name="catsingle"),
    path('logout', views.logout_view, name="logout")
]