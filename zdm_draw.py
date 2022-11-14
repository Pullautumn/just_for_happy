import requests, demjson ,re

#值得买每日转盘抽奖 位置什么值得买app-我的-值会员-每日转盘
# 推送不加了感觉没啥用
# 把值得买的cookie放入下面的单引号里面  有几个帐号就弄几个（默认设置了3个 根据自己情况改）
cookie_list = ['','','']

rewardid = 'jQuery1668392666307_1668392666307'

#获取奖品id对应名次
# rewardurl = 'https://zhiyou.smzdm.com/user/'
# rewardheaders = {
#     'Host': 'zhiyou.smzdm.com',
#     'Accept': '*/*',
#     'Connection': 'keep-alive',
#     'Cookie': cookie_list[0],
#     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/smzdm 10.4.6 rv:130.1 (iPhone 13; iOS 15.6; zh_CN)/iphone_smzdmapp/10.4.6/wkwebview/jsbv_1.0.0',
#     'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
#     'Referer': 'https://m.smzdm.com/',
#     'Accept-Encoding': 'gzip, deflate, br'
# }
# response_reward = requests.post(url=rewardurl, headers=rewardheaders).text
# a = str(response_reward).replace('jQuery1668395883990_1668395883990', '').replace('(', '').replace(')', '')
# data_1 = demjson.decode(a, encoding='utf-8')


for i in range(len(cookie_list)):
    url = f'https://zhiyou.smzdm.com/user/lottery/jsonp_draw?active_id=ljX8qVlEA7&_=1668392666307&callback={rewardid}'
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
    infoheaders = {
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
    response_info = requests.get(url=infourl, headers=infoheaders).text
    name = str(re.findall('<a href="https://zhiyou.smzdm.com/user"> (.*?) </a>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'','')
    level = str(re.findall('<img src="https://res.smzdm.com/h5/h5_user/dist/assets/level/(.*?).png\?v=1">', str(response_info), re.S)).replace('[','').replace(']','').replace('\'','')
    gold = str(re.findall('<div class="assets-part assets-gold">\n                    (.*?)</span>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'’','').replace('<span class="assets-part-element assets-num">','').replace('\'','')
    silver = str(re.findall('<div class="assets-part assets-prestige">\n                    (.*?)</span>', str(response_info), re.S)).replace('[','').replace(']','').replace('\'’','').replace('<span class="assets-part-element assets-num">','').replace('\'','')
    aa = str(response).replace(rewardid, '').replace('(', '').replace(')', '')
    data = demjson.decode(aa, encoding='utf-8')
    if data['error_code'] == 0:
        if data['data']['gift_id'] =='3591':
            print('帐号' + str(i + 1)+ ' ' + name + ' ' +'获得奖品为:2元话费券'+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
        elif data['data']['gift_id'] =='4003':
            print('帐号' + str(i + 1)+ ' ' + name + ' ' +'获得奖品为:1碎银'+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
        elif data['data']['gift_id'] =='3586':
            print('帐号' + str(i + 1)+ ' ' + name + ' ' +'获得奖品为:爱奇艺月卡'+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
        elif data['data']['gift_id'] =='4005':
            print('帐号' + str(i + 1)+ ' ' + '获得奖品为:10碎银'+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
        elif data['data']['gift_id'] =='4142':
            print('帐号' + str(i + 1)+ ' ' + name +' ' + '获得奖品为:5元京东E卡'+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
        else:
            print('帐号' + str(i + 1)+ ' ' + name + ' ' + '获得奖品为:5碎银'+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
    else:
        print('帐号' + str(i + 1)+ ' VIP'+ level +' ' + name  + ' ' +data['error_msg']+'  剩余碎银 '+silver +'  剩余金币 '+ gold)
