# _*_ coding:utf-8 _*_
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from common import const
from common import generic
from users import models as user_models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
# Create your models here.


PROCESS_TYPE = (
    (0, u"提交"),
    (1, u"同意"),
    (2, u"反对"),
    (3, u"终止"))

CHANGE_TYPE = (
    (0, u"新增"),
    (1, u"增加原有设备"),
    (2, u"删减原有设备"))

BRAND_CHOICE = (("Epson",u"爱普生"),("Lenovo",u"联想"))

UNIT_CHOICE = ((u"个",u"个"),(u"只",u"只"))
tool = {'普通员工': 0, '总经理': 1, '商务经理': 2, '财务经理': 3, '工程经理': 4, '技术经理': 5, '库管': 6, '营销经理': 7, '行政经理': 8, '技术中心经理': 9,
        '档案室': 10, '商务助理': 11}


class Worknode(models.Model):
    FILE = ((1,'总流程'),
            (2, '其他费用'),
            (3, '设备更改'),
            (4, '施工材料'),
            (5, '工时记录'),
            (6, '竣工报告'),
            (7, '自评表'),
            (8, '设备信息表')
    )
    doc = models.IntegerField(_("审批文件"),blank=True,null=True, choices=FILE)
    flow = models.CharField(verbose_name='流程',default=0,max_length=12)

    def __str__(self):
        return self.FILE[self.doc-1][1]+"的流程"
    class Meta:
        verbose_name = _("流程")
        verbose_name_plural = _("流程")

def get_node(num):
    flow = Worknode.objects.get(doc = num).flow
    work_node = []
    work_node.append((0,'等待填写人发起'))
    for i in range(0,len(flow)):
        data = flow[i]
        if flow[i] == 'a':
            data = '10'
        elif flow[i] == 'b':
            data = '11'
        work_node.append((i+1,user_models.Employee.RANK[int(data)][1]))


    work_node.append((len(work_node)+1, '完成'))
    return tuple(work_node)
def trans(tup):
    togo = []
    tool = {'普通员工': 0, '总经理': 1, '商务经理': 2, '财务经理': 3, '工程经理': 4, '技术经理': 5, '库管': 6, '营销经理': 7, '行政经理':8,'技术中心经理':9,'档案室':10,'商务助理':11}
    for t in tup:
        if t[0] ==0 or t[1]=='完成':
            pass
        else:
            togo.append((t[0],tool[t[1]]))

    return tuple(togo)


