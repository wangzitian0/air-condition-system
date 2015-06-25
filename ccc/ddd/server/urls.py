from django.conf.urls import patterns, include, url
from server import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sform.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name = "index"),
    url(r'^(?P<roomid>\d+)/$', views.testboard, name='clientboard'),
    url(r'^test/(?P<roomid>\d+)/$', views.postboard, name='postboard'),
    url(r'^(?P<roomid>\d+)/daycost/$', views.testdaycost, name='testdaycost'),
    url(r'^(?P<roomid>\d+)/monthcost/$', views.testmonthcost, name='testmonthcost'),
#url(r'^show$', views.show, name = "show"),
#url(r'^submit$', views.submit, name = "submit"),
)
