
# coding = utf-8
from django.contrib import admin
from basedata import models as mymodels
from zixiangERP import view
from django.contrib import messages
from django.db import models
from django.http import HttpResponseRedirect
from zixiangERP.settings import BASE_DIR
import xlrd
from django.contrib.admin.templatetags.admin_modify import register, submit_row as original_submit_row
from django.forms import widgets

from django.contrib.admin import AdminSite



class MyAdminSite(AdminSite):
    site_header = '志向科技OA管理'
    site_title = '志向'


admin_site = MyAdminSite(name='myadmin')

def sub_can_return(model,curuser):

    return model.get_last_user_rank().title == curuser.title



@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ''' submit buttons context change '''
    ctx = original_submit_row(context)
    ctx.update({
    'show_save_and_add_another': context.get('show_save_and_add_another',
                                             ctx['show_save_and_add_another']),
    'show_save_and_continue': context.get('show_save_and_continue',
                                          ctx['show_save_and_continue']),
    'show_save': context.get('show_save',
                             ctx['show_save']),
    'show_delete_link': context.get('show_delete_link', ctx['show_delete_link'])
    })
    return ctx


from .models import *
ROLES = ('普通员工','总经理',
             '商务经理',
             '财务经理',
             '工程经理',
             '技术经理',
             '库管','营销经理','行政经理','技术中心经理','档案室','商务助理')

def get_edible_user(pro):
    if pro.WORK_FLOW_NODE[pro.workflow_node][1] == '普通员工':
        curuser = pro.manager
    elif pro.workflow_node == 0:
        curuser = pro.get_starter()
    elif pro.WORK_FLOW_NODE[pro.workflow_node][1] == '完成':
        curuser = None
    else:
        curuser = user_models.Employee.objects.get(title=ROLES.index(pro.WORK_FLOW_NODE[pro.workflow_node][1]))
    return curuser

def to_next(obj,proc,user,memo,type,agree=True):
    TodoList.objects.filter(project = obj.project_info,content_type=type).delete()
    if agree:
        obj.to_next()
    else:
        obj.go_back()
    History.objects.create(project = obj.project_info,pro_type = proc,user=user, memo=memo)


