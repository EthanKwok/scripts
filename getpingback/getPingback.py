
# -*- coding: utf-8 -*-

# Title: getPingback
# Version: v0.1
# Last-Modified: 04-10-2014
# Author: Ethan.Guo, guozhiqiang@qiyi.com

import subprocess, re
import threading
from datetime import datetime
import sys, urllib2, json

KEYWORDS = {'albumLike': [], 'albumVideo': [], 'albumList': []}
DICT = {"t": ["日志类型", {'0': '错误信息', '1': '视频开始播放', 
                           '2': '播放计时', '3': 'App启动',
                           '5': '搜索，检索点击或用户行为', '8': '卡顿',
                           '9': '资源请求', '10': '环境信息报告',
                           '11': '自定义：广告相关', '13': '视频播放结束',
                           '14': 'App退出', '15': '播放器初始化',
                           '16': '鉴权', '17': '用户退出播放',
                           '20': '页面点击', 'None': '未提供log类型',

                           'show': '推荐结果展示', 'userclick': '推荐结果点击',
                           'ctplay': '推荐结果连播'}],

        "s1": ["一级来源", {"0": "设备鉴权，App启动，环境信息，App退出等",
                            "1": "渠道站内", "2": "渠道站外"}], 

        "c1": ["一级频道ID", {"1": "电影", "2": "电视剧", "3": "纪录片", "4": "动漫",
                              "5": "音乐", "6": "综艺", "7": "娱乐", "8": "游戏",
                              "9": "旅游", "10": "片花", "11": "公开课", "12": "教育",
                              "13": "时尚", "14": "时尚综艺", "15": "少儿综艺", "16": "微电影",
                              "17": "体育", "18": "奥运", "19": "直播", "20": "广告", "21": "生活",
                              "22": "搞笑", "23": "奇葩"}], 

        "s2": ["二级来源", {"3": "搜索", "detailrec": "详情页猜你喜欢", "playrec": "播放页猜你喜欢",
                            "endrec": "结束页猜你喜欢", "8": "播放记录", "phone": "手机推片", 
                            "7new": "7日最新", "channel": "频道页", "ep_player": "播放页剧集列表",
                            "favorite": "收藏", "continue": "多剧集连续播放", "hookup": "短视频联播",
                            "replay": "重播", "window": "小窗口播放", "out_homerec": "外部首页推荐",
                            "osearch": "外部搜索", "vsearch": "语音搜索", "weekend": "周末影院", "offline": "离线下载"}],

        "r": ["资源ID", {"00001": "首页", "00002": "搜索页键盘", "00003": "标签列表", "00005": "升级弹窗"}],

        "a": ["用户行为", {"mpconnect": "手机连接", "mpcontrol": "手机遥控", "tvclkrec": "推荐位点击", "tvclktag": "标签点击",
                           "tvclksrchplpename": "搜人名", "tvclksrchtvname": "搜片名", "tvpageturn": "翻页",
                           "tvclkepisode": "剧集列表点击", "tvclkfeedback": "意见反馈点击", "tvclkupdate": "立即升级", "tvclkabc": "搜索首字点击",
                           "tvclknexttm": "升级稍后询问", "tvclkexitapp": "退出程序", "3": "拖拽进度", "tvclkoffline": "离线下载"}], 

        "tvtag": ["标签识别", {"robo": "热播", "happing": "好评", "search": "搜索", "0": "最近更新中的全部"}], 

        "rpage": ["页面标识", {"rec": "首页推荐Tab", "channel": "首页频道Tab", "special": "首页专题Tab", "mine": "首页我的Tab", 
                               "search": "首页搜索Tab", "7new": "最新更新", "history": "播放记录", 
                               "fav": "收藏", "vip": "会员专区"}], 

        "block": ["功能区块标识", {"rec": "首页推荐Tab", "channel": "首页频道Tab", "special": "首页专题Tab", "mine": "首页我的Tab", "search": "首页搜索Tab"}], 

        "rseat": ["位置信息", {"7new": "推荐Tab最新更新", "search": "搜索按钮或搜索框", "history": "推荐Tab播放记录", "weekend": "推荐Tab周末影院", "fav": "我的收藏", 
                               "account": "我的账号", "feedback": "意见反馈", "vip": "会员专区", "multiscreen": "多屏互动", "contact": "联系我们"}],

        "ct": ["自定义", {"adstart": "广告开始播放", "adend": "广告播放结束"}],

        "ptype": ["ptype", {"1": "点击三级标签按钮", "2": "点击排序按钮", "3": "点击筛选出来的结果", "1-1": "通过热词进入结果", "1-2": "通过suggest进入结果"}],

        "usract": ["usract", {'show': '推荐结果展示', 'userclick': '推荐结果点击', 'ctplay': '推荐结果连播'}],

        "pf": "一级平台", "p": "二级平台", "p1": "一级产品", "e": "事件ID", "u": "Mac地址", 
        "rn": "随机数", "nu": "是否新用户", "v": "客户端版本", "dt": "UUID", "pu": "用户ID", "ra": "视频播放码流", "cp": "内容提供方", "pr": "集成平台tvid",
        "tvchl": "集成平台频道ID", "re": "分辨率", "os": "操作系统版本", "firmver": "固件版本", "hwver": "硬件型号", "se": "来源事件ID", "tm": "时间长度", 
        "ec": "错误码", "rt": "资源类型", "ri": "资源接口", "td": "延迟", "ps": "观看进度", "st": "鉴权状态", "pfec": "平台错误码", "tvepin": "剧集集数", 
        "tvfbbtn": "意见反馈按钮", "errurl": "出错URL", "userip": "用户IP", "dispip": "用户访问调度器IP", "from": "拖拽开始时间", "to": "拖拽结束时间", 
        "qy_prv": "是否试看",  "type": "推荐相关",

        "ppuid": "用户ID", "uid": "Mac地址", "uuid":"UUID"}

def getTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getConnection():
    ip = raw_input("请输入连接设备的IP地址然后按回车键继续".decode("utf-8").encode("gbk") + "\n\r") #TODO: Invalid IP address
    if not ip.strip():
        print "未提供IP地址，工具即将退出".decode("utf-8").encode("gbk")
        sys.exit()
    p = subprocess.Popen(("adb connect %s" %(ip)).split(), shell=False, stdin=subprocess.PIPE)
    p.communicate("\n")

def clearBuffer():
    p = subprocess.Popen("adb logcat -c".split(), shell=False)

def getLogType(str):
    if 'type=recctplay20121226' not in str:
        m = re.search(r"(&){0,1}(t=){1}[0-9]{0,2}(&){0,1}", str)   
    else:
        m = re.search(r"(&){0,1}(usract=){1}[a-zA-Z]*(&){0,1}", str)
    if not m:
        return DICT["t"][1]['None']
    key = m.group().replace("&", "").split("=")[1]
    if key not in DICT["t"][1]:
        return DICT["t"][1]['None']
    else:
        return DICT["t"][1][key]

MATCH = {'r': ['vrsTvId', 'vrsAlbumId'], 'pr': ['tvId']}

def getAlbumName(out):
    global KEYWORDS
    key = MATCH[out[0]]
    for values in KEYWORDS.values():
        for value in values:
            for v in value:
                for k in key:
                    if k not in v.keys():
                        continue
                    if str(v[k]) == out[1]:
                        if v.get('title', ""):
                            return v.get('title', "") + "(" + out[1] + ")"
                        return v.get('albumName', "") + "(" + out[1] + ")"          
    return out[1]

def parseOutput(output):
    for out in output:
        out = out.split("=")
        if out[0] in ["r", "pr"]:
            out[1] = getAlbumName(out)
        if not out[0] in DICT.keys():
            print "%s:  %23s = %s" %(getTime(), out[0], out[1])
        elif type(DICT[out[0]]) is str:
            print "%s:  %23s = %s" %(getTime(), (DICT[out[0]].decode('utf-8').encode('gbk') + "(" + out[0] + ")"), out[1].encode('gbk'))
        else:
            if out[1] not in DICT[out[0]][1]:
                print "%s:  %23s = %s" %(getTime(), (DICT[out[0]][0].decode('utf-8').encode("gbk") + "(" + out[0] + ")"), out[1].encode('gbk'))
            else:    
                print "%s:  %23s = %s" %(getTime(), (DICT[out[0]][0].decode('utf-8').encode("gbk") + "(" + out[0] + ")"), (DICT[out[0]][1][out[1]].decode('utf-8').encode("gbk") + "(" + out[1] + ")"))

def processPingback():
    for i in range(3):
        print "="*60
    p = subprocess.Popen("adb logcat -v time BasePingbackApi:V *:S".split(), shell=False, stdout=subprocess.PIPE)
    while True:
        output = p.stdout.readline().strip()
        if "?" in output:
            print "%20s" %(getLogType(output).decode("utf-8").encode("gbk"))
            parseOutput(output.split("?")[1].split("&"))
            print "="*60

def fetchVideoInfo():
    global KEYWORDS
    p = subprocess.Popen("adb logcat -v time System.out:V *:S".split(), shell=False, stdout=subprocess.PIPE)
    while True:
        output = p.stdout.readline().strip()
        for key in KEYWORDS.keys():
            if key in output:
                m = re.search((r"(http://data.itv.iqiyi.com/itv/){1}(%s){1}(.)*$" %(key)), output)
                if not m: break
                try:
                    url = m.group()
                    socket = urllib2.urlopen(url)
                except urllib2.URLError:
                    print "URLError: error happens when requesting the URL: %s" %(url)
                    break
                if socket and socket.code == 200:
                    if len(KEYWORDS[key]) == 4:
                        KEYWORDS[key].pop(0)    
                    KEYWORDS[key].append(json.loads(socket.readlines()[0])['data'])
                    socket.close()
                    break
                socket.close()

def startThreading():
    tFetchVideoInfo = threading.Thread(target=fetchVideoInfo, name="Thread_FetchVideoInfo", args=())
    tProcessPingback = threading.Thread(target=processPingback, name="Thread_ProcessPingback", args=())
    tFetchVideoInfo.start()  #Todo: A user friendly way to exit
    tProcessPingback.start()

if __name__ == "__main__":
    getConnection()
    clearBuffer()
    startThreading()
