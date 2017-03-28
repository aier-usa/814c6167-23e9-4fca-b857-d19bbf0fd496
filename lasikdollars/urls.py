"""play URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from app1.views.main import (
    testing,
    main,
    how_to_use,
    encryption,
    benefits,
    demo,
    two_factor_authentication,
    our_story,
    gen_max_pwd_ap,
    partial_sharing)

from app1.views.PasswordCreate import PasswordCreate
from app1.views.PasswordUpdate import PasswordUpdate
from app1.views.PasswordDelete import PasswordDelete
from app1.views.PasswordDetail import PasswordDetail
from app1.views.PasswordList import PasswordList

from app1.views.AccessPointCreate import AccessPointCreate
from app1.views.AccessPointUpdate import AccessPointUpdate
from app1.views.AccessPointDelete import AccessPointDelete
from app1.views.AccessPointDetail import AccessPointDetail
from app1.views.AccessPointList import AccessPointList
from app1.views.ShowMeList import ShowMeList
from app1.views.AssignList import AssignList
from app1.views.ResetPasswordRequestView import \
    ResetPasswordRequestView

from app1.views.builtin_accounts import (
    user_logout,
    user_login,
    register,
    accounts_profile,
    accounts_user_change,
    accounts_user_change_done,
    accounts_password_reset_confirm,
    accounts_password_change,
    accounts_password_change_done,
    accounts_password_reset_done,
    accounts_password_reset_complete
)

from app1.views.export import export_one_user_info
from app1.views.import_info import import_one_user_info
from app1.views.password_and_partial_sharing import (
    link_together)


urlpatterns = [

    url(r'^testing/$', testing, name='testing'),

    url(r'^$', main, name='main'),
    url(r'^how-to-use/$', how_to_use, name="how_to_use"),

    url(r'^encryption/$',
        encryption,
        name="encryption"),

    url(r'^benefits/$',
        benefits,
        name="benefits"),

    url(r'^two-factor-authentication/$',
        two_factor_authentication,
        name="two_factor_authentication"),

    url(r'^our-story/$',
        our_story,
        name="our_story"),

    url(r'^partial-sharing/$',partial_sharing,
        name = "partial_sharing"),


    url(r'^gen/$', gen_max_pwd_ap, name = "gen_max_pwd_ap"),

    url(r'^admin/', admin.site.urls),
    url(r'^su/', admin.site.urls),
    url(r'^root/', admin.site.urls),

    url(r'^accounts/login/$',
        user_login, {}, name='login'),
    url(r'^accounts/logout/$',
        user_logout, {}, name='logout'),
    url(r'accounts/profile/$',
        accounts_profile,
        {}, name='accounts_profile'),

    url(r'^accounts/user_change/$',
        accounts_user_change,
        {}, name='user_change'),

    url(r'^accounts/user_change_done/$',
        accounts_user_change_done,
        {}, name='user_change_done'),

    url(r'^accounts/register/$',
        register,
        {}, name='register'),

    url(r'^accounts/password_change/$',
        accounts_password_change,
        {}, name='password_change'),

    url(r'^accounts/password_change/done/$',
        accounts_password_change_done,
        {}, name='password_change_done'),

    url(r'^accounts/password_reset/$',
        ResetPasswordRequestView.as_view(),
        {}, name='password_reset'),
    url(r'^accounts/password_reset/done/$',
        accounts_password_reset_done,
        {}, name='password_reset_done'),

    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        accounts_password_reset_confirm,
        {}, name='password_reset_confirm'),

    url(r'^accounts/reset/done/$',
        accounts_password_reset_complete,
        {}, name='password_reset_complete'),

    url(r'^export_one_user_info/$',
        export_one_user_info,
        {}, name='export_one_user_info'),

    url(r'^import_one_user_info/$',
        import_one_user_info,
        {}, name='import_one_user_info'),

    url(r'password/$',
        PasswordList.as_view(),
        name='password_list'),

    url(r'password/(?P<pk>[0-9]+)/$',
        PasswordDetail.as_view(),
        name='password_detail'),

    url(r'password/create/$',
        PasswordCreate.as_view(),
        name='password_create'),

    url(r'password/(?P<pk>[0-9]+)/update/$',
        PasswordUpdate.as_view(),
        name='password_update'),

    url(r'password/(?P<pk>[0-9]+)/delete/$',
        PasswordDelete.as_view(),
        name='password_delete'),

    url(r'accesspoint/$',
        AccessPointList.as_view(),
        name='access_point_list'),

    url(r'accesspoint/(?P<pk>[0-9]+)/$',
        AccessPointDetail.as_view(),
        name='access_point_detail'),

    url(r'accesspoint/create/$',
        AccessPointCreate.as_view(),
        name='access_point_create'),

    url(r'accesspoint/(?P<pk>[0-9]+)/update/$',
        AccessPointUpdate.as_view(),
        name='access_point_update'),

    url(r'accesspoint/(?P<pk>[0-9]+)/delete/$',
        AccessPointDelete.as_view(),
        name='access_point_delete'),

    url(r'showme/(?P<nameAP>[a-zA-Z][a-zA-Z0-9]*)/$',
        ShowMeList.as_view(),
        name='show_me_list'),

    url(r'assign/(?P<pk>[0-9]+)$',
        AssignList.as_view(),
        name='assign_list'),

    url(r'^assign/link_together$', link_together),
]
