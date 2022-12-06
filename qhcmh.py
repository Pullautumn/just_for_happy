import requests, json, time, datetime, hashlib

# 企业微信推送参数
corpid = ''
agentid = ''
corpsecret = ''
touser = ''
# 推送加 token
plustoken = ''

# 茄皇登录https://apig.xiaoyisz.com/qiehuang/ga/public/api/login里面的请求body全部
# 抽中实物会推送 支持多账号 多账号格式 qhbody = ['qhbody1','qhbody2']
qhbody = [
    '',
    ''
]

#
def Push(contents):
    # 微信推送
    if all([corpid, agentid, corpsecret, touser]):
        token = \
            requests.get(
                f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}').json()[
                'access_token']
        json = {"touser": touser, "msgtype": "text", "agentid": agentid,
                "text": {"content": "茄皇抽盲盒\n" + contents}}
        resp = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", json=json)
        print('微信推送成功' if resp.json()['errmsg'] == 'ok' else '微信推送失败')

    if plustoken:
        headers = {'Content-Type': 'application/json'}
        json = {"token": plustoken, 'title': '茄皇抽盲盒', 'content': contents.replace('\n', '<br>'),
                "template": "json"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')


for a in range(len(qhbody)):
    sign_url = 'https://apig.xiaoyisz.com/qiehuang/ga/public/api/login'
    sign_headers = {
        'Host': 'apig.xiaoyisz.com',
        'Content-Type': 'application/json',
        'Origin': 'https://thekingoftomato.ioutu.cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d2f) NetType/4G Language/zh_CN miniProgram/wx532ecb3bdaaf92f9',
        'Referer': 'https://thekingoftomato.ioutu.cn/',
        'Content-Length': '134',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    }
    sign_data = f'{qhbody[a]}'

    re = requests.post(url=sign_url, headers=sign_headers, data=sign_data)
    Authorization = json.loads(re.text)['data']
    print(f'开始第{a+1}个帐号抽盲盒')
    # 获取时间戳和signature
    Timestamp = int(round(time.time() * 1000))
    signature = hashlib.md5(bytes(
        'clientKey=IfWu0xwXlWgqkIC7DWn20qpo6a30hXX6&clientSecret=A4rHhUJfMjw2I5CODh5g40Ja1d3Yk1CH&nonce=jXsxneKFRdXPmXHi&timestamp=' + f'{Timestamp}',
        encoding='utf-8')).hexdigest().upper()
    for i in range(5):
        draw_url = 'https://apig.xiaoyisz.com/qiehuang/ga/user/gift/box/drawPrize?timestamp=' + f'{Timestamp}' + '&nonce=jXsxneKFRdXPmXHi&signature=' + f'{signature}' + '&activityId=10001'
        draw_headers = {
            'Host': 'apig.xiaoyisz.com',
            'Content-Type': 'application/json',
            'Origin': 'https://thekingoftomato.ioutu.cn',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d2f) NetType/4G Language/zh_CN miniProgram/wx532ecb3bdaaf92f9',
            'Authorization': f'{Authorization}',
            'Referer': 'https://thekingoftomato.ioutu.cn/',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        }
        re_2 = requests.get(url=draw_url, headers=draw_headers)
        data = json.loads(re_2.text)
        if data['code'] == 0:
            print(f'第{i+1}次抽盲盒成功！')
        elif data['code'] == 1000:
            print('抽奖次数用完了，你还抽啥呢！！')
        else:
            print('抽奖失败！请检查配置是否正确')
        time.sleep(1)
#查询中奖纪录
    search_url = 'https://apig.xiaoyisz.com/qiehuang/ga/user/gift/box/prizeRecord?timestamp=' + f'{Timestamp}' + '&nonce=jXsxneKFRdXPmXHi&signature=' + f'{signature}'
    re_3 = requests.get(url=search_url, headers=draw_headers)
    data_3 = json.loads(re_3.text)
    for j in range(len(data_3['data'])):
        creatTime = data_3['data'][j]['creatTime']
        time_local = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(creatTime))
        name = data_3['data'][j]['name']
        type = data_3['data'][j]['type']
        message = str(time_local)+' '+name
        print(message)
        if type ==4 and "兑换券" in type:
            Push(contents=message)

