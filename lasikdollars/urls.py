"""lasikdollars URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings


from app1.views.main import (
    testing,
    main,
    how_to_use,
    gen_max_receipt,
    daily_all_data,
    users_joined_in_a_date,
    eyecare_q_and_a)

from app1.views.ReceiptCreate import ReceiptCreate
from app1.views.ReceiptUpdate import ReceiptUpdate
from app1.views.ReceiptDelete import ReceiptDelete
from app1.views.ReceiptDetail import ReceiptDetail
from app1.views.ReceiptList import ReceiptList

from app1.views.PrescriptionCreate import PrescriptionCreate
from app1.views.PrescriptionUpdate import PrescriptionUpdate
from app1.views.PrescriptionDelete import PrescriptionDelete
from app1.views.PrescriptionDetail import PrescriptionDetail
from app1.views.PrescriptionList import PrescriptionList


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


urlpatterns = [

    url(r'^testing/$', testing, name='testing'),

    url(r'^$', main, name='main'),
    url(r'^how-to-use/$', how_to_use, name="how_to_use"),

    url(r'^gen/$', gen_max_receipt, name = "gen_max_receipt"),

    url(r'^dailyalldata/$', daily_all_data, name="daily_all_data"),

    url(r'^eyecare-q-and-a/$', eyecare_q_and_a, name="eyecare_q_and_a"),

    url(r'^users-joined-in-a-date/(?P<date_joined>[0-9\-]+)$',
        users_joined_in_a_date, name="users_joined_in_a_date"),

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

    url(r'receipts/$',
        ReceiptList.as_view(),
        name='receipts'),

    url(r'receipt/(?P<pk>[0-9]+)/$',
        ReceiptDetail.as_view(),
        name='receipt_detail'),

    url(r'receipt/create/$',
        ReceiptCreate.as_view(),
        name='receipt_create'),

    url(r'receipt/(?P<pk>[0-9]+)/update/$',
        ReceiptUpdate.as_view(),
        name='receipt_update'),

    url(r'receipt/(?P<pk>[0-9]+)/delete/$',
        ReceiptDelete.as_view(),
        name='receipt_delete'),

    url(r'prescriptions/$',
        PrescriptionList.as_view(),
        name='prescriptions'),

    url(r'prescription/(?P<pk>[0-9]+)/$',
        PrescriptionDetail.as_view(),
        name='prescription_detail'),

    url(r'prescription/create/$',
        PrescriptionCreate.as_view(),
        name='prescription_create'),

    url(r'prescription/(?P<pk>[0-9]+)/update/$',
        PrescriptionUpdate.as_view(),
        name='prescription_update'),

    url(r'prescription/(?P<pk>[0-9]+)/delete/$',
        PrescriptionDelete.as_view(),
        name='prescription_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
