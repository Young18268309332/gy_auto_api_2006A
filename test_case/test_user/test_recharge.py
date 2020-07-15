import random

import allure
import requests
  # 通过自己写框架生成allure文件，并在reports中查看文件内容

from config.conf import API_URL
from test_case.conftest import pub_data


@allure.feature("用户管理")  #第一等级
@allure.story("充值提现")  #第二等级
@allure.title("扣款接口-账户金额不足")  #第三等级
def test_recharge_op (db):
     # 执行查询sql语句
     with allure.step("第一步,执行sql语句"):
        res = db.select_execute("SELECT account_name FROM `t_cst_account` WHERE STATUS = 0 AND account_name IS NOT NULL")

        allure.attach("SELECT account_name FROM `t_cst_account` WHERE STATUS = 0 AND account_name IS NOT NULL","执行sql语句",allure.attachment_type.TEXT)
     with allure.step("第二步,从查询结果中随机获取一条,取第一条数据"):

        account_name = random.choice(res)[0]
        allure.attach(random.choice(res)[0],"请求数据",allure.attachment_type.TEXT)
     with allure.step("第三步,准备请求数据"):

         data={
             "accountName":account_name ,
             "changeMoney": 100
         }
     with allure.step("第四步,发送请求"):

        r = requests.post(API_URL + "/acc/charge",json=data)

     with allure.step("第五步,获取请求内容"):
         allure.attach(r.request.method,"请求方法",allure.attachment_type.TEXT)
         allure.attach(r.request.url,"请求url",allure.attachment_type.TEXT)
         allure.attach(str(r.request.headers),"请求头",allure.attachment_type.TEXT)
         allure.attach(r.request.body,"请求正文",allure.attachment_type.TEXT)

     with allure.step("第六步,获取响应内容"):
        allure.attach(str(r.status_code),"响应状态码",allure.attachment_type.TEXT)
        allure.attach(str(r.headers),"响应头",allure.attachment_type.TEXT)
        allure.attach(str(r.text),"响应正文",allure.attachment_type.TEXT)
     with allure.step("第七步,断言"):
         allure.attach(r.text,"实际结果",allure.attachment_type.TEXT)
         allure.attach("账户余额不足","实际结果",allure.attachment_type.TEXT)
         assert ("账户余额不足") in r.text


# '''
  #在terminal 输入这两行命令
#   pytest test_case/test_user.py --alluredir=reports/xml   生成reports xml 文件
#   allure generate reports/xml -o reports/html  把xml文件转换成能看懂的响应报告
#   allure generate reports/xml -o reports/html --clean
#
# '''