def make_number(objects):
    i = 1
    for model in objects:
        model.thisid = i
        print(str(model.thisid))
        i += 1
        model.save()

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基础信息", {'fields': ['begin', 'starter', 'name', 'contract', 'total_price','kaipiao']}),
        ("客户及付款人信息", {
            'fields': [('cusname', 'cusaddr'), ('recname', 'recaddr'), ('receiver', 'receiverdep'),
                                 ('receivertele', 'receiverphone'), ('payer', 'payerdep'), ('payertele', 'payerphone')]}),
        ("其他", {'fields': [
            ('end', 'deliver_time'), 'manager', 'description', 'associated_file',
                           ('niehe_hour', 'total_hour', 'hour_cost'), ('total_out', 'total_mat', 'total_money'),
                           'workflow_node','comment']}),

        )

    def get_queryset(self, request):

        qs = super(ProjectAdmin, self).get_queryset(request)
        if request.user.title == 0:
            return qs.filter(id = request.user.recent_pro)
        return qs

    def _changeform_view(self, request, object_id, form_url, extra_context):

        if "_confirm" in request.POST:
            ModelForm = self.get_form(request)

            form = ModelForm(request.POST, request.FILES)

            form_validated = form.is_valid()

            if form_validated:
                new_object = form.save(commit=False)

                context = {

                    **self.admin_site.each_context(request),

                    'obj': new_object,

                    'opts': self.model._meta,

                    'form': form,

                }
                from django.template.response import TemplateResponse
                return TemplateResponse(

                    request, 'admin/basedata/form_confirmation.html', context)

        return super()._changeform_view(request, object_id, form_url, extra_context)

    def get_changeform_initial_data(self, request):
        return {'starter': request.user}

    def get_readonly_fields(self, request, obj=None):

        if obj==None: ##adding
            return ['workflow_node', 'total_price', 'manager', 'active', 'niehe_hour', 'total_hour', 'total_mat',
                    'total_money','hour_cost','total_out']
        elif request.user.title ==4:
            return ['active','begin','starter','name','cusname',
                    'cusaddr','recname','recaddr','receiver',
                    'receiverdep','receiverphone','receivertele',
                    'payer','payerdep','payerphone','payertele','total_price','kaipiao','contract','deliver_time',
                    'description','associated_file','total_hour','total_mat','total_money','niehe_hour','workflow_node','hour_cost','total_out']
        elif request.user ==obj.starter:
            return ['workflow_node', 'total_price', 'manager', 'active', 'niehe_hour', 'total_hour', 'total_mat',
                    'total_money','hour_cost','total_out']
        elif request.user == obj.manager:
            return ['active', 'begin', 'starter', 'name', 'cusname',
                    'cusaddr', 'recname', 'recaddr', 'receiver',
                    'receiverdep', 'receiverphone', 'receivertele',
                    'payer', 'payerdep', 'payerphone', 'payertele', 'total_price', 'kaipiao','deliver_time','manager',
                    'description', 'associated_file', 'total_hour', 'total_mat', 'total_money','niehe_hour','workflow_node','end','hour_cost','contract','total_out']
        else:

            return  ['active', 'begin', 'starter', 'name', 'cusname',
                    'cusaddr', 'recname', 'recaddr', 'receiver',
                    'receiverdep', 'receiverphone', 'receivertele',
                    'payer', 'payerdep', 'payerphone', 'payertele', 'total_price', 'kaipiao','deliver_time','manager',
                    'description', 'associated_file', 'total_hour', 'total_mat', 'total_money','niehe_hour','workflow_node','end','hour_cost','contract','total_out']


    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """

        :param request:
        :param object_id:
        :param form_url:
        :param extra_context:
        :return:
        """

        '''store recent project'''
        request.user.recent_pro = object_id
        request.user.save()

        show_save = False
        show_workflow_line = False
        can_edit = False
        show_save_and_continue = False

        if object_id != None:  #change

            show_workflow_line = True
            obj = Project.objects.get(id = object_id)
            curuser = get_edible_user(obj)

            if request.user == curuser:
                show_submit_button = True
                show_save = True
                show_save_and_continue = True

            todo = TodoList.objects.filter(user=request.user,project = obj)
            unread = todo.filter(is_read=0)
            if unread.count() > 0:
                import datetime
                unread.update(is_read=1, read_time=datetime.datetime.now())

        else:
            show_save_and_continue = False
            show_save = True

        extra_context = extra_context or {}
        ctx = dict(
            show_workflow_line = show_workflow_line,
            can_edit=can_edit,
            instance_id=object_id,
            show_save_and_add_another = False,
            show_delete_link = show_save_and_continue,
            show_save = show_save,
            show_save_and_continue = show_save_and_continue
        )

        extra_context.update(ctx)
        return super(ProjectAdmin, self).changeform_view(request, object_id, form_url, extra_context)


    def save_model(self, request, obj, form, change):

        msg = ''
        if change:

            '''update project fields'''
            Ds = Device_form.objects.get(project_info=obj)
            total = Ds.total_price
            obj.total_price = total

            ms = Material_log.objects.filter(project_info=obj)
            hs = work_hour.objects.filter(work_report = work_report.objects.get(project_info=obj))
            total = 0
            money = 0
            for h in hs:
                total += h.inside_work_hour + h.extra_work_hour
                money += h.inside_work_hour * 100 + h.extra_work_hour * 200
            obj.total_hour = total
            obj.hour_cost = money

            total_material = 0
            for m in ms:
                total_material += m.total
            obj.total_mat = total_material

            other_price = Outsource.objects.get(project_info = obj).total_price
            obj.total_money = total + money + other_price





            '''project to next'''

            if "_next" in request.POST:
                '''project workflow submit requirment'''

                if request.user.title == 4:
                    '''工程经理'''
                    if form.cleaned_data['manager'] == None:
                        msg += "未指派项目经理,修改失败"

                        self.message_user(request, msg)

                        return
                    else:
                        obj.save()

                elif request.user == obj.manager:
                    dict = ('竣工报告', '项目经理自评', '设备更改', '设备信息', '工时记录', '材料领取')
                    try:
                        result = [Finish_report.objects.get(project_info=obj).agreed,
                                  feedback_form.objects.get(project_info=obj).agreed,
                                  Device_finalform.objects.get(project_info=obj).agreed]
                    except Exception as e:
                        self.message_user(request, "信息不全，无法提交")
                        return
                    if False in result:
                        self.message_user(request, '分流程: ' + dict[result.index(False)] + ' 未完成审批，无法提交')
                        return

                    else:
                        obj.save()



                todo_list = TodoList.objects.filter(project=obj, user=request.user,content_type=1)
                if todo_list.count() > 0:
                    TodoList.objects.filter(user=request.user,  project=obj,content_type=1).delete()
                    obj.to_next()
                    History.objects.create(project=obj, user=request.user, pro_type=1)
                    if obj.WORK_FLOW_NODE[obj.workflow_node][1] != '普通员工':
                        msg += "提交成功，进入下一工作流 "+obj.WORK_FLOW_NODE[obj.workflow_node][1]
                    else:

                        msg += "提交成功，进入下一工作流 项目经理"+obj.manager.first_name+obj.manager.last_name


                    self.message_user(request, msg)


        else:
            '''initial project add'''
            obj.save()
            Outsource.objects.create(project_info=obj)
            Finish_report.objects.create(project_info=obj)
            History.objects.create(project=obj, user=request.user, pro_type=0)
            TodoList.objects.create(project=obj, user=request.user,content_type=1)
            Device_form.objects.create(project_info=obj)
            Device_finalform.objects.create(project_info=obj)
            work_report.objects.create(project_info = obj)
            Material_log.objects.create(project_info= obj)
            ff = feedback_form.objects.create(project_info = obj)
            feedback_report.objects.create(feedback_form = ff,idnum=1,item = '要货及施工计划',points = 6, standard='（1）施工前进行施工现场踏勘，提前消化合同执行报告，制定合理清晰的施工方案； ')
            feedback_report.objects.create(feedback_form = ff,idnum=1,item = '要货及施工计划',points = 2,standard='（2）内外部沟通协调顺畅； ')
            feedback_report.objects.create(feedback_form = ff,idnum=1,item = '要货及施工计划',points = 2,standard='（3）人员、设备、辅材辅料、配件、施工机具等准备充分合理； ')
            feedback_report.objects.create(feedback_form = ff,idnum=1,item = '要货及施工计划',points = 5,standard='（4）制定项目要货计划合理，货到公司库房不超过两周。')
            feedback_report.objects.create(feedback_form = ff,idnum=2,item = '进度',points = 15,standard=' 按施工进度计划施工作业，无特殊情况下能按时间节点管控工程，如期交付。')
            feedback_report.objects.create(feedback_form = ff,idnum=3,item = '质量',points = 3,standard='（1）产品保护良好；   ')
            feedback_report.objects.create(feedback_form = ff,idnum=3,item = '质量',points = 2,standard='（2）施工现场秩序井然，无脏、乱、差现象； ')
            feedback_report.objects.create(feedback_form = ff,idnum=3,item = '质量',points = 15,standard='（3）无较大质量问题，一次性通过外部验收，无整改或只有局部整改项。 ')
            feedback_report.objects.create(feedback_form=ff, idnum=4,item = '用料',points = 15,standard='根据最终出库数量和现场测量进行评定，若损耗＞10%，则此项计0分。')
            feedback_report.objects.create(feedback_form=ff, idnum=5,item = '用工',points = 5,standard='（1）工时绩效表中针对项目成员的工时考评合理；')
            feedback_report.objects.create(feedback_form=ff, idnum=5,item = '用工',points = 10,standard='（2）根据项目具体情况，总工时控制合理。')
            feedback_report.objects.create(feedback_form=ff, idnum=6,item = '安全规范',points = 5,standard=' 施工现场无违反安全作业规范行为。 ')
            feedback_report.objects.create(feedback_form=ff, idnum=7,item = '验收',points = 3,standard='（1） 验收电子及纸质资料：验收报告、施工日志、材料报验申请、设备移交记录、调试检测记录、试运行记录； ')
            feedback_report.objects.create(feedback_form=ff, idnum=7,item = '验收',points = 3,standard='（2）设备信息登录齐全； ')
            feedback_report.objects.create(feedback_form=ff, idnum=7,item = '验收',points = 4,standard='（3）对整改项及时处理无遗留问题； ')
            feedback_report.objects.create(feedback_form=ff, idnum=7,item = '验收',points = 2,standard='（4）积极及时协调客户、通知营销人员协调组织验收； ')
            feedback_report.objects.create(feedback_form=ff, idnum=8,item = '合理化建议',points = 3,standard=' 项目施工过程中提出合理化建议，完工后自觉进行总结并提交书面报告。')







    def delete_model(self, request, obj):
        if request.user == obj.starter and obj.WORK_FLOW_NODE[obj.workflow_node][1] == '合同签约人':
            obj.active = False
            obj.name = obj.name + " 由合同签约人终止"
            TodoList.objects.filter(user=request.user, project=obj,content_type=1).delete()
            History.objects.create(project=obj, user=request.user, pro_type=3)
            return
        else:

            TodoList.objects.filter(user=request.user, project=obj,content_type=1).delete()
            obj.go_back()
            History.objects.create(project=obj, user=request.user, pro_type=2)
            self.message_user(request, "已反对，回到上一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def response_change(self, request, obj):
        return HttpResponseRedirect('/admin/basedata/todolist')
    def response_add(self, request, obj):
        return HttpResponseRedirect('/admin/basedata/todolist')

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')





admin_site.register(Project,ProjectAdmin)


class ItemInfoInline(admin.TabularInline): # TabularInline

    formfield_overrides = {
        models.CharField:{'widget':widgets.TextInput(attrs={'size': 15})},
        models.IntegerField: {'widget': widgets.TextInput(attrs={'size': 3})},
        models.DecimalField: {'widget': widgets.TextInput(attrs={'size': 5})}
    }
    model = Outsource_items
    extra = 0
    def get_exclude(self, request, obj=None):
        id = request.user.recent_pro
        if id != 0:
            if request.user.title == 4:
                self.fields = ['thisid', 'item_name', 'provider', 'num', 'price', 'note', 'total_price']
                self.readonly_fields = ['total_price']

            else:
                self.fields = ['thisid', 'item_name', 'provider', 'num', 'price', 'note', 'total_price']
                self.readonly_fields = self.fields
        return []
class OutsourceAdmin(admin.ModelAdmin):

    inlines = [ItemInfoInline]
    list_display = ['myname', 'begin_time', 'fuzeren', 'end_time', 'total_price']

    def get_readonly_fields(self, request, obj=None):
        if request.user.title ==4:
            return ['total_price','workflow_node','project_info','agreed']
        else:
            return [f.name for f in self.model._meta.fields]

    def get_queryset(self, request):
        pros = ContentType.objects.get(app_label='basedata', model='project')
        try:
            pro = pros.model_class().objects.get(id=request.user.recent_pro)
        except Exception as e:
            return super(OutsourceAdmin, self).get_queryset(request)

        qs = super(OutsourceAdmin, self).get_queryset(request)
        return qs.filter(project_info=pro)


    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        show_return = False
        obj = Outsource.objects.get(id=object_id)
        if obj.workflow_node == 0:
            show_return = False
        elif sub_can_return(obj, request.user):
            show_return = True
        show_save = False
        show_save_and_continue = False
        show_delete_link = False
        show_submit_button = False
        pro = Project.objects.get(id = request.user.recent_pro)
        curuser = get_edible_user(pro)
        if curuser.title == 4:
            '''到达工程经理'''
            curuser = get_edible_user(Outsource.objects.get(id = object_id))
            if curuser == request.user:
                show_submit_button = True
                show_save = True
                show_delete_link = True
                show_save_and_continue = True


        extra_context = extra_context or {}

        if request.user == Project.objects.get(id = object_id).manager:
            show_delete_link = False
        '''WARNING: check for the user to show save'''
        ctx = dict(
            show_return= show_return,
            show_submit_button=show_submit_button,
            is_outSource=True,
            show_save_and_continue = show_save_and_continue,
            show_save_and_add_another=False,
            show_delete_link=show_delete_link,
            show_save=show_save,
            show_back = True,
            instance_id = request.user.recent_pro,
            show_workflow_line = True

        )

        extra_context.update(ctx)
        return super(OutsourceAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        pro = obj.project_info


        obj.save()
        '''update info'''
        if request.user.title == 4:
            self.message_user(request, "工作流内的修改")

            obj.save()
        if "_confirm" in request.POST:
            to_next(obj,1,request.user,"提交了其他费用表格",2)
            self.message_user(request, "提交成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])


    def delete_model(self, request, obj):
        pro = obj.project_info
        if request.user.title == 4:
            self.message_user(request, "填写人无法反对")
        else:

            to_next(obj,2,request.user,"反对了其他费用表格",2,False)
            self.message_user(request, "反对成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])


    def response_change(self, request, obj):

        items = Outsource_items.objects.filter(outsource_info=obj)
        total = 0
        for it in items:
            total += it.num * it.price
            it.total_price = it.num * it.price
            it.save()
        obj.total_price = total
        obj.save()

        return HttpResponseRedirect(request.path)


    def response_add(self, request, obj):

        items = Outsource_items.objects.filter(outsource_info=obj)
        total = 0
        for it in items:
            total += it.num * it.price
            it.total_price = it.num * it.price
            it.save()
        obj.total_price = total
        obj.save()

        return HttpResponseRedirect(request.path)



admin_site.register(Outsource,OutsourceAdmin)



class Outsource_itemsAdmin(admin.ModelAdmin):
    list_display = ['thisid','item_name','provider','num','price']

    def get_queryset(self, request):
        pros = ContentType.objects.get(app_label='basedata', model='project')
        try:
            pro = pros.model_class().objects.get(id=request.user.recent_pro)
        except Exception as e:
            return super(Outsource_itemsAdmin, self).get_queryset(request)
        qs = super(Outsource_itemsAdmin, self).get_queryset(request)
        os = Outsource.objects.get(project_info= pro)
        return qs.filter(outsource_info=os)

    def _changeform_view(self, request, object_id, form_url, extra_context):

        if "_confirm" in request.POST:
            ModelForm = self.get_form(request)

            form = ModelForm(request.POST, request.FILES)

            form_validated = form.is_valid()

            if form_validated:
                new_object = form.save(commit=False)

                context = {

                    **self.admin_site.each_context(request),

                    'obj': new_object,

                    'opts': self.model._meta,

                    'form': form,

                }
                from django.template.response import TemplateResponse
                return TemplateResponse(

                    request, 'admin/basedata/form_confirmation.html', context)

        return super()._changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        if request.user.recent_pro != 0:
            oi = Outsource.objects.get(project_info=Project.objects.get(id=request.user.recent_pro))
            os = Outsource_items.objects.filter(outsource_info = oi)
            maxID = 0
            for o in os:
                if o.thisid>maxID:
                    maxID = o.thisid
            if request.user == Project.objects.get(id=request.user.recent_pro).manager:
                self.list_editable = ['item_name','provider','num','price']

            if len(Outsource_items.objects.filter(item_name = '---',outsource_info=Outsource.objects.get(oi))>0):
                pass
            else:
                newobj = Outsource_items.objects.create(thisid=maxID+1,item_name = "---", provider = "---",outsource_info=Outsource.objects.get(project_info = Project.objects.get(id=request.user.recent_pro)))
                newobj.save()
        else:
            self.message_user(request,"项目ID不存在，请重新获取")

        return super(Outsource_itemsAdmin, self).changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        pro = obj.outsource_info.project_info

        if request.user == pro.manager:
            self.message_user(request, "工作流内的修改")
            obj.save()
            obj.outsource_info.total_price += obj.price*obj.num
            obj.outsource_info.save()
        else:
            str = "您无权对该项目  " + pro.name + " 的其他费用文件修改，修改失败"
            self.message_user(request, str)

admin_site.register(Outsource_items,Outsource_itemsAdmin)



class DeviceInfoInline(admin.TabularInline): # TabularInline


    formfield_overrides = {
        models.CharField:{'widget':widgets.TextInput(attrs={'size': 12})},
        models.IntegerField: {'widget': widgets.TextInput(attrs={'size': 2})},
        models.DecimalField: {'widget': widgets.TextInput(attrs={'size': 5})},
        models.TextField: {'widget': widgets.Textarea(attrs={'cols': '20', 'rows': '2'})},

    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'unit':
            kwargs['widget'] = widgets.TextInput(attrs={'size': 2})
        if db_field.name == 'insurance' or db_field.name == 'insurance_g' or db_field.name == 'insurance_to':
            kwargs['widget'] = widgets.TextInput(attrs={'size': 5})

        return  super(DeviceInfoInline,self).formfield_for_dbfield(db_field, request, **kwargs)


    model = Device
    extra = 0
    def get_exclude(self, request, obj=None):
        id = request.user.recent_pro
        if id != 0:
            if request.user == Project.objects.get(id=request.user.recent_pro).starter:
                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price', 'total_price','insurance']


                self.readonly_fields = ['thisid','total_price']
            elif request.user.title == 2:
                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price','total_price', 'insurance',
                                     'Inquiry_price','insurance_g', 'buy_price','total_buy_price','buy_from','insurance_to','tiaojian','time_deliver']
                self.readonly_fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit', 'insurance',
                                     'sale_price','total_price','total_buy_price','Inquiry_price','insurance_g','time_deliver']

            elif request.user.title == 4:
                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                               'sale_price', 'total_price','insurance','time_deliver']
                self.readonly_fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                               'sale_price', 'total_price', 'insurance']
            elif request.user.title == 1 or request.user.title == 3 or  request.user.title == 7 or request.user.title == 5 or request.user.title == 9:

                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price','total_price', 'insurance',
                                     'Inquiry_price','insurance_g', 'buy_price','total_buy_price','buy_from','insurance_to','tiaojian','time_deliver']

                self.readonly_fields = self.fields
            elif request.user.title == 11:

                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                               'sale_price', 'total_price', 'insurance',
                               'Inquiry_price', 'insurance_g']
                self.readonly_fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price','total_price', 'insurance']
            else:
                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit', 'insurance',
                                     'sale_price', 'total_price']
                self.readonly_fields = self.fields
        return []


    def has_delete_permission(self, request, obj=None):
        return request.user == Project.objects.get(id = request.user.recent_pro).starter
    def has_add_permission(self, request):
        return request.user == Project.objects.get(id = request.user.recent_pro).starter




