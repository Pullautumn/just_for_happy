import requests, json,time

# 逑美在线app 可以完成签到和抽卡人任务
# qmzxbody取app登录(使用帐号密码登录)界面登录后的https://api.qiumeiapp.com/qm/10001/qmLogin URL的请求body全部 放到单引号里面 多账号支持
# 示例'{"deviceNumber":"*****","anonymousId":"*****","appVersion":"7.2.1","appMarket":"appstore","password":"*****","deviceModel":"iPhone14,5","sign":"******","deviceToken":"*****==","phoneNumber":"*****"}',
qmzxbody = [
'',
''
]
# print(result)
# 获取token
for i in range(len(qmzxbody)):
    url = 'https://api.qiumeiapp.com/qm/10001/qmLogin'
    headers = {
        'Host': 'api.qiumeiapp.com',
        'Content-Type': 'application/json',
        'appVersion': '7.2.0',
        'Content-Length': '425',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'qiu mei zai xian/7.2.0 (iPhone; iOS 15.6; Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'Accept-Encoding': 'gzip, deflate, br',
        'appMarket': 'appstore-qmzx'
    }
    data = f"{qmzxbody[i]}"
    html = requests.post(url=url, headers=headers, data=data)
    data_1 = json.loads(html.text)
    print(f"账号{i+1}-"+data_1['data']['phoneNumber'])
    is_true = data_1['msg']
    if is_true == "登录成功!":
        print('登录成功')
    else:
        print('登录失败!')
    # 获取token
    qmUserToken = data_1['data']['qmUserToken']
    url_qd  ='https://api.qiumeiapp.com/qm-activity/qdcj/signin'
    headers = {
        'Host': 'api.qiumeiapp.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://h5.qiumeiapp.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Umeng4Aplus/1.0.0',
        'Referer': 'https://h5.qiumeiapp.com/',
        'Content-Length': '52',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    }
    data = f'qmUserToken={qmUserToken}'
    html_qd = requests.post(url=url_qd, headers=headers, data=data)
    data_3 = json.loads(html_qd.text)
    print(data_3['msg'])
    # 抽卡
    url_ck = 'https://api.qiumeiapp.com/qm-activity/qdcj/luckyDraw'
    html_2 = requests.post(url=url_ck, headers=headers, data=data)
    data_2 = json.loads(html_2.text)
    print(data_2['msg'])


    url_user ='https://api.qiumeiapp.com/qmxcx/10001/getQmUserPointInfo'
    url_run ='https://api.qiumeiapp.com/qm-activity/qdcj/getUserSigninInfo'
    token = f'appUserToken={qmUserToken}'
    html_user = requests.post(url=url_user, headers=headers, data=token)
    html_run = requests.post(url=url_run, headers=headers, data=data)
    data_4 = json.loads(html_user.text)
    data_5 = json.loads(html_run.text)
    print('本月登录天数: ' + str(data_5['data']['runningDays']) +' 豆豆余额: '+str(data_4['data']['totalAmount']))
    print('*****')
print("共"+str(len(qmzxbody))+"个帐号已经执行完毕,等待300秒关闭本窗口！！！")
time.sleep(300)
