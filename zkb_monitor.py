import requests, json, re, urllib3, xlwt,datetime
from bs4 import BeautifulSoup as bs

# 配置新赚吧cookie 单引号里面填帆软网页的cookie就可以了
cookie = ''
#监控关键词
keywords =['有水','BUG','bug','中信','交行','快']

# 企业微信推送参数
corpid = ''
agentid = ''
corpsecret = ''
touser = ''
# 推送加 token
plustoken = ''

urllib3.disable_warnings()

url = 'http://www.zuanke8.com/forum-15-1.html'
headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'host': 'www.zuanke8.com',
    'cookie': f'{cookie}',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
response = requests.get(url=url, headers=headers, verify=False)
soup = bs(response.text, "lxml")
# print(soup)
pro_str = soup.find_all('a', class_='s xst')
pro_str2 = soup.find_all('span',class_="xi1")
#置顶有几个
alist = []
for a in range(len(pro_str)):
    a = "".join(re.findall('<a class="s xst" href="(.*?)" style="font-weight', str(pro_str[a]), re.S))
    if len(a)>0:
        alist.append(a)

project_list = []
for i in range(len(pro_str2)):
    link = "".join(re.findall('<a class="s xst" href="(.*?)" target="_blank">', str(pro_str[i+len(alist)]), re.S)) #去掉置顶消息
    title = "".join(re.findall('" target="_blank">(.*?)</a>', str(pro_str[i+len(alist)]), re.S))
    time = "".join(re.findall('<span class="xi1">(.*?)</span>', str(pro_str2[i]), re.S))
    project = {
        'title': title,
        'link': link,
        'time': time
    }
    project_list.append(project)

new_list = sorted(project_list, key=lambda x: x['time'],reverse=True)
print(new_list)
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
for k in range(len(keywords)):
    for j in range(len(new_list)):
        result_match = re.findall(keywords[k], str(new_list[j]['title']))
        if new_list[j]['time'] == str(nowtime) and len(result_match)>0:
            push_title = new_list[j]['title']
            push_url = new_list[j]['link']
            print(new_list[j])
            response2 = requests.get(url=push_url, headers=headers, verify=False)
            soup2 = bs(response2.text, "lxml")
            message= str(soup2.find_all('td',class_="t_f")).replace('[','').replace(']','')
            print(message)
            def Push(contents):
                # 微信推送
                if all([corpid, agentid, corpsecret, touser]):
                    token = \
                        requests.get(
                            f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}').json()[
                            'access_token']
                    json = {"touser": touser, "msgtype": "text", "agentid": agentid,
                            "text": {"content": f"{push_title}" + contents}}
                    resp = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}",
                                         json=json)
                    print('微信推送成功' if resp.json()['errmsg'] == 'ok' else '微信推送失败')

                if plustoken:
                    headers = {'Content-Type': 'application/json'}
                    json = {"token": plustoken, 'title': f'{push_title}', 'content': contents.replace('\n', '<br>'),
                            "template": "json"}
                    resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
                    print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')
            Push(contents=message)
