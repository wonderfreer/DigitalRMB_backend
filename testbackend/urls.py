"""testbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from django.views.generic import TemplateView
from testbackend import dododoo

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="front_page.html")),
    url(r'^api/test',dododoo.test),
    url(r'^api/judge_sms',dododoo.judge_sms),
    url(r'^api/get_form_data',dododoo.account_open),
    url(r'^api/bind_bank',dododoo.bind_bank)
]