class Project(models.Model):
    """
    工程项目
    """
    budge = 0
    index_weight = 1

    active = models.BooleanField(verbose_name=u'状态',default=True)
    begin = models.DateField(_('开始日期'), blank=True, null=True)

    starter = models.ForeignKey(user_models.Employee,verbose_name=u"合同签约人",on_delete=models.CASCADE)
    name = models.CharField(verbose_name=u"执行编号", max_length=const.DB_CHAR_NAME_40)
    contract = models.CharField(verbose_name=u"合同编号", max_length=const.DB_CHAR_NAME_40,blank = True,default = '')
    cusname = models.CharField(verbose_name=u"客户单位",max_length=const.DB_CHAR_NAME_20,default='',blank=True)
    cusaddr = models.CharField(verbose_name=u"客户地址",max_length=const.DB_CHAR_NAME_40,default='',blank=True)
    recname = models.CharField(verbose_name=u"收货单位",max_length=const.DB_CHAR_NAME_20,default='',blank=True)
    recaddr = models.CharField(verbose_name=u"收货地址",max_length=const.DB_CHAR_NAME_40,default='',blank=True)
    receiver = models.CharField(verbose_name=u"收货人", max_length=const.DB_CHAR_CODE_10,default='',blank=True)
    receiverdep = models.CharField(_(u"收货部门"),max_length=const.DB_CHAR_NAME_20,default='',blank=True)
    receiverphone = models.CharField(_(u"收货手机"),max_length=const.DB_CHAR_NAME_20,default='',blank=True)
    receivertele = models.CharField(_(u"收货电话"), max_length=const.DB_CHAR_NAME_20,default='',blank=True)
    payer = models.CharField(verbose_name=u"付款人", max_length=const.DB_CHAR_CODE_10,default='',blank=True)
    payerdep = models.CharField(_(u"付款部门"), max_length=const.DB_CHAR_NAME_20,default='',blank=True)
    payerphone = models.CharField(_(u"付款手机"), max_length=const.DB_CHAR_NAME_20,default='',blank=True)
    payertele = models.CharField(_(u"付款电话"), max_length=const.DB_CHAR_NAME_20,default='',blank=True)
    total_price = models.DecimalField(verbose_name=u"合同金额",max_length=const.DB_CHAR_CODE_10,default=0,blank=True, null=True,max_digits=10,decimal_places=2)
    end = models.DateField(_('完工日期'), blank=True, null=True)
    deliver_time = models.CharField(_('收款日期'),max_length=const.DB_CHAR_NAME_40, blank=True, null=True)
    kaipiao = models.BooleanField(_(u"开票"),default=False)
    niehe_hour = models.PositiveIntegerField(verbose_name=u'内核工时数',null= True, blank= True,default=0)
    total_hour = models.PositiveIntegerField(verbose_name=u'总工时',null= True, blank= True,default=0)
    hour_cost = models.PositiveIntegerField(verbose_name=u'工时费',null= True, blank= True,default=0)
    total_mat = models.PositiveIntegerField(verbose_name=u'材料金额',null= True, blank= True,default=0)
    total_money = models.PositiveIntegerField(verbose_name=u'合计费用',null= True, blank= True,default=0)
    total_out = models.PositiveIntegerField(verbose_name=u'其他费用',null= True, blank= True,default=0)



    description = models.TextField(verbose_name=u"其他",blank=True,null=True)

    manager = models.ForeignKey(user_models.Employee,verbose_name=u"项目经理",related_name=u"manager",blank=True,null=True,on_delete=models.CASCADE)

    comment = models.TextField(verbose_name=u"批示",blank=True,null=True)
    associated_file = models.FileField(_("文件"),upload_to='excel',blank=True,null=True)

    """工作流"""
    WORK_FLOW_NODE = get_node(1)




    workflow_node = models.IntegerField(default=0, verbose_name=u"工作流节点", choices=WORK_FLOW_NODE)
    def restart(self):
        self.WORK_FLOW_NODE = get_node(1)
        self.workflow_node = self.WORK_FLOW_NODE[1]
        self.save()
    def updateMoney(self):
        try:
            self.total_money = self.total_mat+self.total_out+self.hour_cost
            self.save()
        except Exception:
            return
    def get_starter(self):
        return self.starter
    def get_curr_node(self):
        return self.WORK_FLOW_NODE[self.workflow_node][1]

    def to_next(self):
        if self.workflow_node ==len(self.WORK_FLOW_NODE)-2:
            self.workflow_node += 1
            self.active = False
            TodoList.objects.filter(project=self).delete()
            History.objects.filter(project=self).delete()
            History.objects.create(project=self,user=self.starter,memo='项目完成')

            History.objects.create(project=self,user=self.manager,memo='项目完成')

            print("流程全部完成")

            return
        elif self.workflow_node <len(self.WORK_FLOW_NODE):
            self.workflow_node+=1
            self.save()
            if trans(self.WORK_FLOW_NODE)[self.workflow_node-1][1] == 0:
                user = self.manager
            else:
                user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node-1][1])
            TodoList.objects.create(project=self, user=user , memo = "总流程  上一节点为 "+self.WORK_FLOW_NODE[self.workflow_node-1][1],content_type=1)
            if self.WORK_FLOW_NODE[self.workflow_node-1][1] == '总经理':
                if len(TodoList.objects.filter(project=self, user=user_models.Employee.objects.get(title=6),
                                        memo="请安排出货", content_type=1)) ==0:
                    TodoList.objects.create(project=self, user=user_models.Employee.objects.get(title=6),
                                        memo="请安排出货", content_type=1)
        else:
            print("已终结或暂挂，无法流程继续")

    def go_back(self):

        if self.workflow_node == 0:
            self.active = False
            TodoList.objects.filter(project=self).delete()
            self.save()
        else:
            self.workflow_node -= 1
            self.save()
            if self.workflow_node == 0:
                user = self.starter

            else:
                user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node-1][1])
            TodoList.objects.create(project=self, user=user , memo = "总流程  由"+self.WORK_FLOW_NODE[self.workflow_node+1][1]+"退回",content_type=1)


    def __str__(self):
        return self.name

    def get_project(self):
        return

    def get_all_devices_price(self):
        ds = Device.objects.filter(project_info=self)
        total = 0
        for d in ds:
            total += d.get_total_sale_price()
        return total

    class Meta:
        verbose_name = u"项目"
        verbose_name_plural = u"项目"


