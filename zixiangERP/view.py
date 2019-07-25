from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.contrib.contenttypes.models import ContentType
from basedata import admin
from basedata import models
from users import models as user_models

from _io import StringIO

ProjID = 0




def home(request):
    return HttpResponseRedirect("/admin/")

def deviceInfo(request,project_id):

    if project_id is not None:
        pro = models.Project.objects.get(id = str(project_id))
        request.user.recent_pro = project_id
        request.user.save()
    else:
        pro = models.Project.objects.get(id = request.user.recent_pro)

    frs = ContentType.objects.get(app_label='basedata', model='Device_form')
    fr = frs.model_class().objects.get(project_info=pro)
    return HttpResponseRedirect('/admin/basedata/device_form/' + str(fr.id) + '/change')

def deviceChange(request,project_id):
    request.user.recent_pro = project_id
    request.user.save()
    return HttpResponseRedirect("/admin/basedata/device_changelog")

def deviceFinal(request,project_id):

    if project_id is not None:
        request.user.recent_pro = project_id
        request.user.save()
        pro = models.Project.objects.get(id = str(project_id))
    else:
        pro = models.Project.objects.get(id = request.user.recent_pro)

    frs = ContentType.objects.get(app_label='basedata', model='Device_finalform')
    fr = frs.model_class().objects.get(project_info=pro)
    return HttpResponseRedirect('/admin/basedata/device_finalform/'+str(fr.id)+'/change')
def stock(request,project_id):


    if project_id is not None:
        pro = models.Project.objects.get(id = str(project_id))
        request.user.recent_pro = project_id
        request.user.save()
    else:
        pro = models.Project.objects.get(id = request.user.recent_pro)

    frs = ContentType.objects.get(app_label='basedata', model='Material_log')
    fr = frs.model_class().objects.get(project_info=pro)
    return HttpResponseRedirect('/admin/basedata/material_log/'+str(fr.id)+'/change')

def workH(request,project_id):
    return HttpResponseRedirect("/admin/basedata/work_report")

def outItem(request,outSource_id):
    return HttpResponseRedirect("/admin/basedata/outsource_items")

def finalReport(request,project_id):
    if project_id is not None:
        pro = models.Project.objects.get(id = str(project_id))
        request.user.recent_pro = project_id
        request.user.save()
    else:
        pro = models.Project.objects.get(id = request.user.recent_pro)
    frs = ContentType.objects.get(app_label='basedata', model='Finish_report')
    fr = frs.model_class().objects.get(project_info=pro)
    return HttpResponseRedirect('/admin/basedata/finish_report/'+str(fr.id)+'/change')


def Evalu(request,project_id):

    if project_id is not None:
        pro = models.Project.objects.get(id = str(project_id))
        request.user.recent_pro = project_id
        request.user.save()
    else:
        pro = models.Project.objects.get(id = request.user.recent_pro)
    frs = ContentType.objects.get(app_label='basedata', model='feedback_form')
    fr = frs.model_class().objects.get(project_info=pro)
    return HttpResponseRedirect('/admin/basedata/feedback_form/'+str(fr.id)+'/change')

def outSource(request,project_id):

    if project_id is not None:
        pro = models.Project.objects.get(id = str(project_id))
        request.user.recent_pro = project_id
        request.user.save()
    else:
        pro = models.Project.objects.get(id = request.user.recent_pro)

    frs = ContentType.objects.get(app_label='basedata', model='outsource')
    fr = frs.model_class().objects.get(project_info=pro)
    return HttpResponseRedirect('/admin/basedata/outsource/'+str(fr.id)+'/change')
import xlsxwriter
from io import BytesIO

