import requests,json ,time, datetime,hashlib

# # 企业微信推送参数
# corpid = ''
# agentid = ''
# corpsecret = ''
# touser = ''
# # 推送加 token
# plustoken = '5c1524fa76a9420db7089decc1817f55'

#茄皇登录https://apig.xiaoyisz.com/qiehuang/ga/public/api/login里面的请求body全部
qhbody='{"appId":"wx532ecb3bdaaf92f9","openId":"oBk224nb3ruPrPfhTaRJidB4-a34","wid":3152750189,"signature":"3753808EA1D138880D410EC31430E7DC"}'


# def Push(contents):
#     # 微信推送
#     if all([corpid, agentid, corpsecret, touser]):
#         token = \
#         requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}').json()[
#             'access_token']
#         json = {"touser": touser, "msgtype": "text", "agentid": agentid, "text": {"content": "茄皇库存监控\n" + contents}}
#         resp = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", json=json)
#         print('微信推送成功' if resp.json()['errmsg'] == 'ok' else '微信推送失败')
#
#     if plustoken:
#         headers = {'Content-Type': 'application/json'}
#         json = {"token": plustoken, 'title': '茄皇库存监控', 'content': contents.replace('\n', '<br>'), "template": "json"}
#         resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
#         print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')


sign_url = 'https://apig.xiaoyisz.com/qiehuang/ga/public/api/login'
sign_headers = {
    'Host':'apig.xiaoyisz.com',
    'Content-Type':'application/json',
    'Origin':'https://thekingoftomato.ioutu.cn',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'Accept':'*/*',
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d2f) NetType/4G Language/zh_CN miniProgram/wx532ecb3bdaaf92f9',
    'Referer':'https://thekingoftomato.ioutu.cn/',
    'Content-Length':'134',
    'Accept-Language':'zh-CN,zh-Hans;q=0.9',
}
sign_data= f'{qhbody}'

re= requests.post(url=sign_url, headers=sign_headers, data=sign_data)
Authorization=json.loads(re.text)['data']

#获取时间戳和signature
Timestamp=int(round(time.time() * 1000))
signature = hashlib.md5(bytes('clientKey=IfWu0xwXlWgqkIC7DWn20qpo6a30hXX6&clientSecret=A4rHhUJfMjw2I5CODh5g40Ja1d3Yk1CH&nonce=jXsxneKFRdXPmXHi&timestamp='+f'{Timestamp}',encoding = 'utf-8')).hexdigest().upper()

#获取奖品仓库库存
gift_url = 'https://apig.xiaoyisz.com/qiehuang/ga/user/gift/list?timestamp='+f'{Timestamp}'+'&nonce=jXsxneKFRdXPmXHi&signature='+f'{signature}'
gift_headers={
    'Host':'apig.xiaoyisz.com',
    'Content-Type':'application/json',
    'Origin':'https://thekingoftomato.ioutu.cn',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'Accept':'*/*',
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d2f) NetType/4G Language/zh_CN miniProgram/wx532ecb3bdaaf92f9',
    'Authorization':f'{Authorization}',
    'Referer':'https://thekingoftomato.ioutu.cn/',
    'Accept-Language':'zh-CN,zh-Hans;q=0.9',
}
re_2= requests.get(url=gift_url, headers=gift_headers)
data= json.loads(re_2.text)['data']
#
for i in range(0, len(data)):
    message =data[i]['name']+' 库存：'+str(data[i]['leftStock'])
    print(message)

if data[2]['leftStock']+data[3]['leftStock']+data[4]['leftStock']+data[5]['leftStock']+data[6]['leftStock']+data[7]['leftStock']+data[8]['leftStock']+data[9]['leftStock']>0:
    Push(contents=message)
else:
    print('********************'+'\n'+'洗洗睡没有货，本条消息不推送！！！')

