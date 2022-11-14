import requests, demjson ,re,time,json

# 推送不加了感觉没啥用
# 把值得买的cookie放入下面的单引号里面  有几个帐号就弄几个（默认设置了3个 根据自己情况改）
cookie_list = ['','','']
# 活动id
active_id = ['ljX8qVlEA7','daY8jaOgOo']


for i in range(len(cookie_list)):
    for a in range(len(active_id)):
        projectList = []
        url = f'https://zhiyou.smzdm.com/user/lottery/jsonp_draw?active_id={active_id[a]}'
        rewardurl= f'https://zhiyou.smzdm.com/user/lottery/jsonp_get_active_info?active_id={active_id[a]}'
        infourl = 'https://zhiyou.smzdm.com/user/'
        headers = {
            'Host': 'zhiyou.smzdm.com',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Cookie': cookie_list[i],
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/smzdm 10.4.6 rv:130.1 (iPhone 13; iOS 15.6; zh_CN)/iphone_smzdmapp/10.4.6/wkwebview/jsbv_1.0.0',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Referer': 'https://m.smzdm.com/',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        response = requests.post(url=url, headers=headers).text
        response_info = requests.get(url=infourl, headers=headers).text
        response_reward = requests.get(url=rewardurl, headers=headers)
        result_reward = json.loads(response_reward.text)
        name = str(re.findall('<a href="https://zhiyou.smzdm.com/user"> (.*?) </a>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'','')
        level = str(re.findall('<img src="https://res.smzdm.com/h5/h5_user/dist/assets/level/(.*?).png\?v=1">', str(response_info), re.S)).replace('[','').replace(']','').replace('\'','')
        gold = str(re.findall('<div class="assets-part assets-gold">\n                    (.*?)</span>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'’','').replace('<span class="assets-part-element assets-num">','').replace('\'','')
        silver = str(re.findall('<div class="assets-part assets-prestige">\n                    (.*?)</span>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'’','').replace('<span class="assets-part-element assets-num">','').replace('\'','')
        data = demjson.decode(str(response), encoding='utf-8')
        print('帐号' + str(i + 1)+ ' VIP'+ level + ' ' + name + ' ' + data['error_msg']+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
        time.sleep(2)