from django.db import models
class Device_form(models.Model):

    project_info = models.ForeignKey(Project, on_delete=models.CASCADE,verbose_name=u"所属项目", null=True)
    total_price = models.DecimalField(verbose_name=u"合计金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                    null=True, max_digits=10, decimal_places=2)
    total_buyprice = models.DecimalField(verbose_name=u"合计采购金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                      null=True, max_digits=10, decimal_places=2)
    file = models.FileField(upload_to='uploads/',verbose_name='导入EXCEL文件',blank=True,null=True)

    def __str__(self):
        return self.project_info.name+'的设备表'

    def save_change(self):
        ds = Device.objects.filter(device_form = self)
        total = 0
        total_buy = 0
        for d in ds:
            if d.get_total_sale_price is not None and d.get_total_buy_price is not None:
                total += d.get_total_sale_price()
                total_buy += d.get_total_buy_price()
        self.total_price = total
        self.total_buyprice = total_buy
        self.file = None
        self.save()

    class Meta:
        verbose_name = u"设备表"
        verbose_name_plural = u"设备表"

class Device(models.Model):
    project_info = models.ForeignKey(Project, on_delete=models.CASCADE,verbose_name=u"所属项目",default=None, null=True,blank=True)
    device_form = models.ForeignKey(Device_form, on_delete=models.CASCADE,verbose_name=u"表单",default=None, null=True,blank=True)
    thisid = models.IntegerField(default=0,verbose_name="序号",null=True,blank=True)
    name = models.TextField(default="", verbose_name=u"设备名称",blank=True, null=True)
    brand = models.CharField(verbose_name=u"品牌",max_length=const.DB_CHAR_NAME_20,blank=True, null=True)
    type = models.CharField(verbose_name=u"型号",blank=True, null=True,max_length=const.DB_CHAR_NAME_20)
    specification = models.TextField(verbose_name=u"规格",blank=True, null=True)
    num = models.IntegerField(verbose_name=u"数量",blank=True, null=True)
    unit = models.CharField(verbose_name=u"单位",max_length=const.DB_CHAR_CODE_4,blank=True, null=True)
    sale_price = models.DecimalField(verbose_name=u"单价",max_length=const.DB_CHAR_CODE_8,default=0,blank=True, null=True,max_digits=10,decimal_places=2)
    total_price = models.DecimalField(verbose_name=u"金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                     null=True, max_digits=10, decimal_places=2)
    insurance = models.CharField(verbose_name=u"保修", max_length=const.DB_CHAR_CODE_10, default=u"", blank=True,
                                 null=True)
    Inquiry_price = models.DecimalField(verbose_name=u"询价单价", max_length=const.DB_CHAR_CODE_8, blank=True, null=True, max_digits=10, decimal_places=2)
    insurance_g = models.CharField(verbose_name=u"保修承诺", max_length=const.DB_CHAR_CODE_10, default=u"", blank=True,
                                 null=True)
    buy_from = models.TextField(verbose_name=u"供应商", blank=True, null=True)
    buy_price = models.DecimalField(verbose_name=u"采购单价", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                    null=True, max_digits=10, decimal_places=2)
    total_buy_price = models.DecimalField(verbose_name=u"采购金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                      null=True, max_digits=10, decimal_places=2)
    insurance_to = models.CharField(verbose_name=u"保修期", blank=True, null=True,max_length=const.DB_CHAR_NAME_20)
    time_deliver = models.DateField(verbose_name=u"到货时间", blank=True, null=True)
    tiaojian = models.CharField(verbose_name=u"付款条件", max_length=const.DB_CHAR_NAME_20,blank=True, null=True)
    def __str__(self):
        return self.name;



    def get_total_sale_price(self):
        title = u'金额'
        if self.num!=None and self.sale_price!=None:
            return self.sale_price* self.num
        else:
            return 0



    def get_total_buy_price(self):
        if self.num!=None and self.buy_price!=None:
            return self.buy_price * self.num
        return 0
    def save_change(self):
        self.total_buy_price = self.get_total_buy_price()
        self.total_price = self.get_total_sale_price()
        self.save()


    get_total_sale_price.allow_tags = True
    get_total_sale_price.short_description = _("金额")

    class Meta:
        verbose_name=u"设备单项"
        verbose_name_plural=u"设备单项"

class Device_changelog(models.Model):
    time = models.DateField(verbose_name=u"添加时间", blank=True, null=True)
    thisid = models.IntegerField(verbose_name="序号",blank = True,null = True)
    project_info = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=u"所属项目", null=True)
    agreed = models.BooleanField(verbose_name=u"已审批完成", default=False)
    note = models.CharField(max_length=const.DB_CHAR_NAME_40, default="", verbose_name=u"备注", blank=True, null=True)
    log = models.TextField(default="", verbose_name=u"报告", blank=True, null=True)
    total_price = models.DecimalField(verbose_name=u"总变动金额", max_length=const.DB_CHAR_CODE_10, default=0, blank=True,
                                      null=True, max_digits=10, decimal_places=2)

    device = models.ManyToManyField(Device, verbose_name=u"选择设备", blank=True)

    WORK_FLOW_NODE = get_node(3)

    workflow_node = models.IntegerField(default=0, verbose_name=u"工作流节点", choices=WORK_FLOW_NODE)


    def get_last_user_rank(self):
        if self.workflow_node == 1:
            return self.project_info.starter
        return user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])

    def get_starter(self):
        return self.project_info.starter
    def __str__(self):
        return self.project_info.name + "的第"+str(self.thisid)+"次设备更改"

    def to_next(self):
        if self.workflow_node < len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
            TodoList.objects.create(project=self.project_info, user=user,content_type=3,
                                    memo="设备更改  上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node - 1][1])


        elif self.workflow_node == len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            self.agreed = True

        self.save()

    def go_back(self):
        if self.workflow_node != 0:
            self.workflow_node -= 1
        self.save()

        user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node-1][1])
        TodoList.objects.create(project=self.project_info, user=user , memo = "设备更改  上一节点为 "+self.WORK_FLOW_NODE[self.workflow_node+1][1]+"退回",content_type=3)

    class Meta:
        verbose_name=u"修改记录"
        verbose_name_plural=u"修改记录"



