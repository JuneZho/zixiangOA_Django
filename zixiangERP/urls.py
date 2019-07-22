"""zixiangERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import TemplateView
from basedata.admin import admin_site
import xadmin
import zixiangERP.view
urlpatterns = [
    path('admin/', admin_site.urls),
    path('xadmin/', xadmin.site.urls),
    path('',zixiangERP.view.home),

    path('deviceInfo/<int:project_id>',zixiangERP.view.deviceInfo,name='toDevice'),
    path('HRInfo/<int:project_id>', zixiangERP.view.workH),
    path('devicesChangeInfo/<int:project_id>', zixiangERP.view.deviceChange),
    path('StockInfo/<int:project_id>', zixiangERP.view.stock),
    path('devicesFinalInfo/<int:project_id>',zixiangERP.view.deviceFinal),
    path('FinalReportInfo/<int:project_id>', zixiangERP.view.finalReport),
    path('EvaluationInfo/<int:project_id>', zixiangERP.view.Evalu),
    path('outSource/<int:project_id>', zixiangERP.view.outSource),

    path('outSourceItem/<int:outSource_id>', zixiangERP.view.outItem),

    path('export/<int:obj_id>/export.xlsx', zixiangERP.view.export),

    path('next/<int:type>/<int:project_id>', zixiangERP.view.next),

]