class DeviceFormAdmin(admin.ModelAdmin):
    inlines = [DeviceInfoInline]

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """

        :param request:
        :param object_id:
        :param form_url:
        :param extra_context:
        :return:
        """
        show_submit_button = False
        show_save = False
        extra_context = extra_context or {}
        pro = Device_form.objects.get(id = object_id).project_info
        if request.user == pro.starter and pro.workflow_node == 0:
            show_submit_button = True
            show_save = True
        elif (request.user.title == 2 and pro.WORK_FLOW_NODE[pro.workflow_node][1] =='商务经理') or (request.user.title == 11 and pro.WORK_FLOW_NODE[pro.workflow_node][1] =='商务助理') \
                or (request.user.title == 4 and pro.WORK_FLOW_NODE[pro.workflow_node][1] == '工程经理'):
            show_save = True
        ctx = dict(

            show_submit_button=show_submit_button,
            show_save_and_add_another = False,
            show_delete_link = False,
            show_save_and_continue = False,
            show_save = show_save,
            instance_id = pro.id,
            show_back = True,
            obj_id = object_id,
            show_out = True,
            show_workflow_line=True
        )

        extra_context.update(ctx)
        return super(DeviceFormAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.save_change()
        formset.save()
    def get_readonly_fields(self, request, obj=None):

        if request.user == obj.project_info.starter:
            self.exclude = ['total_buyprice']
            return ['project_info','total_price']
        elif request.user.title==1 or request.user.title==2 or request.user.title==3 or request.user.title==5 or request.user.title==7 or request.user.title==9 or request.user.title==11:
            self.exclude = ['file']
            return ['project_info','total_price','total_buyprice']
        else:

            self.exclude = ['total_buyprice','file']
            return ['project_info','total_price']




    def save_model(self, request, obj, form, change):
        import os
        obj.save()
        if obj.file != None and obj.file.name !='':
            workbook = xlrd.open_workbook(os.path.join(BASE_DIR, obj.file.name).replace('\\','/'))
            table = workbook.sheets()[0]
            if True:
                s = 2
                try:
                    for i in range(2,table.nrows):
                        s += 1
                        if len(table.row_values(i))<5:
                            break
                        if table.row_values(i)[1] is not '':
                            if len(Device.objects.filter(device_form = obj,
                                                  name = table.row_values(i)[1],
                                                  brand = table.row_values(i)[2],
                                                  type=table.row_values(i)[3],
                                                  specification=table.row_values(i)[4],
                                                  num=table.row_values(i)[5],
                                                  unit=table.row_values(i)[6],
                                                  sale_price=table.row_values(i)[7],
                                                  total_price=table.row_values(i)[8],
                                                  insurance=table.row_values(i)[9])) !=0:
                                print('exist in the database')



                            else:
                                Device.objects.create(device_form = obj,
                                                  thisid = table.row_values(i)[0],
                                                  name = table.row_values(i)[1],
                                                  brand = table.row_values(i)[2],
                                                  type=table.row_values(i)[3],
                                                  specification=table.row_values(i)[4],
                                                  num=table.row_values(i)[5],
                                                  unit=table.row_values(i)[6],
                                                  sale_price=table.row_values(i)[7],
                                                  total_price=table.row_values(i)[8],
                                                  insurance=str(table.row_values(i)[9])
                                                  )

                except Exception as e:
                    self.message_user(request, "失败"+' 第'+str(s)+'行'+e.__str__())
                    print("失败"+' 第'+str(s)+'行'+e.__str__())

            try:
                os.remove(os.path.join(BASE_DIR, obj.file.name))
                obj.file = None
                obj.save()
            except Exception as e:
                pass

        self.message_user(request, "成功")




    def response_change(self, request, obj):
        ds = Device.objects.filter(device_form=obj)
        total = 0
        total_buy = 0
        i = 1
        for d in ds:
            d.thisid = i
            i += 1
            d.save_change()
            total += d.get_total_sale_price()
            total_buy +=d.get_total_buy_price()
        obj.total_price = total
        obj.total_buyprice = total_buy
        obj.save()
        obj.project_info.total_price = total
        obj.project_info.save()
        return HttpResponseRedirect(request.path)

    def response_add(self, request, obj):
        ds = Device.objects.filter(device_form=obj)
        total = 0
        i = 1
        for d in ds:
            d.thisid = i
            d.save()
            i += 1
            total += d.get_total_sale_price()
        obj.total_price = total
        obj.save()
        obj.project_info.total_price = total
        obj.project_info.save()
        return HttpResponseRedirect('/admin/')

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')




admin_site.register(Device_form,DeviceFormAdmin)


class DCInfoInline(admin.TabularInline):

    formfield_overrides = {
        models.CharField:{'widget':widgets.TextInput(attrs={'size': 12})},
        models.IntegerField: {'widget': widgets.TextInput(attrs={'size': 2})},
        models.DecimalField: {'widget': widgets.TextInput(attrs={'size': 5})},
        models.TextField: {'widget': widgets.Textarea(attrs={'cols': '20', 'rows': '2'})},

    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'unit':
            kwargs['widget'] = widgets.TextInput(attrs={'size': 2})
        if db_field.name == 'insurance':
            kwargs['widget'] = widgets.TextInput(attrs={'size': 5})
        kwargs['widget'] = widgets.TextInput(attrs={'size': 5})

        return  super(DCInfoInline,self).formfield_for_dbfield(db_field, request, **kwargs)
    model = Device_change
    extra = 0
    def get_exclude(self, request, obj=None):
        id = request.user.recent_pro
        if id != 0:
            if request.user == Project.objects.get(id=request.user.recent_pro).starter:
                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price', 'total_price','reason','memo']


                self.readonly_fields = ['thisid','total_price','memo']
            elif request.user.title == 2:
                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price','total_price', 'buy_price','total_buy_price','reason','memo']
                self.readonly_fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price','total_price','reason','total_buy_price','memo']

            elif request.user.title == 1 or request.user.title == 3:
                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price','total_price', 'buy_price','total_buy_price','reason','memo']
                self.readonly_fields = self.fields
            else:
                self.fields = ['thisid', 'name', 'brand', 'type', 'specification', 'num', 'unit',
                                     'sale_price', 'total_price','reason','memo']
                self.readonly_fields = self.fields
        return []

    def has_delete_permission(self, request, obj=None):
        return request.user == Project.objects.get(id = request.user.recent_pro).starter
    def has_add_permission(self, request):
        return request.user == Project.objects.get(id = request.user.recent_pro).starter

class device_logAdmin(admin.ModelAdmin):
    inlines = [DCInfoInline]
    filter_horizontal = ('device',)



    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "device":
            kwargs['queryset']=Device.objects.filter(device_form__project_info_id = request.user.recent_pro)
        return super(device_logAdmin,self).formfield_for_manytomany(db_field,request,**kwargs)
    def has_add_permission(self, request):
        try:
            return request.user == Project.objects.get(id=request.user.recent_pro).starter
        except Exception as e:
            return False



    def get_changeform_initial_data(self, request):
        ds = Device_changelog.objects.filter(project_info = Project.objects.get(id=request.user.recent_pro))
        "slow"
        return {'thisid': len(ds)+1}
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        show_return = False
        obj = Device_changelog.objects.get(id=object_id)
        if obj.workflow_node == 0:
            show_return = False
        elif sub_can_return(obj, request.user):
            show_return = True
        self.readonly_fields = ['agreed', 'workflow_node', 'total_price'];
        self.exclude = ['project_info']
        show_delete = False
        if object_id == None:
            show_submit_button = True
            show_save_and_continue = True
        else:
            curuser = get_edible_user(Device_changelog.objects.get(id=object_id))
            if curuser == request.user:
                show_submit_button = True
                show_save_and_continue = True
                show_delete = True
            else:

                show_submit_button = False
                show_save_and_continue = False
        extra_context = extra_context or {}

        ctx = dict(
            show_return = show_return,
            show_save=show_submit_button,
            show_save_and_continue=show_save_and_continue,
            show_save_and_add_another = False,
            show_back = True,
            instance_id = request.user.recent_pro,
            show_workflow_line = True,
            show_delete = show_delete
        )
        extra_context.update(ctx)
        return super(device_logAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        ctx = dict(

            action_form=False,
        )

        extra_context.update(ctx)
        return super(device_logAdmin, self).changelist_view(request, extra_context)
    def get_queryset(self, request):
        pros = ContentType.objects.get(app_label='basedata', model='project')
        try:
            pro = pros.model_class().objects.get(id=request.user.recent_pro)
        except Exception as e:
            print("未找到")
            return super(device_logAdmin, self).get_queryset(request)
        qs = super(device_logAdmin, self).get_queryset(request)
        return qs.filter(project_info=pro)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.save_change()
        formset.save()
        self.message_user(request, "成功")

    def save_model(self, request, obj, form, change):
        obj.project_info =Project.objects.get(id=request.user.recent_pro)

        "add the device"
        obj.save()

        for d in form.cleaned_data['device']:
            Device_change.objects.create(change_log = obj, name = d.name, brand = d.brand, type = d.type, specification = d.specification, unit = d.unit,
                                        sale_price=d.sale_price, buy_price = d.buy_price)

        form.cleaned_data['device'] = [];
        obj.save()

        if "_confirm" in request.POST:
            to_next(obj,1,request.user,"提交了设备变更表格",3)
            self.message_user(request, "提交成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])
            if obj.WORK_FLOW_NODE[obj.workflow_node][1] == '完成':
                total_change = 0
                total_buychange = 0
                dcs = Device_change.objects.filter(change_log = obj)
                dss = Device.objects.filter(device_form = Device_form.objects.get(project_info = obj.project_info))
                for dc in dcs:
                    d = dss.filter(name = dc.name, brand = dc.brand, type = dc.type)
                    if len(d) ==1:
                        d[0].num = d[0].num + dc.num
                        d[0].total_price = d[0].total_price + dc.total_price
                        d[0].save()
                        if d[0].num ==0:
                            d[0].delete()

                        self.message_user(request,str(dc.name)+ '已在设备表中修改')
                        print(str(dc.thisid)+'已在设备表中修改')

                        total_change += dc.total_price
                        total_buychange += dc.total_buy_price
                    else:
                        self.message_user(request, str(dc.name)+'已在设备表中添加')

                        print(str(dc.thisid)+'已在设备表中添加')
                        Device.objects.create(name=dc.name, brand=dc.brand, type=dc.type, specification=dc.specification,num=dc.num,unit=dc.unit,
                                              sale_price=dc.sale_price,total_price=dc.total_price,buy_price=dc.buy_price,total_buy_price=dc.total_buy_price,
                                              device_form = Device_form.objects.get(project_info = obj.project_info))
                        total_change += dc.total_price
                        total_buychange += dc.total_buy_price

                make_number(dss)
                df = Device_form.objects.get(project_info = obj.project_info)
                df.total_price += total_change
                df.total_buyprice += total_buychange
                df.save()
                obj.project_info.total_price = df.total_price
                obj.project_info.save()
    def delete_model(self, request, obj):

        to_next(obj, 2, request.user, "反对了设备更改表格", 3, False)
        self.message_user(request, "反对成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])


    def response_change(self, request, obj):

        total = 0
        cs = Device_change.objects.filter(change_log=obj)
        for c in cs:
            if c.num is not None and c.sale_price is not None:
                total += c.num * c.sale_price
                c.total_price = c.num * c.sale_price
                c.total_buy_price = c.num * c.buy_price
                c.save()

                ds = Device.objects.filter(name=c.name, brand=c.brand, type=c.type)
                if len(ds) == 0:
                    self.message_user(request, c.name + '在原项目清单不存在，添加')
                    c.memo = "新的添加"
                    if c.num < 1:
                        self.message_user(request, c.name + '数量为负数，无法添加', messages.ERROR)
                else:
                    self.message_user(request, c.name +  '已在原项目中找到')
                    if c.num < 1:
                        c.memo = "原设备"+str(c.num)+"  现设备数量为"+str(ds[1].num+c.num)
                    else:
                        c.memo = "原设备+" + str(c.num) + "  现设备数量为" + str(ds[1].num + c.num)

        obj.total_price = total
        obj.save()
        make_number(cs)

        return HttpResponseRedirect(request.path)

    def response_add(self, request, obj):
        total = 0
        cs = Device_change.objects.filter(change_log=obj)
        for c in cs:
            if c.num is not None and c.sale_price is not None:
                total += c.num * c.sale_price
                c.total_price = c.num * c.sale_price
                c.save()

                ds = Device.objects.filter(name=c.name, brand=c.brand, type=c.type)
                if len(ds) == 0:
                    self.message_user(request, c.name + '在原项目清单不存在，添加')
                    c.memo = "新的添加"
                    if c.num < 1:
                        self.message_user(request, c.name + '数量为负数，无法添加', messages.ERROR)
                else:
                    self.message_user(request, c.name +  '已在原项目中找到')
                    if c.num < 1:
                        c.memo = "原设备"+str(c.num)+"  现设备数量为"+str(ds[1].num+c.num)
                    else:
                        c.memo = "原设备+" + str(c.num) + "  现设备数量为" + str(ds[1].num + c.num)

        obj.total_price = total
        obj.save()
        make_number(cs)

        return HttpResponseRedirect('/admin/basedata/device_changelog/'+str(obj.id)+'/change/')

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')

admin_site.register(Device_changelog, device_logAdmin)




class MaterialInfoInline(admin.TabularInline): # TabularInline

    formfield_overrides = {
        models.CharField:{'widget':widgets.TextInput(attrs={'size': 12})},
        models.IntegerField: {'widget': widgets.TextInput(attrs={'size': 2})},
        models.DecimalField: {'widget': widgets.TextInput(attrs={'size': 5})},
        models.TextField: {'widget': widgets.Textarea(attrs={'cols': '20', 'rows': '2'})},

    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'unit':
            kwargs['widget'] = widgets.TextInput(attrs={'size': 2})

        return super(MaterialInfoInline,self).formfield_for_dbfield(db_field, request, **kwargs)

    def get_exclude(self, request, obj=None):
        if request.user == Project.objects.get(id = request.user.recent_pro).manager:
            self.fields = ['material_name','brand','xinhao','guige','num','unit','price','total_price']
            self.readonly_fields = ['total_price','price']
        elif request.user.title == 6:
            self.fields = ['material_name','brand','xinhao','guige','num','unit','price','total_price']
            self.readonly_fields = ['material_name','brand','guige','xinhao','num','unit','total_price']
        else:

            self.fields = ['material_name','brand','xinhao','guige','num','unit','price','total_price']
            self.readonly_fields = self.fields


    def has_delete_permission(self, request, obj=None):
        return request.user == Project.objects.get(id = request.user.recent_pro).manager
    def has_add_permission(self, request):
        return request.user == Project.objects.get(id = request.user.recent_pro).manager
    model = Material_use
    extra = 0
class Material_logAdmin(admin.ModelAdmin):
    inlines = [MaterialInfoInline]


    def get_queryset(self, request):
        pros = ContentType.objects.get(app_label='basedata', model='project')
        try:
            pro = pros.model_class().objects.get(id=request.user.recent_pro)
        except Exception as e:
            return super(Material_logAdmin, self).get_queryset(request)
        qs = super(Material_logAdmin, self).get_queryset(request)
        return qs.filter(project_info=pro)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        show_return = False
        obj = Material_log.objects.get(id=object_id)
        if obj.workflow_node == 0:
            show_return = False
        elif sub_can_return(obj,request.user):
            show_return = True
        self.readonly_fields = ['total','workflow_node','agreed']
        self.exclude=['project_info']

        show_submit_button = False
        show_save_and_continue = False
        if object_id == None: #adding
            if request.user == Project.objects.get(id = request.user.recent_pro).manager:
                show_submit_button = True
                show_save_and_continue = True
        else:
            curuser = get_edible_user(obj)
            if curuser == request.user:
                show_submit_button = True
                show_save_and_continue = True
        extra_context = extra_context or {}

        ctx = dict(
            show_return = show_return,
            show_save=show_submit_button,
            show_save_and_continue=show_save_and_continue,
            show_save_and_add_another = False,
            show_delete_link = show_save_and_continue,
            show_back = True,
            instance_id = request.user.recent_pro,

            show_workflow_line=True

        )
        extra_context.update(ctx)
        return super(Material_logAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):

        if "_return" in request.POST:
            TodoList.objects.filter(project=obj.project_info, content_type=4).delete()
            obj.go_back()
            return
        obj.project_info = Project.objects.get(id = request.user.recent_pro)
        items = Material_use.objects.filter(material_log=obj)
        total = 0
        for item in items:
            if item.num is not None and  item.price is not None:
                total += item.num * item.price
        obj.total = total
        obj.save()

        if "_confirm" in request.POST:
            to_next(obj,1,request.user,"提交了材料领用表格",4)
            self.message_user(request, "提交成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def delete_model(self, request, obj):
        to_next(obj, 2, request.user, "反对了材料领用表格", 4,False)
        self.message_user(request, "反对成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def response_change(self, request, obj):
        ms = Material_use.objects.filter(material_log=obj)
        total = 0
        for m in ms:
            m.save_change()
            total += m.total_price
        obj.total = total
        obj.save()
        obj.project_info.total_mat = total
        obj.project_info.updateMoney()

        return HttpResponseRedirect(request.path)

    def response_add(self, request, obj):
        ms = Material_use.objects.filter(material_log=obj)
        total = 0
        for m in ms:
            m.save_change()
            total += m.total_price
        obj.total = total
        obj.save()
        obj.project_info.total_mat = total
        obj.project_info.updateMoney()

        return HttpResponseRedirect(request.path)

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')


admin_site.register(Material_log,Material_logAdmin)


class DeviceFinalInfoInline(admin.TabularInline): # TabularInline

    model = Device_final
    extra = 0

    formfield_overrides = {
        models.CharField:{'widget':widgets.TextInput(attrs={'size': 12})},
        models.IntegerField: {'widget': widgets.TextInput(attrs={'size': 2})},
        models.DecimalField: {'widget': widgets.TextInput(attrs={'size': 5})},
        models.TextField: {'widget': widgets.Textarea(attrs={'cols': '20', 'rows': '2'})},

    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'unit':
            kwargs['widget'] = widgets.TextInput(attrs={'size': 2})
        if db_field.name == 'insurance':
            kwargs['widget'] = widgets.TextInput(attrs={'size': 5})

        return  super(DeviceFinalInfoInline,self).formfield_for_dbfield(db_field, request, **kwargs)
    def get_exclude(self, request, obj=None):
        id = request.user.recent_pro
        if id != 0:
            if request.user == Project.objects.get(id=request.user.recent_pro).manager:
                self.fields = [ 'name', 'brand', 'type', 'specification','producer','produce_num','produce_time','place_keep','bill_num','price',
                               'time_install','record','note']
                #self.readonly_fields = ['name', 'brand', 'specification', 'price']
            else:

                self.fields = ['name', 'brand', 'type', 'specification','producer','produce_num','produce_time','place_keep','bill_num','price',
                               'time_install','record','note']
                self.readonly_fields = self.fields
        return ['project_info']

    def has_delete_permission(self, request, obj=None):
        return request.user == Project.objects.get(id = request.user.recent_pro).manager
    def has_add_permission(self, request):
        return request.user == Project.objects.get(id = request.user.recent_pro).manager



def date(dates):  # 定义转化日期戳的函数,dates为日期戳
    import datetime
    if dates is None or dates is '':
        return None
    delta = datetime.timedelta(days=int(dates))
    today = datetime.datetime.strptime('1899-12-30',
                                       '%Y-%m-%d') + delta  # 将1899-12-30转化为可以计算的时间格式并加上要转化的日期戳
    return datetime.datetime.strftime(today, '%Y-%m-%d')
def read(value):
    if value is '':
        return None
    else:
        return value

class DeviceFinalFormAdmin(admin.ModelAdmin):
    inlines = [DeviceFinalInfoInline]

    filter_horizontal = ('device',)



    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "device":
            kwargs['queryset']=Device.objects.filter(device_form__project_info_id = request.user.recent_pro)
        return super(DeviceFinalFormAdmin,self).formfield_for_manytomany(db_field,request,**kwargs)
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        show_return = False
        obj = Device_finalform.objects.get(id=object_id)
        if obj.workflow_node == 0:
            show_return = False
        elif sub_can_return(obj, request.user):
            show_return = True
        self.readonly_fields = ['workflow_node','agreed']
        self.exclude = ['project_info','device']
        if request.user == Project.objects.get(id=request.user.recent_pro).manager:
            self.exclude = ['project_info']


        show_submit_button = False
        show_save_and_continue = False
        if object_id == None: #adding
            if request.user == Project.objects.get(id = request.user.recent_pro).manager:
                show_submit_button = True
                show_save_and_continue = True
            else:

                self.exclude = ['project_info', 'file']
        else:

            curuser = get_edible_user(Device_finalform.objects.get(id=object_id))
            if curuser == request.user:
                show_submit_button = True
                show_save_and_continue = True
        extra_context = extra_context or {}

        ctx = dict(
            show_return = show_return,
            show_save=show_submit_button,
            show_save_and_continue=show_save_and_continue,
            show_save_and_add_another = False,
            show_delete_link = show_save_and_continue,
            show_back = True,
            instance_id = request.user.recent_pro,

            show_workflow_line=True
        )
        extra_context.update(ctx)
        return super(DeviceFinalFormAdmin, self).changeform_view(request, object_id, form_url, extra_context)
    def get_readonly_fields(self, request, obj=None):
        return ['project_info','agreed','workflow_node']

    def save_model(self, request, obj, form, change):

        "add the device"
        if request.user == obj.project_info.manager:
            for d in form.cleaned_data['device']:
                for i in range(0, d.num):
                    Device_final.objects.create(form = obj, name = d.name, brand = d.brand, type = d.type, specification = d.specification,
                                        price=d.sale_price)

            form.cleaned_data['device'] = [];
            obj.save()
        import os

        if "_confirm" in request.POST:
            to_next(obj, 1, request.user, "提交了设备信息表格", 8)
            self.message_user(request, "提交成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

        elif obj.file != None and obj.file.name !='':
            workbook = xlrd.open_workbook(os.path.join(BASE_DIR, obj.file.name).replace('\\','/'))
            table = workbook.sheets()[0]
            if table.row_values(0)[0] =='设备信息表':
                try:
                    for i in range(2,table.nrows):
                        if table.row_values(i)[1] is not '' and table.row_values(i)[2] is not '':

                            Device_final.objects.create(form=obj,
                                                               thisid=read(table.row_values(i)[0]),
                                                               name=read(table.row_values(i)[1]),
                                                               brand=read(table.row_values(i)[2]),
                                                               type=read(table.row_values(i)[3]),
                                                               specification=read(table.row_values(i)[4]),
                                                               producer=read(table.row_values(i)[5]),
                                                               produce_num=read(table.row_values(i)[6]),
                                                               produce_time=date(table.row_values(i)[7]),
                                                               place_keep=read(table.row_values(i)[8]),
                                                               bill_num=read(table.row_values(i)[9]),
                                                               price=read(table.row_values(i)[10]),
                                                               time_install=date(table.row_values(i)[11]),
                                                               record=read(table.row_values(i)[12]),
                                                               note=read(table.row_values(i)[13])
                                                               )
                        else:
                            break


                except Exception as e:
                    self.message_user(request, "失败"+e.__str__())
                    import traceback
                    print(traceback.print_exc())


            try:
                os.remove(os.path.join(BASE_DIR, obj.file.name))
                obj.file = None
                obj.save()
            except Exception as e:
                pass


    def delete_model(self, request, obj):
        to_next(obj, 2, request.user, "反对了设备信息表格", 8, False)
        self.message_user(request, "反对成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def response_change(self, request, obj):

        dfs = Device_final.objects.filter(name = '', form = obj)
        for ds in dfs:
            ods = Device.objects.filter(thisid = ds.originID, device_form= Device_form.objects.get(project_info=obj.project_info))
            if len(ods) == 0:
                self.message_user(request,str(ds.originID)+'不存在')
            else:
                for i in range(0,ods[0].num):
                    Device_final.objects.create(name = ods[0].name,type = ods[0].type, brand=ods[0].brand, specification=ods[0].specification,form = obj,price=ods[0].sale_price)
        dfs.delete()

        return HttpResponseRedirect(request.path)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect('/admin/basedata/project/' + str(obj.project_info.id) + '/change')

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')


admin_site.register(Device_finalform,DeviceFinalFormAdmin)

class Device_finalAdmin(admin.ModelAdmin):
    list_display = ['thisid','name', 'brand', 'type', 'specification', 'producer','produce_num','produce_time','place_keep','bill_num', 'price']
    def get_readonly_fields(self, request, obj=None):
        return ['agreed','workflow_node']


    def get_queryset(self, request):
        pros = ContentType.objects.get(app_label='basedata', model='project')
        try:
            pro = pros.model_class().objects.get(id=request.user.recent_pro)
        except Exception as e:
            return super(Device_finalAdmin, self).get_queryset(request)
        qs = super(Device_finalAdmin, self).get_queryset(request)
        return qs.filter(work_report=work_report.objects.get(project_info_id = request.user.recent_pro))

    def changelist_view(self, request, extra_context=None):
        id = request.user.recent_pro
        pros = ContentType.objects.get(app_label='basedata', model='project')

        if id ==0:
            self.message_user(request, "请重新获取项目id")
            return


        pro = pros.model_class().objects.get(id=id)
        if request.user == pro.manager:
            self.list_editable = ['name', 'brand', 'type', 'specification', 'producer','produce_num','produce_time','place_keep','bill_num', 'price']
            can_submit = True
        else:
            whs = mymodels.Device_final.objects.filter(work_report=work_report.objects.get(project_info_id = request.user.recent_pro))
            wh = whs[0]
            if wh.WORK_FLOW_NODE[wh.workflow_node][1] == '完成':
                over = True
            else:
                if wh.WORK_FLOW_NODE[wh.workflow_node][1]!='等待':
                    next = user_models.Employee.objects.get(title=ROLES.index(wh.WORK_FLOW_NODE[wh.workflow_node][1]))
                    if request.user == next:
                        can_submit = True
        ctx = dict(
            can_submit=can_submit,
            type=3,
            instance_id=id
        )

        extra_context.update(ctx)
        return super(Device_finalAdmin, self).changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):

        show_submit_button = True
        extra_context = extra_context or {}

        ctx = dict(
            show_submit_button=show_submit_button,
            show_save_and_continue = False,
        )

        extra_context.update(ctx)
        return super(Device_finalAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        pro = obj.project_info
        if request.user == pro.manager:
            self.message_user(request, "成功")
            obj.save()
        else:
            str = "您无权对该项目  " + pro.name + " 的最终设备文件修改，失败"
            self.message_user(request, str)

    def delete_model(self, request, obj):
        pro = obj.project_info
        if request.user == pro.starter:
            self.message_user(request, "删除成功")
            obj.delete()
        else:
            str = "您无权对该项目  " + pro.name + " 的最终设备文件修改，失败"
            self.message_user(request, str)

    def response_change(self, request, obj):
        if "_addanother" in request.POST:
            return HttpResponseRedirect('/admin/basedata/device_change/add/')
        return HttpResponseRedirect('/admin/basedata/project/' + str(obj.project_info.id) + '/change')

    def response_add(self, request, obj):
        if "_addanother" in request.POST:
            return HttpResponseRedirect('/admin/basedata/device_change/add/')
        return HttpResponseRedirect('/admin/basedata/project/' + str(obj.project_info.id) + '/change')

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')


admin_site.register(Device_final,Device_finalAdmin)


class work_hourinline(admin.TabularInline): # TabularInline
    model = work_hour
    extra = 0

    formfield_overrides = {
        models.CharField:{'widget':widgets.TextInput(attrs={'size': 13})},
        models.IntegerField: {'widget': widgets.TextInput(attrs={'size': 3})},
        models.DecimalField: {'widget': widgets.TextInput(attrs={'size': 5})}
    }

    def has_delete_permission(self, request, obj=None):
        return request.user == Project.objects.get(id = request.user.recent_pro).manager
    def has_add_permission(self, request):
        return request.user == Project.objects.get(id = request.user.recent_pro).manager

    def get_exclude(self, request, obj=None):
        self.fields = ['employee', 'start_time', 'finish_time', 'time', 'work_content', 'inside_work_hour',
                       'inside_price', 'extra_work_hour'
            , 'extra_price', 'total_price']
        if request.user== Project.objects.get(id = request.user.recent_pro).manager:
            self.readonly_fields = ['extra_price','inside_price','total_price']
        elif request.user.title == 4 or request.user.title == 9 or request.user.title == 8:

            self.readonly_fields = ['employee','start_time','finish_time','time','work_content','inside_price'
                ,'extra_price','total_price']
        else:
            self.readonly_fields = ['employee','start_time','finish_time','time','work_content','inside_work_hour','inside_price','extra_work_hour'
                ,'extra_price','total_price']


class work_recordAdmin(admin.ModelAdmin):
    inlines = [work_hourinline]

    def get_queryset(self, request):
        pros = ContentType.objects.get(app_label='basedata', model='project')
        try:
            pro = pros.model_class().objects.get(id=request.user.recent_pro)
        except Exception as e:
            return super(work_recordAdmin, self).get_queryset(request)
        qs = super(work_recordAdmin, self).get_queryset(request)
        return qs.filter(project_info=pro)
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        show_return = False
        obj = work_report.objects.get(id=object_id)
        if obj.workflow_node == 0:
            show_return = False
        elif sub_can_return(obj, request.user):
            show_return = True
        show_submit_button = False
        show_save_and_continue = False
        if object_id == None: #adding
            if request.user == Project.objects.get(id = request.user.recent_pro).manager:
                show_submit_button = True
                show_save_and_continue = True
        else:
            curuser = get_edible_user(work_report.objects.get(id=object_id))
            if curuser == request.user:
                show_submit_button = True
                show_save_and_continue = True
        self.readonly_fields= ['agreed','workflow_node','note']
        self.exclude = ['project_info']
        extra_context = extra_context or {}

        ctx = dict(
            show_return = show_return,
            show_save=show_submit_button,
            show_save_and_continue=show_save_and_continue,
            show_save_and_add_another = False,
            show_delete_link = show_save_and_continue,
            show_back = True,
            instance_id = request.user.recent_pro,
            show_workflow_line = True
        )
        extra_context.update(ctx)
        return super(work_recordAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        ctx = dict(
            show_all=True,

            action_form=False,
            href = '/admin/basedata/work_hour/'
        )

        extra_context.update(ctx)
        return super(work_recordAdmin, self).changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):

        obj.project_info = Project.objects.get(id = request.user.recent_pro)
        obj.save()

        if "_confirm" in request.POST:
            to_next(obj, 1, request.user, "提交了工时表格", 5)
            self.message_user(request, "提交成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def delete_model(self, request, obj):
        to_next(obj, 2, request.user, "反对了工时表格", 5, False)
        self.message_user(request, "反对成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])


    def response_change(self, request, obj):
        total = 0
        dict = {}
        for wh in work_hour.objects.filter(work_report = obj):
            if wh.employee.username not in dict:
                dict[wh.employee.username] = [0,0,0]

            wh.save_change()
            dict[wh.employee.username][0] += wh.inside_work_hour
            dict[wh.employee.username][1] += wh.extra_work_hour
            dict[wh.employee.username][2] += wh.total_price
            total+=wh.extra_work_hour+wh.inside_work_hour
        obj.project_info.total_hour = total
        obj.project_info.hour_cost = total*220
        obj.project_info.updateMoney()
        obj.project_info.save()
        note = '合计 \n'

        for k in dict.keys():
            note += k+" \t 上班工时: "+str(dict[k][0])+"个 \t    加班工时: "+str(dict[k][1])+"个     \t    总绩效工资:"+str(dict[k][2])+ '元'+'\n'
        obj.note = note
        obj.save()

        return HttpResponseRedirect(request.path)

    def response_add(self, request, obj):
        total = 0
        dict = {}
        for wh in work_hour.objects.filter(work_report=obj):
            if wh.employee.username not in dict:
                dict[wh.employee.username] = [0,0,0]

            wh.save_change()
            dict[wh.employee.username][0] += wh.inside_work_hour
            dict[wh.employee.username][1] += wh.extra_work_hour
            dict[wh.employee.username][2] += wh.total_price
            total += wh.extra_work_hour + wh.inside_work_hour
        obj.project_info.total_hour = total
        obj.project_info.hour_cost = total * 220
        obj.project_info.total_money = obj.project_info.total_mat + obj.project_info.total_out + obj.project_info.hour_cost

        obj.project_info.save()

        note = '合计 \n'

        for k in dict.keys():
            note += k+" \t 上班工时: "+str(dict[k][0])+"个 \t    加班工时: "+str(dict[k][1])+"个     \t    总绩效工资:"+str(dict[k][2])+ '元'+'\n'
        obj.note = note
        obj.save()

        return HttpResponseRedirect(request.path)

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')



admin_site.register(work_report,work_recordAdmin)

class work_hourAdmin(admin.ModelAdmin):
    list_display = ['work_report','employee', 'work_content','start_time','finish_time', 'inside_work_hour', 'extra_work_hour','total_price']
    list_filter = ['employee', 'start_time']
    ordering = ['thisid']
    def get_readonly_fields(self, request, obj=None):
        return ['agreed','workflow_node']

    def get_queryset(self, request):

        return super(work_hourAdmin,self).get_queryset(request).filter(work_report__project_info=request.user.recent_pro)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        ctx = dict(
            action_form=False,
        )

        extra_context.update(ctx)
        return super(work_hourAdmin, self).changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):

        show_submit_button = True
        extra_context = extra_context or {}

        ctx = dict(
            show_submit_button=show_submit_button,

            action_form=False,
            show_save_and_add_another=False,
        )

        extra_context.update(ctx)
        return super(work_hourAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        '''pro = Project.objects.get(id= request.user.recent_pro)
        if request.user == pro.manager:
            whs = work_hour.objects.filter(project_info=pro)
            if len(whs) >0:
                self.message_user(request, "工作流还原")
                TodoList.objects.filter(project = pro, content_type = 5).delete()
                for wh in whs:
                    wh.workflow_node = 0
                    wh.save()
            self.message_user(request, "修改成功")
            obj.save()
        else:
            str = "您无权对该项目  " + pro.name + " 的工时更改文件修改，修改失败"
            self.message_user(request, str)'''
        obj.save()

    def delete_model(self, request, obj):
        pro = obj.project_info
        intodo = TodoList.objects.filter(user=request.user, project=pro)
        inHis = History.objects.filter(user=request.user, project=pro)
        if request.user == pro.starter:
            self.message_user(request, "删除成功")
            obj.delete()
        else:
            str = "您无权对该项目  " + pro.name + " 的工时文件修改，删除失败"
            self.message_user(request, str)

    def response_change(self, request, obj):
        if "_addanother" in request.POST:
            return HttpResponseRedirect('/admin/basedata/work_hour/add/')
        return HttpResponseRedirect('/admin/basedata/project/' + str(obj.project_info.id) + '/change')

    def response_add(self, request, obj):
        if "_addanother" in request.POST:
            return HttpResponseRedirect('/admin/basedata/work_hour/add/')
        return HttpResponseRedirect('/admin/basedata/project/' + str(obj.project_info.id) + '/change')


    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')


admin_site.register(work_hour,work_hourAdmin)

class Finish_reportAdmin(admin.ModelAdmin):
    list_display = ['project_info', 'time']
    ordering = ['id']


    def get_queryset(self, request):
        pros = ContentType.objects.get(app_label='basedata', model='project')
        try:
            pro = pros.model_class().objects.get(id=request.user.recent_pro)
        except Exception as e:
            return super(Finish_reportAdmin, self).get_queryset(request)
        qs = super(Finish_reportAdmin, self).get_queryset(request)
        return qs.filter(project_info=pro)

    def get_readonly_fields(self, request, obj=None):

        if request.user.title == 4:
            return ['details','agreed','workflow_node']
        return ['agreed','workflow_node']


    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        show_return = False
        obj = Finish_report.objects.get(id=object_id)
        if obj.workflow_node == 0:
            show_return = False
        elif sub_can_return(obj, request.user):
            show_return = True
        self.exclude = ['project_info']
        show_save_and_continue = False
        show_submit_button = False
        show_save = False
        show_delete_link = False
        extra_context = extra_context or {}
        obj = Finish_report.objects.get(id=object_id)
        curuser = get_edible_user(obj)
        if curuser == request.user:
            show_save = True
            show_delete_link = True
            show_save_and_continue = True
        ctx = dict(
            show_return=show_return,
            show_save_and_continue=show_save_and_continue,
            show_save_and_add_another=False,
            show_delete_link=show_delete_link,
            show_save=show_save,
            show_workflow_line = True,
            instance_id=request.user.recent_pro

        )

        extra_context.update(ctx)
        return super(Finish_reportAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):

        obj.save()
        if "_confirm" in request.POST:
            to_next(obj, 1, request.user, "提交了竣工报告表格", 6)
            self.message_user(request, "提交成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def delete_model(self, request, obj):
        to_next(obj, 2, request.user, "反对了竣工报告表格", 6, False)
        self.message_user(request, "反对成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def response_change(self, request, obj):

        return HttpResponseRedirect('/admin/basedata/project/'+str(obj.project_info.id)+'/change')

    def response_add(self, request, obj):
        return HttpResponseRedirect('/admin/')

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')


admin_site.register(Finish_report,Finish_reportAdmin)




class FFInfoInline(admin.TabularInline): # TabularInline

    formfield_overrides = {
        models.CharField:{'widget':widgets.TextInput(attrs={'size': 15})},
        models.IntegerField: {'widget': widgets.TextInput(attrs={'size': 3})},
        models.DecimalField: {'widget': widgets.TextInput(attrs={'size': 5})}
    }
    model = feedback_report
    extra = 0
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def get_readonly_fields(self, request, obj=None):
        self.fields = ['idnum','item','standard','points','eva','self_eva','note']
        if request.user == Project.objects.get(id=request.user.recent_pro).manager:
            return ['idnum','item','standard','points','eva','note']
        return ['idnum','item','standard','points','self_eva','note']

class feedback_formAdmin(admin.ModelAdmin):

    inlines = [FFInfoInline]

    def get_readonly_fields(self, request, obj=None):
        if request.user.title == 1:
            return ['workflow_node','agreed','project_info','total_point', 'total_self']
        return ['workflow_node','agreed','project_info','total_point','total_self','bonus']


    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        self.readonly_fields = ['workflow_node','agreed']
        self.exclude=['project_info']

        show_submit_button = False
        show_save_and_continue = False
        if object_id == None: #adding
            if request.user == Project.objects.get(id = request.user.recent_pro).manager:
                show_submit_button = True
                show_save_and_continue = True
        else:
            curuser = get_edible_user(feedback_form.objects.get(id=object_id))
            if curuser == request.user:
                show_submit_button = True
                show_save_and_continue = True
        extra_context = extra_context or {}

        ctx = dict(
            show_save=show_submit_button,
            show_save_and_continue=show_save_and_continue,
            show_save_and_add_another = False,
            show_delete_link = show_save_and_continue,
            show_back = True,
            instance_id=request.user.recent_pro,
            show_workflow_line = True
        )
        extra_context.update(ctx)
        return super(feedback_formAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):

        obj.save()
        if "_next" in request.POST:
            to_next(obj, 1, request.user, "提交了自评报告表格", 7)
            self.message_user(request, "提交成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def delete_model(self, request, obj):
        to_next(obj, 2, request.user, "反对了自评报告表格", 7, False)
        self.message_user(request, "反对成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def response_change(self, request, obj):
        total_self = 0
        total_eva = 0
        for i in feedback_report.objects.filter(feedback_form = obj):
            total_self += i.self_eva
            total_eva += i.eva
        obj.total_self = total_self
        obj.total_point =total_eva
        obj.save()
        return HttpResponseRedirect(request.path)

    def response_add(self, request, obj):

        total_self = 0
        total_eva = 0
        for i in feedback_report.objects.filter(feedback_form = obj):
            total_self += i.self_eva
            total_eva += i.eva
        obj.total_self = total_self
        obj.total_point =total_eva
        obj.save()
        return HttpResponseRedirect(request.path)

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')


admin_site.register(feedback_form,feedback_formAdmin)

class feedback_reportAdmin(admin.ModelAdmin):
    list_display = ['idnum', 'item', 'standard', 'points', 'self_eva', 'eva', 'note']
    ordering = ['idnum']


    def get_queryset(self, request):
        pros = ContentType.objects.get(app_label='basedata', model='project')
        try:
            pro = pros.model_class().objects.get(id=request.user.recent_pro)
        except Exception as e:
            return super(feedback_reportAdmin, self).get_queryset(request)
        qs = super(feedback_reportAdmin, self).get_queryset(request)
        return qs.filter(project_info=pro)
    def get_readonly_fields(self, request, obj=None):
        return ['agreed', 'workflow_node']
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        show_return = False
        obj = feedback_report.objects.get(id=object_id)
        if obj.workflow_node == 0:
            show_return = False
        elif sub_can_return(obj, request.user):
            show_return = True

        show_save_and_continue = False
        show_submit_button = True
        show_save = False
        show_delete_link = False
        extra_context = extra_context or {}
        obj = feedback_report.objects.get(id=object_id)
        if request.user == obj.project_info.manager:
            show_save = True
        if obj.WORK_FLOW_NODE[obj.workflow_node][1] == '完成':
            show_save_and_continue = False
        else:
            if obj.WORK_FLOW_NODE[obj.workflow_node][1] == '等待':
                if request.user == obj.project_info.manager:
                    show_save = True
                    show_delete_link = True
                    show_save_and_continue = True
            else:
                curuser = user_models.Employee.objects.get(title=ROLES.index(obj.WORK_FLOW_NODE[obj.workflow_node][1]))
                if curuser == request.user:
                    show_save_and_continue = True
        ctx = dict(
            show_return=show_return,
            show_save_and_continue = show_save_and_continue,
            show_save_and_add_another=False,
            show_delete_link=show_delete_link,
            show_save=show_save

        )

        extra_context.update(ctx)
        return super(feedback_reportAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        id = request.user.recent_pro
        if id != 0:
            if request.user == Project.objects.get(id=id).manager:
                self.list_editable = ['self_eva','note']
            elif request.user.title == 4 or request.user.title == 5:
                self.list_editable = ['eva','note']
        else:
            self.message_user(request, "项目ID不存在，请重新获取")
            return super(feedback_reportAdmin, self).changelist_view(request, extra_context)
        can_submit = False
        pros = ContentType.objects.get(app_label='basedata', model='project')
        pro = pros.model_class().objects.get(id=id)
        if request.user == pro.manager:
            can_submit = True
        else:
            whs = mymodels.feedback_report.objects.filter(feedback_form=feedback_form.objects.get(project_info = pro))
            wh = whs[0]
            if wh.WORK_FLOW_NODE[wh.workflow_node][1] == '完成':
                over = True
            else:
                if wh.WORK_FLOW_NODE[wh.workflow_node][1] != '等待':
                    next = user_models.Employee.objects.get(title=ROLES.index(wh.WORK_FLOW_NODE[wh.workflow_node][1]))
                    if request.user == next:
                        can_submit = True
        extra_context = extra_context or {}
        ctx = dict(
            can_submit=can_submit,
            type=6,
            instance_id=id
        )

        extra_context.update(ctx)
        return super(feedback_reportAdmin, self).changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        obj.save()
        pro = Project.objects.get(id =id)

        if "_confirm" in request.POST:
            to_next(obj, 1, request.user, "提交了材料领用表格", 4)
            self.message_user(request, "提交成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])

    def delete_model(self, request, obj):
        to_next(obj, 2, request.user, "反对了材料领用表格", 4, False)
        self.message_user(request, "反对成功，进入下一工作流 " + obj.WORK_FLOW_NODE[obj.workflow_node][1])


    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        ctx = dict(
            show_save_and_add_another=False,

        )
        extra_context['show_save_and_add_another'] = False

        extra_context.update(ctx)
        return super(feedback_reportAdmin, self).change_view(request, object_id, form_url, extra_context)
    def response_change(self, request, obj):

        return HttpResponseRedirect(request.path)

    def response_add(self, request, obj):
        return HttpResponseRedirect('/admin/')

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect('/admin/')



admin_site.register(feedback_report,feedback_reportAdmin)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['project', 'href', 'memo', 'pro_type', 'pro_time']
    list_filter = ['pro_type','project']
    def get_queryset(self, request):
        qs = super(HistoryAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)


    def has_add_permission(self, request):
        return False


admin_site.register(History, HistoryAdmin)


class TodoListAdmin(admin.ModelAdmin):

    list_display = ['code', 'project','content_type', 'href', 'is_read', 'status', 'arrived_time','memo']
    def get_queryset(self, request):
        qs = super(TodoListAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)
    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        ctx = dict(
            action_form=False,
        )

        extra_context.update(ctx)
        return super(TodoListAdmin, self).changelist_view(request, extra_context)


admin_site.register(TodoList, TodoListAdmin)