class Device_change(models.Model):

    thisid = models.IntegerField(verbose_name="序号",blank = True,null = True)
    name = models.TextField(default="", verbose_name=u"设备名称",blank=True, null=True)
    brand = models.CharField(verbose_name=u"品牌", max_length=const.DB_CHAR_NAME_20, blank=True,
                             null=True)
    type = models.CharField(verbose_name=u"型号", max_length=const.DB_CHAR_NAME_20, blank=True, null=True)
    specification = models.TextField(verbose_name=u"规格",blank=True, null=True)
    num = models.IntegerField(verbose_name=u"数量", blank=True, null=True)
    unit = models.CharField(verbose_name=u"单位", max_length=const.DB_CHAR_CODE_4, blank=True,
                            null=True)
    sale_price = models.DecimalField(verbose_name=u"单价", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                     null=True, max_digits=7, decimal_places=2)
    total_price = models.DecimalField(verbose_name=u"金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                      null=True, max_digits=7, decimal_places=2)
    buy_price = models.DecimalField(verbose_name=u"成本单价", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                    null=True, max_digits=7, decimal_places=2)
    total_buy_price = models.DecimalField(verbose_name=u"成本金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                      null=True, max_digits=7, decimal_places=2)
    reason = models.CharField(verbose_name=u"变更原因", max_length=const.DB_CHAR_NAME_40, blank=True, null=True)
    memo = models.CharField(verbose_name=u"说明", max_length=const.DB_CHAR_NAME_40, blank=True, null=True)

    change_log = models.ForeignKey(Device_changelog,verbose_name=u"修改次数", blank=True, null=True,on_delete=models.CASCADE)


    def get_total_sale_price(self):
        if self.num != None and self.sale_price != None:
            return self.sale_price * self.num
        else:
            return 0
    def get_total_buy_price(self):
        if self.buy_price is None or self.num is None:
            return 0
        return self.buy_price * self.num
    def save_change(self):
        self.total_buy_price = self.get_total_buy_price()
        self.total_price = self.get_total_sale_price()
        self.save()


    def __str__(self):
        return str(self.change_log) + "的单项"


    class Meta:
        verbose_name = u"设备更改"
        verbose_name_plural = u"设备更改"


class Outsource(models.Model):

    project_info = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name=u"项目名字",blank=True, null=True)
    myname = models.CharField(max_length=const.DB_CHAR_CODE_10, default="", verbose_name=u"营销员", blank=True, null=True)
    begin_time = models.DateField(verbose_name=u"计划开工时间",blank=True,null=True)
    end_time = models.DateField(verbose_name=u"计划竣工时间",blank=True,null=True)
    description = models.TextField(default="", verbose_name=u"工程内容", blank=True, null=True)
    fuzeren = models.CharField(max_length=const.DB_CHAR_CODE_8, default="", verbose_name=u"项目负责人", blank=True, null=True)

    price = models.DecimalField(verbose_name=u"外包施工单位报价", max_length=const.DB_CHAR_CODE_10, default=0, blank=True,
                                     null=True, max_digits=10, decimal_places=2)

    total_price = models.DecimalField(verbose_name=u"总价", max_length=const.DB_CHAR_CODE_10, default=0, blank=True,
                                     null=True, max_digits=10, decimal_places=2)
    recom = models.CharField(max_length=20, default="", verbose_name=u"推荐施工单位", blank=True, null=True)

    project_info = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name=u"项目名字",blank=True, null=True)
    agreed = models.BooleanField(verbose_name=u"已审批完成", default=False)
    WORK_FLOW_NODE = get_node(2)

    workflow_node = models.IntegerField(default=0, verbose_name=u"工作流节点", choices=WORK_FLOW_NODE)
    class Meta:
        verbose_name = u"其他费用"
        verbose_name_plural = u"其他费用"

    def __str__(self):
        return self.project_info.name + "的其他费用表"


    def get_last_user_rank(self):
        return user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])

    def to_next(self):
        if self.workflow_node < len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
            TodoList.objects.create(project=self.project_info, user=user,content_type=2,
                                    memo="其他费用  上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node - 1][1])


        elif self.workflow_node == len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            self.agreed = True

            self.project_info.total_out = self.total_price
            self.project_info.save()

        self.save()

    def go_back(self):
        if self.workflow_node != 0:
            self.workflow_node -= 1
        self.save()

        user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
        TodoList.objects.create(project=self.project_info, user=user, content_type=2,
                                memo="其他费用  由上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node + 1][1] + "退回")

    def get_starter(self):
        return user_models.Employee.objects.get(title = 4)



class Outsource_items(models.Model):

    thisid = models.IntegerField(verbose_name="序号",blank = True,null = True)
    outsource_info = models.ForeignKey(Outsource,on_delete=models.CASCADE,verbose_name=u"所属外包项目",blank=True, null=True)
    item_name = models.CharField(max_length=const.DB_CHAR_NAME_20,default="",verbose_name=u"外包施工单位名称",blank=True, null=True)
    provider = models.CharField(max_length=const.DB_CHAR_CODE_8,default="",verbose_name=u"外包施工负责人",blank=True, null=True)
    num = models.IntegerField(default=0,validators=[MaxValueValidator(5000),MinValueValidator(0)],verbose_name=u"外包数量")
    price = models.DecimalField(verbose_name=u"单价", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                     null=True, max_digits=7, decimal_places=2)

    total_price = models.DecimalField(verbose_name=u"金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                     null=True, max_digits=10, decimal_places=2)
    note = models.CharField(max_length=const.DB_CHAR_CODE_10, default="", verbose_name=u"备注", blank=True, null=True)

    def get_total(self):
        return self.num * self.price


    def __str__(self):
        return self.outsource_info.project_info.name + "的外包明细"
    class Meta:
        verbose_name = u"外包项目明细"
        verbose_name_plural = u"外包项目明细"


class Material_log(models.Model):
    total = models.DecimalField(verbose_name=u"总金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                null=True, max_digits=7, decimal_places=2)

    project_info = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=u"所属项目", null=True)

    agreed = models.BooleanField(verbose_name=u"已审批完成", default=False)

    WORK_FLOW_NODE = get_node(4)

    workflow_node = models.IntegerField(default=0, verbose_name=u"工作流节点", choices=WORK_FLOW_NODE)

    def get_starter(self):
        return self.project_info.manager


    def get_last_user_rank(self):
        if self.workflow_node == 1:
            return self.project_info.manager
        elif self.workflow_node == 0:
            return None
        return user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])

    def to_next(self):
        if self.workflow_node < len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1

            user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
            TodoList.objects.create(project=self.project_info, user=user,content_type=4,
                                    memo="材料领用  上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node - 1][1])


        elif self.workflow_node == len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            self.agreed = True

        self.save()

    def go_back(self):
        if self.workflow_node != 1 and self.workflow_node != 0:
            self.workflow_node -= 1
            user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
        elif self.workflow_node == 1:
            print("gogo")
            self.workflow_node -= 1
            user = self.project_info.manager

        self.save()

        TodoList.objects.create(project=self.project_info, user=user, content_type=4,
                                memo="材料领用  由上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node + 1][1]+"退回")

    def back_to(self, node_num):
        if node_num < 3:
            self.workflow_node = node_num
        else:
            print("num is too large")

    def deny_table(self):
        self.workflow_node = 0


    def __str__(self):
        return self.project_info.name + "的施工材料领用记录"
    class Meta:
        verbose_name = u"材料领用"
        verbose_name_plural = u"材料领用"

class Material_use(models.Model):

    thisid = models.IntegerField(verbose_name="序号",blank = True,null = True)
    material_log = models.ForeignKey(Material_log, on_delete=models.CASCADE, verbose_name=u"所属项目", null=True)
    material_name = models.CharField(max_length=const.DB_CHAR_CODE_10, default="", verbose_name=u"名称", blank=True, null=True)
    brand = models.CharField(verbose_name=u"品牌", max_length=const.DB_CHAR_NAME_20, blank=True,
                             null=True)
    guige = models.CharField(max_length=const.DB_CHAR_CODE_10, default="", verbose_name=u"规格", blank=True,
                                     null=True)
    xinhao = models.CharField(max_length=const.DB_CHAR_CODE_10, default="", verbose_name=u"型号", blank=True,
                                     null=True)
    num = models.IntegerField(default=1, validators=[MaxValueValidator(10000), MinValueValidator(0)], verbose_name=u"数量")
    unit = models.CharField(verbose_name=u"单位", max_length=const.DB_CHAR_CODE_4, blank=True,
                            null=True)

    price = models.DecimalField(verbose_name=u"单价", max_length=const.DB_CHAR_CODE_8, blank=True,default=0,
                                     null=True, max_digits=7, decimal_places=2)

    total_price = models.DecimalField(verbose_name=u"金额", max_length=const.DB_CHAR_CODE_8, blank=True,default=0,
                                     null=True, max_digits=7, decimal_places=2)

    def __str__(self):
        return self.material_log.project_info.name + "的施工材料领用项目"

    def save_change(self):
        self.total_price = self.price *self.num
        self.save()

    class Meta:
        verbose_name = u"材料领单项"
        verbose_name_plural = u"材料领用单项"

class Device_finalform(models.Model):
    project_info = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=u"所属项目", null=True)
    file = models.FileField(upload_to='uploads/', verbose_name='导入EXCEL文件', blank=True, null=True)
    agreed = models.BooleanField(verbose_name=u"已审批完成", default=False)
    WORK_FLOW_NODE = get_node(8)
    workflow_node = models.IntegerField(default=0, verbose_name=u"工作流节点", choices=WORK_FLOW_NODE)

    device = models.ManyToManyField(Device, verbose_name=u"选择设备", blank=True,related_name='设备')



    def get_last_user_rank(self):
        if self.workflow_node == 1:
            return self.project_info.manager
        return user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])

    def get_starter(self):
        return self.project_info.manager
    def __str__(self):
        return self.project_info.name + "的设备信息表"

    def to_next(self):
        if self.workflow_node < len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1

            user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
            TodoList.objects.create(project=self.project_info, user=user, content_type=8,
                                    memo="设备信息  上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node - 1][1])


        elif self.workflow_node == len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            self.agreed = True

        self.save()

    def go_back(self):
        if self.workflow_node != 0:
            self.workflow_node -= 1
        self.save()

        user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
        TodoList.objects.create(project=self.project_info, user=user, content_type=8,
                                memo="设备信息  由上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node + 1][1] + "退回")

    def back(self, node_num):
        if node_num < 3:
            self.workflow_node = node_num
        else:
            print("num is too large")

    def deny_table(self):
        self.workflow_node = 0

    class Meta:
        verbose_name=u"设备信息"
        verbose_name_plural=u"设备信息"

class Device_final(models.Model):

    thisid = models.IntegerField(verbose_name="序号",blank = True,null = True)
    name = models.TextField( default="", verbose_name=u"设备名称",blank=True, null=True)
    brand = models.CharField(verbose_name=u"品牌",max_length=const.DB_CHAR_NAME_20,blank=True, null=True,default='')
    type = models.CharField(verbose_name=u"型号",max_length=const.DB_CHAR_NAME_20,blank=True, null=True)
    specification = models.TextField(verbose_name=u"规格",blank=True, null=True)
    producer = models.TextField(verbose_name=u"生产厂家",blank=True, null=True)
    produce_num = models.CharField(verbose_name=u"出厂编号", max_length=const.DB_CHAR_NAME_20, blank=True, null=True)
    produce_time = models.DateField(verbose_name=u"出厂日期",blank = True, null = True)
    place_keep = models.CharField(verbose_name=u"存放地点", max_length=const.DB_CHAR_NAME_20, blank=True, null=True)
    bill_num = models.CharField(verbose_name=u"单据号", max_length=const.DB_CHAR_CODE_10, blank=True, null=True)
    price = models.DecimalField(verbose_name=u"单价", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                    null=True, max_digits=9, decimal_places=2)
    time_install = models.DateField(verbose_name=u"安装日期", blank=True, null=True)
    record = models.TextField(verbose_name=u"维修记录", blank=True, null=True)
    note = models.CharField(verbose_name=u"备注", max_length=const.DB_CHAR_NAME_120, blank=True, null=True)


    form = models.ForeignKey(Device_finalform, on_delete=models.CASCADE,verbose_name=u"表单", null=True)


    def __str__(self):
        return str(self.form) + "单项"


    class Meta:
        verbose_name=u"设备信息单项"
        verbose_name_plural=u"设备信息单项"


class Finish_report(models.Model):

    project_info = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=u"所属项目", null=True)
    time = models.DateField(verbose_name=u"日期", auto_now_add=True, blank=True, null=True)
    details = models.TextField(verbose_name=u"报告", blank=True, null=True)
    agreed = models.BooleanField(verbose_name=u"已审批完成", default=False)
    WORK_FLOW_NODE = get_node(6)

    workflow_node = models.IntegerField(default=0, verbose_name=u"工作流节点", choices=WORK_FLOW_NODE)

    def get_starter(self):
        return self.project_info.manager



    def get_last_user_rank(self):
        if self.workflow_node == 1:
            return self.project_info.manager
        return user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])

    def to_next(self):
        if self.workflow_node < len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1

            user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
            TodoList.objects.create(project=self.project_info, user=user, content_type=6,
                                    memo="竣工报告  上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node - 1][1])


        elif self.workflow_node == len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            self.agreed = True

        self.save()

    def go_back(self):
        if self.workflow_node != 0:
            self.workflow_node -= 1
        self.save()

        user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
        TodoList.objects.create(project=self.project_info, user=user, content_type=6,
                                memo="竣工报告  由上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node + 1][1] + "退回")

    def back_to(self, node_num):
        if node_num < 3:
            self.workflow_node = node_num
        else:
            print("num is too large")

    def deny_table(self):
        self.workflow_node = 0

    def __str__(self):
        return self.project_info.name + "的竣工报告"

    class Meta:
        verbose_name=u"竣工报告"
        verbose_name_plural=u"竣工报告"

class work_report(models.Model):
    name = models.CharField(max_length=20, default="", verbose_name=u"月份",blank=True, null=True)
    input_date = models.DateField(verbose_name=u"填写日期", auto_now_add=True, blank=True, null=True)
    project_info = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=u"所属项目", null=True)
    agreed = models.BooleanField(verbose_name=u"已审批完成", default=False)
    note = models.TextField(verbose_name=u"合计绩效工资",default='',blank=True)
    WORK_FLOW_NODE = get_node(5)
    workflow_node = models.IntegerField(default=0, verbose_name=u"工作流节点", choices=WORK_FLOW_NODE)



    def get_last_user_rank(self):
        if self.workflow_node == 1:
            return self.project_info.manager
        return user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])

    def get_starter(self):
        return self.project_info.manager
    def __str__(self):
        return str(self.project_info.name) + "的"+str(self.name)+"工时记录"

    def to_next(self):
        if self.workflow_node < len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1

            user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
            TodoList.objects.create(project=self.project_info, user=user, content_type=5,
                                    memo="工时记录  上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node - 1][1])


        elif self.workflow_node == len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            self.agreed = True

        self.save()

    def go_back(self):
        if self.workflow_node != 0:
            self.workflow_node -= 1
        self.save()

        user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
        TodoList.objects.create(project=self.project_info, user=user, content_type=5,
                                memo="工时记录  由上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node + 1][1] + "退回")

    def back_to(self, node_num):
        if node_num < 3:
            self.workflow_node = node_num
        else:
            print("num is too large")

    def deny_table(self):
        self.workflow_node = 0

    class Meta:
        verbose_name=u""
        verbose_name_plural=u"工时记录"

class work_hour(models.Model):

    thisid = models.IntegerField(verbose_name="序号",blank = True,null = True)
    input_date = models.DateField(verbose_name=u"填写日期", auto_now_add=True, blank=True, null=True)
    employee = models.ForeignKey(user_models.Employee,verbose_name=u"施工人员姓名",blank=True, null=True,on_delete=models.CASCADE)
    start_time = models.DateField(verbose_name=u"开始日期", blank=True, null=True)
    finish_time = models.DateField(verbose_name=u"结束日期", blank=True, null=True)
    time = models.CharField(verbose_name=u"时间段", max_length=const.DB_CHAR_NAME_20, blank=True, null=True)
    work_content = models.CharField(verbose_name=u"工作内容", max_length=const.DB_CHAR_NAME_60, blank=True, null=True)
    inside_work_hour = models.DecimalField(verbose_name=u"上班工时系数/单价100", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                null=True, max_digits=4, decimal_places=1)

    inside_price = models.DecimalField(verbose_name=u"上班绩效工资", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                null=True, max_digits=7, decimal_places=2)

    extra_work_hour = models.DecimalField(verbose_name=u"加班工时系数/单价200", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                null=True, max_digits=4, decimal_places=1)
    extra_price = models.DecimalField(verbose_name=u"加班绩效工资", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                null=True, max_digits=7, decimal_places=2)
    total_price = models.DecimalField(verbose_name=u"合计绩效工资", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                null=True, max_digits=7, decimal_places=2)
    work_report = models.ForeignKey(work_report, on_delete=models.CASCADE, verbose_name=u"所属项目", null=True)





    def save_change(self):

        self.extra_price = self.extra_work_hour*200
        self.inside_price = self.inside_work_hour*100
        self.total_price = self.extra_price + self.inside_price
        self.save()

    class Meta:
        verbose_name = u"工时记录单项"
        verbose_name_plural = u"工时记录单项"

class feedback_form(models.Model):

    bonus = models.DecimalField(verbose_name=u"项目经理奖励金额", max_length=const.DB_CHAR_CODE_8, default=0, blank=True,
                                    null=True, max_digits=9, decimal_places=2)
    agreed = models.BooleanField(verbose_name=u"已审批完成", default=False)
    total_self = models.PositiveIntegerField(verbose_name=u"总自评", blank=True, null=True)
    total_point = models.PositiveIntegerField(verbose_name=u"总得分", blank=True, null=True)

    project_info = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=u"所属项目", null=True)
    WORK_FLOW_NODE = get_node(7)
    workflow_node = models.IntegerField(default=0, verbose_name=u"工作流节点", choices=WORK_FLOW_NODE)



    def get_last_user_rank(self):
        if self.workflow_node == 1:
            return self.project_info.manager
        return user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])

    def __str__(self):
        return self.project_info.name +"的项目经理考核"

    def get_starter(self):
        return self.project_info.manager

    def to_next(self):
        if self.workflow_node < len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1

            user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
            TodoList.objects.create(project=self.project_info, user=user, content_type=7,
                                    memo="项目经理考核  上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node - 1][1])


        elif self.workflow_node == len(self.WORK_FLOW_NODE) - 2:
            self.workflow_node += 1
            self.agreed = True

        self.save()

    def go_back(self):
        if self.workflow_node != 0:
            self.workflow_node -= 1
        self.save()

        user = user_models.Employee.objects.get(title=trans(self.WORK_FLOW_NODE)[self.workflow_node - 1][1])
        TodoList.objects.create(project=self.project_info, user=user, content_type=7,
                                memo="项目经理考核  由上一节点为 " + self.WORK_FLOW_NODE[self.workflow_node + 1][1] + "退回")

    def back_to(self, node_num):
        if node_num < 5:
            self.workflow_node = node_num
        else:
            print("num is too large")


    def deny_table(self):
        self.workflow_node = 0

    class Meta:
        verbose_name = u"项目经理考核"
        verbose_name_plural = u"项目经理考核"



class feedback_report(models.Model):
    idnum = models.PositiveIntegerField(verbose_name=u"序号", blank=True, null=True)
    item =  models.CharField(verbose_name=u"考核项目",max_length=const.DB_CHAR_NAME_40,blank=True, null=True)
    standard = models.CharField(verbose_name=u"考核标准",max_length=const.DB_CHAR_NAME_200,blank=True, null=True)
    points = models.PositiveIntegerField(verbose_name=u"分值")
    self_eva = models.PositiveIntegerField(verbose_name="自评分",default=0)
    eva = models.PositiveIntegerField(verbose_name="得分",default=0)
    note = models.CharField(verbose_name=u"说明",max_length=const.DB_CHAR_NAME_60,blank=True, null=True)

    feedback_form = models.ForeignKey(feedback_form, on_delete=models.CASCADE, verbose_name=u"表单", null=True)

    class Meta:
        verbose_name = u"项目经理考核单项"
        verbose_name_plural = u"项目经理考核单项"


"""work flow model"""






class History(models.Model):
    """
    workflow history
    """
    PROCESS_TYPE = (
        (0, u"提交"),
        (1, u"同意"),
        (2, u"反对"),
        (3, u"终止"),

    )
    index_weight = 5

    project = models.ForeignKey(Project,verbose_name=_("项目"),on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(user_models.Employee, verbose_name=u"用户", on_delete=models.CASCADE)
    pro_time = models.DateTimeField(verbose_name=u"操作时间",auto_now=True)
    pro_type = models.IntegerField(verbose_name=u"操作类别", choices=PROCESS_TYPE,default=0)
    memo = models.CharField(verbose_name="备注",max_length=const.DB_CHAR_NAME_40,blank=True,null=True)

    def get_project_desc(self):
        if self.node:
            return self.node.name
        else:
            return u'启动'

    def get_action_desc(self):
        action_mapping = {0:u'提交',1:u'同意',2:u'拒绝',3:u'终止'}
        # print action_mapping
        if self.pro_type:
            return action_mapping[self.pro_type]
        else:
            return u'提交'

    def get_memo_desc(self):
        if self.memo:
            return self.memo
        else:
            return ''

    def href(self):
        title = u"项目链接"
        return format_html("<a href='/admin/basedata/project/{}/change'>{}</a>",
                           self.project.id, title)

    def navi_href(self):
        title = self.project.name

        return format_html("<a href='/admin/basedata/project/{}/change'>{}</a>",
                           self.project.id, title)

    href.allow_tags = True
    href.short_description = _("项目链接")

    class Meta:
        verbose_name = _("历史事务")
        verbose_name_plural = _("历史事务")
        ordering = ['-pro_time','project']


class TodoList(models.Model):
    """

    """
    FILE = ((1,'总流程'),
            (2, '其他费用'),
            (3, '设备更改'),
            (4, '施工材料'),
            (5, '工时记录'),
            (6, '竣工报告'),
            (7, '自评表'),
            (8, '设备信息表')
    )
    code = models.CharField(_("编码"),max_length=const.DB_CHAR_CODE_10,blank=True,null=True)
    project = models.ForeignKey(Project,verbose_name=_("项目"),on_delete=models.CASCADE)
    user = models.ForeignKey(user_models.Employee,verbose_name=_("操作人"),on_delete=models.CASCADE)
    arrived_time = models.DateTimeField(_("消息时间"), auto_now=True)
    is_read = models.BooleanField(_("已读?"),default=False)
    read_time = models.DateTimeField(_("阅读时间"),blank=True,null=True)
    status = models.BooleanField(_("已完结"),default=False)
    memo = models.CharField(verbose_name=_("备注"),max_length=const.DB_CHAR_NAME_40,blank=True,null=True)
    content_type = models.IntegerField(verbose_name=u"任务类别", choices=FILE,default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(TodoList,self).save(force_update,force_update,using,update_fields)
        if not self.code:
            self.code = 'TD%05d' % self.id
            self.save()

    def project_dsc(self):
        if self.project:
            return u'%s'%self.project.workflow_node
        else:
            return u'启动'


    def href(self):
        title = u"链接"

        return format_html("<a href='/admin/basedata/project/{}/change'>{}</a>",
                           self.project.id,title)

    def navi_href(self):
        title = self.project.name

        return format_html("<a href='/admin/basedata/project/{}/change'>{}</a>",
                           self.project.id, title)

    def detail(self):

        return self.project.WORK_FLOW_NODE
    def project_dsc(self):
        return u'%s'%(self.project.name)
    project_dsc.short_description = u'业务流程'


    href.allow_tags = True
    href.short_description = _("项目链接")



    class Meta:
        verbose_name = _("待办事务")
        verbose_name_plural = _("待办事务")
        ordering = ['user','-arrived_time']