def export(request,obj_id):
    out = BytesIO()
    ds = models.Device.objects.filter(device_form= models.Device_form.objects.get(id = obj_id))
    wb = xlsxwriter.Workbook(out,{'in_memory': True})
    ws = wb.add_worksheet('设备清单')


    ws.write(0,0,'设备信息')
    ws.write(1,0,'序号')
    ws.write(1,1,'设备名称')
    ws.write(1,2,'品牌')
    ws.write(1,3,'型号')
    ws.write(1,4,'规格')
    ws.write(1,5,'数量')
    ws.write(1,6,'单位')
    ws.write(1,7,'单价')
    ws.write(1,8,'金额')
    ws.write(1,9,'保修')
    row = 1
    for d in ds:
        row += 1
        ws.write(row, 0, d.thisid)
        ws.write(row, 1, d.name)
        ws.write(row, 2, d.brand)
        ws.write(row, 3, d.type)
        ws.write(row, 4, d.specification)
        ws.write(row, 5, d.num)
        ws.write(row, 6, d.unit)
        ws.write(row, 7, d.sale_price)
        ws.write(row, 8, d.total_price)
        ws.write(row, 9, d.insurance)

    wb.close()
    out.seek(0)
    response = HttpResponse(
        out,
        content_type='application/octet-stream'
    )
    response['Content-Disposition'] = 'attachment;filename="设备清单导出.xlsx"'
    return response

    return response
def next(request,type,project_id):
    RANK = {'普通员工': 0, '总经理': 1, '商务经理': 2, '财务经理': 3, '工程经理': 4, '技术经理': 5, '库管': 6, '营销经理': 7, '行政经理':8}
    dict ={ 1:'Device_change',2: 'Material_use', 3:'Device_final', 4:'Finish_report', 5:'work_hour', 6:'feedback_report'}
    try:
        pros = ContentType.objects.get(app_label='basedata', model='project')
        pro = pros.model_class().objects.get(id=project_id)
        subjects = ContentType.objects.get(app_label='basedata', model=dict[type])
        subject = subjects.model_class().objects.filter(project_info = pro)
        for sub in subject:
            sub.to_next()
        if len(subject)>0:

            if subject[0].MYROLES[subject[0].workflow_node][1]=='完成':
                if type == 1:
                    for sub in subject:
                        dss = ContentType.objects.get(app_label='basedata', model='device')
                        ds = dss.model_class().objects.filter(name=sub.name, brand=sub.brand, type=sub.type,
                                                              project_info=sub.project_info)
                        if len(ds) == 0:
                            print('adding')
                            if sub.name != '----':
                                dss.model_class().objects.create(name=sub.name, brand=sub.brand, type=sub.type,
                                                             project_info=sub.project_info,
                                                             specification=sub.specification, num=sub.num,
                                                             unit=sub.unit, sale_price=sub.sale_price)
                        else:
                            print('changing')
                            d = ds[0]
                            ornum = d.num
                            d.num +=ornum
                            dss.model_class().objects.filter(num=0).delete()

                        total = 0
                        #change the total price in the project due to the change of the devices
                        for di in ds:
                            total += di.sale_price
                        pro.total_price = total
                        d.save()
                memo = "提交了 " + subject[0]._meta.verbose_name.title() + " 分项目完成"
                models.History.objects.create(project=pro, user=request.user, pro_type=5, memo=memo)
                models.TodoList.objects.get(project=pro, user=request.user, content_type=type).delete()

                return HttpResponseRedirect('/admin/basedata/history/')

            nextUser = user_models.Employee.objects.get(title=RANK[subject[0].MYROLES[subject[0].workflow_node][1]])
            models.TodoList.objects.create(project=pro, user=nextUser, content_type=type)
            memo = "提交了 " + subject[0]._meta.verbose_name.title() + "下一节点是 " + subject[0].MYROLES[subject[0].workflow_node][1]
            models.History.objects.create(project=pro, user=request.user, pro_type=5, memo=memo)
            if request.user != pro.manager:
                models.TodoList.objects.get(project=pro, user=request.user, content_type=type).delete()
        else:
            print("没有数据")

        return HttpResponseRedirect('/admin/basedata/history/')
    except Exception as e:
        print(e)



