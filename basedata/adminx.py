import xadmin

# Register your models here.


from .models import *
from xadmin import views


class ProjectAdmin(object):
    pass


class GlobalSetting(object):

    site_title ="志向OA后台管理系统"

    site_footer ="志向科技"

xadmin.site.register(views.CommAdminView,GlobalSetting)



xadmin.site.register(Project,ProjectAdmin)


class OutsourceAdmin(object):
    pass


xadmin.site.register(Outsource,OutsourceAdmin)


class deviceChangeAdmin(object):
    list_display = ['change_log', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                   'sale_price', 'total_price', 'buy_price', 'total_buy_price', 'reason']
    list_filter = ['change_log']


xadmin.site.register(Device_change,deviceChangeAdmin)





class Outsource_itemsAdmin(object):
    list_display = ['outsource_info', 'item_name', 'provider', 'num', 'price']
    list_filter = ['outsource_info', 'provider']
    order = ['thisid']

xadmin.site.register(Outsource_items,Outsource_itemsAdmin)


class DeviceRecord(object):

    list_display = ['device_form', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price','total_price', 'insurance',
                                     'Inquiry_price','insurance_g', 'buy_price','total_buy_price','buy_from','insurance_to','tiaojian','time_deliver']

    list_filter = ['device_form','brand','buy_from','time_deliver']



xadmin.site.register(Device,DeviceRecord)



class Material_useAdmin(object):
    list_display = ['material_log', 'material_name', 'brand', 'xinhao', 'guige', 'num', 'unit', 'price', 'total_price']
    list_filter = ['material_log', 'material_name']


xadmin.site.register(Material_use,Material_useAdmin)


class Device_finalAdmin(object):
    list_display = ['name', 'brand', 'type', 'specification', 'producer', 'produce_num', 'produce_time', 'place_keep',
     'bill_num', 'price',
     'time_install', 'record', 'note']
    list_filter = ['form','brand', 'producer','type']


xadmin.site.register(Device_final,Device_finalAdmin)



class Finish_reportAdmin(object):
    pass


xadmin.site.register(Finish_report,Finish_reportAdmin)


class work_hourAdmin(object):
    list_display = ['work_report','employee','start_time','finish_time','time','work_content','inside_work_hour','inside_price','extra_work_hour'
                ,'extra_price','total_price']
    list_filter = ['employee', 'start_time']
    ordering = ['-start_time']


xadmin.site.register(work_hour,work_hourAdmin)


class feedback_reportAdmin(object):
    list_display = ['idnum', 'item', 'standard', 'points', 'self_eva', 'eva', 'note']
    list_filter = ['feedback_form']
    ordering = ['feedback_form','idnum','standard']


xadmin.site.register(feedback_report,feedback_reportAdmin)


class HistoryAdmin(object):
    pass


xadmin.site.register(History, HistoryAdmin)


class TodoListAdmin(object):
    list_display = ['code', 'project', 'is_read', 'status', 'arrived_time']
    list_filter = ['status','user']

    def queryset(self):
        qs = super(TodoListAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(user=self.request.user)  # user是IDC Model的user字段

xadmin.site.register(TodoList, TodoListAdmin)

class WorknodeAdmin(object):

    def save_model(self, request, obj, form, change):

        obj.save()
        ps = Project.objects.filter(end_isnull = True)
        for p in ps:
            p.restart()
            p.save()

xadmin.site.register(Worknode, WorknodeAdmin)