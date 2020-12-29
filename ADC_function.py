import requests
from lxml import etree
import re
import config

SUPPORT_PROXY_TYPE = ("http", "socks5", "socks5h")

def get_data_state(data: dict) -> bool:  # 元数据获取失败检测
    if "title" not in data or "number" not in data:
        return False

    if data["title"] is None or data["title"] == "" or data["title"] == "null":
        return False

    if data["number"] is None or data["number"] == "" or data["number"] == "null":
        return False

    return True


def getXpathSingle(htmlcode,xpath):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result1 = str(html.xpath(xpath)).strip(" ['']")
    return result1


def get_proxy(proxy: str, proxytype: str = None) -> dict:
    ''' 获得代理参数，默认http代理
    '''
    if proxy:
        if proxytype in SUPPORT_PROXY_TYPE:
            proxies = {"http": proxytype + "://" + proxy, "https": proxytype + "://" + proxy}
        else:
            proxies = {"http": "http://" + proxy, "https": "https://" + proxy}
    else:
        proxies = {}

    return proxies


# 网页请求核心
def get_html(url, cookies: dict = None, ua: str = None, return_type: str = None):
    switch, proxy, timeout, retry_count, proxytype = config.Config().proxy()
    proxies = get_proxy(proxy, proxytype)

    if ua is None:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"} # noqa
    else:
        headers = {"User-Agent": ua}

    for i in range(retry_count):
        try:
            if switch == '1' or switch == 1:
                result = requests.get(str(url), headers=headers, timeout=timeout, proxies=proxies, cookies=cookies)
            else:
                result = requests.get(str(url), headers=headers, timeout=timeout, cookies=cookies)

            result.encoding = "utf-8"

            if return_type == "object":
                return result
            else:
                return result.text

        except Exception as e:
            print("[-]Connect retry {}/{}".format(i + 1, retry_count))
            print("[-]" + str(e))
    print('[-]Connect Failed! Please check your Proxy or Network!')


def post_html(url: str, query: dict) -> requests.Response:
    switch, proxy, timeout, retry_count, proxytype = config.Config().proxy()
    proxies = get_proxy(proxy, proxytype)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"}

    for i in range(retry_count):
        try:
            if switch == 1 or switch == '1':
                result = requests.post(url, data=query, proxies=proxies,headers=headers, timeout=timeout)
            else:
                result = requests.post(url, data=query, headers=headers, timeout=timeout)
            return result
        except requests.exceptions.ProxyError:
            print("[-]Connect retry {}/{}".format(i+1, retry_count))
    print("[-]Connect Failed! Please check your Proxy or Network!")


def get_javlib_cookie() -> [dict, str]:
    import cloudscraper
    switch, proxy, timeout, retry_count, proxytype = config.Config().proxy()
    proxies = get_proxy(proxy, proxytype)

    raw_cookie = {}
    user_agent = ""

    # Get __cfduid/cf_clearance and user-agent
    for i in range(retry_count):
        try:
            if switch == 1 or switch == '1':
                raw_cookie, user_agent = cloudscraper.get_cookie_string(
                    "http://www.m45e.com/",
                    proxies=proxies
                )
            else:
                raw_cookie, user_agent = cloudscraper.get_cookie_string(
                    "http://www.m45e.com/"
                )
        except requests.exceptions.ProxyError:
            print("[-] ProxyError, retry {}/{}".format(i+1, retry_count))
        except cloudscraper.exceptions.CloudflareIUAMError:
            print("[-] IUAMError, retry {}/{}".format(i+1, retry_count))

    return raw_cookie, user_agent

def translateTag_to_sc(tag):
    tranlate_to_sc = config.Config().transalte_to_sc()
    if tranlate_to_sc:
        dict_gen = {'中文字幕': '中文字幕',
                    '高清': 'XXXX', '字幕': 'XXXX', '推薦作品': '推荐作品', '通姦': '通奸', '淋浴': '淋浴', '舌頭': '舌头',
                    '下流': '下流', '敏感': '敏感', '變態': '变态', '願望': '愿望', '慾求不滿': '慾求不满', '服侍': '服侍',
                    '外遇': '外遇', '訪問': '访问', '性伴侶': '性伴侣', '保守': '保守', '購物': '购物', '誘惑': '诱惑',
                    '出差': '出差', '煩惱': '烦恼', '主動': '主动', '再會': '再会', '戀物癖': '恋物癖', '問題': '问题',
                    '騙奸': '骗奸', '鬼混': '鬼混', '高手': '高手', '順從': '顺从', '密會': '密会', '做家務': '做家务',
                    '秘密': '秘密', '送貨上門': '送货上门', '壓力': '压力', '處女作': '处女作', '淫語': '淫语', '問卷': '问卷',
                    '住一宿': '住一宿', '眼淚': '眼泪', '跪求': '跪求', '求職': '求职', '婚禮': '婚礼', '第一視角': '第一视角',
                    '洗澡': '洗澡', '首次': '首次', '劇情': '剧情', '約會': '约会', '實拍': '实拍', '同性戀': '同性恋',
                    '幻想': '幻想', '淫蕩': '淫荡', '旅行': '旅行', '面試': '面试', '喝酒': '喝酒', '尖叫': '尖叫',
                    '新年': '新年', '借款': '借款', '不忠': '不忠', '檢查': '检查', '羞恥': '羞耻', '勾引': '勾引',
                    '新人': '新人', '推銷': '推销', 'ブルマ': '运动短裤',

                    'AV女優': 'AV女优', '情人': '情人', '丈夫': '丈夫', '辣妹': '辣妹', 'S級女優': 'S级女优', '白領': '白领',
                    '偶像': '偶像', '兒子': '儿子', '女僕': '女仆', '老師': '老师', '夫婦': '夫妇', '保健室': '保健室',
                    '朋友': '朋友', '工作人員': '工作人员', '明星': '明星', '同事': '同事', '面具男': '面具男', '上司': '上司',
                    '睡眠系': '睡眠系', '奶奶': '奶奶', '播音員': '播音员', '鄰居': '邻居', '親人': '亲人', '店員': '店员',
                    '魔女': '魔女', '視訊小姐': '视讯小姐', '大學生': '大学生', '寡婦': '寡妇', '小姐': '小姐', '秘書': '秘书',
                    '人妖': '人妖', '啦啦隊': '啦啦队', '美容師': '美容师', '岳母': '岳母', '警察': '警察', '熟女': '熟女',
                    '素人': '素人', '人妻': '人妻', '痴女': '痴女', '角色扮演': '角色扮演', '蘿莉': '萝莉', '姐姐': '姐姐',
                    '模特': '模特', '教師': '教师', '學生': '学生', '少女': '少女', '新手': '新手', '男友': '男友',
                    '護士': '护士', '媽媽': '妈妈', '主婦': '主妇', '孕婦': '孕妇', '女教師': '女教师', '年輕人妻': '年轻人妻',
                    '職員': '职员', '看護': '看护', '外觀相似': '外观相似', '色狼': '色狼', '醫生': '医生', '新婚': '新婚',
                    '黑人': '黑人', '空中小姐': '空中小姐', '運動系': '运动系', '女王': '女王', '西裝': '西装', '旗袍': '旗袍',
                    '兔女郎': '兔女郎', '白人': '白人',

                    '制服': '制服', '內衣': '内衣', '休閒裝': '休閒装', '水手服': '水手服', '全裸': '全裸', '不穿內褲': '不穿内裤',
                    '和服': '和服', '不戴胸罩': '不戴胸罩', '連衣裙': '连衣裙', '打底褲': '打底裤', '緊身衣': '紧身衣', '客人': '客人',
                    '晚禮服': '晚礼服', '治癒系': '治癒系', '大衣': '大衣', '裸體襪子': '裸体袜子', '絲帶': '丝带', '睡衣': '睡衣',
                    '面具': '面具', '牛仔褲': '牛仔裤', '喪服': '丧服', '極小比基尼': '极小比基尼', '混血': '混血', '毛衣': '毛衣',
                    '頸鏈': '颈链', '短褲': '短裤', '美人': '美人', '連褲襪': '连裤袜', '裙子': '裙子', '浴衣和服': '浴衣和服',
                    '泳衣': '泳衣', '網襪': '网袜', '眼罩': '眼罩', '圍裙': '围裙', '比基尼': '比基尼', '情趣內衣': '情趣内衣',
                    '迷你裙': '迷你裙', '套裝': '套装', '眼鏡': '眼镜', '丁字褲': '丁字裤', '陽具腰帶': '阳具腰带', '男装': '男装',
                    '襪': '袜',

                    '美肌': '美肌', '屁股': '屁股', '美穴': '美穴', '黑髮': '黑发', '嬌小': '娇小', '曬痕': '晒痕',
                    'F罩杯': 'F罩杯', 'E罩杯': 'E罩杯', 'D罩杯': 'D罩杯', '素顏': '素颜', '貓眼': '猫眼', '捲髮': '捲发',
                    '虎牙': '虎牙', 'C罩杯': 'C罩杯', 'I罩杯': 'I罩杯', '小麥色': '小麦色', '大陰蒂': '大阴蒂', '美乳': '美乳',
                    '巨乳': '巨乳', '豐滿': '丰满', '苗條': '苗条', '美臀': '美臀', '美腿': '美腿', '無毛': '无毛',
                    '美白': '美白', '微乳': '微乳', '性感': '性感', '高個子': '高个子', '爆乳': '爆乳', 'G罩杯': 'G罩杯',
                    '多毛': '多毛', '巨臀': '巨臀', '軟體': '软体', '巨大陽具': '巨大阳具', '長發': '长发', 'H罩杯': 'H罩杯',

                    '舔陰': '舔阴', '電動陽具': '电动阳具', '淫亂': '淫乱', '射在外陰': '射在外阴', '猛烈': '猛烈', '後入內射': '后入内射',
                    '足交': '足交', '射在胸部': '射在胸部', '側位內射': '侧位内射', '射在腹部': '射在腹部', '騎乘內射': '骑乘内射', '射在頭髮': '射在头发',
                    '母乳': '母乳', '站立姿勢': '站立姿势', '肛射': '肛射', '陰道擴張': '阴道扩张', '內射觀察': '内射观察', '射在大腿': '射在大腿',
                    '精液流出': '精液流出', '射在屁股': '射在屁股', '內射潮吹': '内射潮吹', '首次肛交': '首次肛交', '射在衣服上': '射在衣服上', '首次內射': '首次内射',
                    '早洩': '早洩', '翻白眼': '翻白眼', '舔腳': '舔脚', '喝尿': '喝尿', '口交': '口交', '內射': '内射',
                    '自慰': '自慰', '後入': '后入', '騎乘位': '骑乘位', '顏射': '颜射', '口內射精': '口内射精', '手淫': '手淫',
                    '潮吹': '潮吹', '輪姦': '轮奸', '亂交': '乱交', '乳交': '乳交', '小便': '小便', '吸精': '吸精',
                    '深膚色': '深肤色', '指法': '指法', '騎在臉上': '骑在脸上', '連續內射': '连续内射', '打樁機': '打桩机', '肛交': '肛交',
                    '吞精': '吞精', '鴨嘴': '鸭嘴', '打飛機': '打飞机', '剃毛': '剃毛', '站立位': '站立位', '高潮': '高潮',
                    '二穴同入': '二穴同入', '舔肛': '舔肛', '多人口交': '多人口交', '痙攣': '痉挛', '玩弄肛門': '玩弄肛门', '立即口交': '立即口交',
                    '舔蛋蛋': '舔蛋蛋', '口射': '口射', '陰屁': '阴屁', '失禁': '失禁', '大量潮吹': '大量潮吹', '69': '69',

                    '振動': '振动', '搭訕': '搭讪', '奴役': '奴役', '打屁股': '打屁股', '潤滑油': '润滑油',
                    '按摩': '按摩', '散步': '散步', '扯破連褲襪': '扯破连裤袜', '手銬': '手铐', '束縛': '束缚', '調教': '调教',
                    '假陽具': '假阳具', '變態遊戲': '变态游戏', '注視': '注视', '蠟燭': '蜡烛', '電鑽': '电钻', '亂搞': '乱搞',
                    '摩擦': '摩擦', '項圈': '项圈', '繩子': '绳子', '灌腸': '灌肠', '監禁': '监禁', '車震': '车震',
                    '鞭打': '鞭打', '懸掛': '悬挂', '喝口水': '喝口水', '精液塗抹': '精液涂抹', '舔耳朵': '舔耳朵', '女體盛': '女体盛',
                    '便利店': '便利店', '插兩根': '插两根', '開口器': '开口器', '暴露': '暴露', '陰道放入食物': '阴道放入食物', '大便': '大便',
                    '經期': '经期', '惡作劇': '恶作剧', '電動按摩器': '电动按摩器', '凌辱': '凌辱', '玩具': '玩具', '露出': '露出',
                    '肛門': '肛门', '拘束': '拘束', '多P': '多P', '潤滑劑': '润滑剂', '攝影': '摄影', '野外': '野外',
                    '陰道觀察': '阴道观察', 'SM': 'SM', '灌入精液': '灌入精液', '受虐': '受虐', '綁縛': '绑缚', '偷拍': '偷拍',
                    '異物插入': '异物插入', '電話': '电话', '公寓': '公寓', '遠程操作': '远程操作', '偷窺': '偷窥', '踩踏': '踩踏',
                    '無套': '无套',

                    '企劃物': '企划物', '獨佔動畫': '独佔动画', '10代': '10代', '1080p': 'XXXX', '人氣系列': '人气系列', '60fps': 'XXXX',
                    '超VIP': '超VIP', '投稿': '投稿', 'VIP': 'VIP', '椅子': '椅子', '風格出眾': '风格出众', '首次作品': '首次作品',
                    '更衣室': '更衣室', '下午': '下午', 'KTV': 'KTV', '白天': '白天', '最佳合集': '最佳合集', 'VR': 'VR',
                    '動漫': '动漫',

                    '酒店': '酒店', '密室': '密室', '車': '车', '床': '床', '陽台': '阳台', '公園': '公园',
                    '家中': '家中', '公交車': '公交车', '公司': '公司', '門口': '门口', '附近': '附近', '學校': '学校',
                    '辦公室': '办公室', '樓梯': '楼梯', '住宅': '住宅', '公共廁所': '公共厕所', '旅館': '旅馆', '教室': '教室',
                    '廚房': '厨房', '桌子': '桌子', '大街': '大街', '農村': '农村', '和室': '和室', '地下室': '地下室',
                    '牢籠': '牢笼', '屋頂': '屋顶', '游泳池': '游泳池', '電梯': '电梯', '拍攝現場': '拍摄现场', '別墅': '别墅',
                    '房間': '房间', '愛情旅館': '爱情旅馆', '車內': '车内', '沙發': '沙发', '浴室': '浴室', '廁所': '厕所',
                    '溫泉': '温泉', '醫院': '医院', '榻榻米': '榻榻米',

                    '中文字幕': '中文字幕', '无码流出': '无码流出',
                    '折磨': '折磨', '嘔吐': '呕吐', '觸手': '触手', '蠻橫嬌羞': '蛮横娇羞', '處男': '处男', '正太控': '正太控',
                    '出軌': '出轨', '瘙癢': '瘙痒', '運動': '运动', '女同接吻': '女同接吻', '性感的x': '性感的', '美容院': '美容院',
                    '處女': '处女', '爛醉如泥的': '烂醉如泥的', '殘忍畫面': '残忍画面', '妄想': '妄想', '惡作劇': '恶作剧', '學校作品': '学校作品',
                    '粗暴': '粗暴', '通姦': '通奸', '姐妹': '姐妹', '雙性人': '双性人', '跳舞': '跳舞', '性奴': '性奴',
                    '倒追': '倒追', '性騷擾': '性骚扰', '其他': '其他', '戀腿癖': '恋腿癖', '偷窥': '偷窥', '花癡': '花痴',
                    '男同性恋': '男同性恋', '情侶': '情侣', '戀乳癖': '恋乳癖', '亂倫': '乱伦', '其他戀物癖': '其他恋物癖', '偶像藝人': '偶像艺人',
                    '野外・露出': '野外・露出', '獵豔': '猎艳', '女同性戀': '女同性恋', '企畫': '企画', '10枚組': '10枚组', '性感的': '性感的',
                    '科幻': '科幻', '女優ベスト・総集編': '演员的总编', '温泉': '温泉', 'M男': 'M男', '原作コラボ': '原作协作',
                    '16時間以上作品': '16时间以上作品', 'デカチン・巨根': '巨根', 'ファン感謝・訪問': '感恩祭', '動画': '动画', '巨尻': '巨尻', 'ハーレム': '后宫',
                    '日焼け': '晒黑', '早漏': '早漏', 'キス・接吻': '接吻.', '汗だく': '汗流浃背', 'スマホ専用縦動画': '智能手机的垂直视频', 'Vシネマ': '电影放映',
                    'Don Cipote\'s choice': 'Don Cipote\'s choice', 'アニメ': '日本动漫', 'アクション': '动作',
                    'イメージビデオ（男性）': '（视频）男性',
                    '孕ませ': '孕育', 'ボーイズラブ': '男孩恋爱',
                    'ビッチ': 'bitch', '特典あり（AVベースボール）': '特典（AV棒球）', 'コミック雑誌': '漫画雑志', '時間停止': '时间停止',

                    '黑幫成員': '黑帮成员', '童年朋友': '童年朋友', '公主': '公主', '亞洲女演員': '亚洲女演员', '伴侶': '伴侣', '講師': '讲师',
                    '婆婆': '婆婆', '格鬥家': '格斗家', '女檢察官': '女检察官', '明星臉': '明星脸', '女主人、女老板': '女主人、女老板', '模特兒': '模特',
                    '秘書': '秘书', '美少女': '美少女', '新娘、年輕妻子': '新娘、年轻妻子', '姐姐': '姐姐', '車掌小姐': '车掌小姐',
                    '寡婦': '寡妇', '千金小姐': '千金小姐', '白人': '白人', '已婚婦女': '已婚妇女', '女醫生': '女医生', '各種職業': '各种职业',
                    '妓女': '妓女', '賽車女郎': '赛车女郎', '女大學生': '女大学生', '展場女孩': '展场女孩', '女教師': '女教师', '母親': '母亲',
                    '家教': '家教', '护士': '护士', '蕩婦': '荡妇', '黑人演員': '黑人演员', '女生': '女生', '女主播': '女主播',
                    '高中女生': '高中女生', '服務生': '服务生', '魔法少女': '魔法少女', '學生（其他）': '学生（其他）', '動畫人物': '动画人物', '遊戲的真人版': '游戏真人版',
                    '超級女英雄': '超级女英雄',

                    '角色扮演': '角色扮演', '制服': '制服', '女戰士': '女战士', '及膝襪': '及膝袜', '娃娃': '娃娃', '女忍者': '女忍者',
                    '女裝人妖': '女装人妖', '內衣': '內衣', '猥褻穿著': '猥亵穿着', '兔女郎': '兔女郎', '貓耳女': '猫耳女', '女祭司': '女祭司',
                    '泡泡襪': '泡泡袜', '緊身衣': '紧身衣', '裸體圍裙': '裸体围裙', '迷你裙警察': '迷你裙警察', '空中小姐': '空中小姐',
                    '連褲襪': '连裤袜', '身體意識': '身体意识', 'OL': 'OL', '和服・喪服': '和服・丧服', '體育服': '体育服', '内衣': '内衣',
                    '水手服': '水手服', '學校泳裝': '学校泳装', '旗袍': '旗袍', '女傭': '女佣', '迷你裙': '迷你裙', '校服': '校服',
                    '泳裝': '泳装', '眼鏡': '眼镜', '哥德蘿莉': '哥德萝莉', '和服・浴衣': '和服・浴衣',

                    '超乳': '超乳', '肌肉': '肌肉', '乳房': '乳房', '嬌小的': '娇小的', '屁股': '屁股', '高': '高',
                    '變性者': '变性人', '無毛': '无毛', '胖女人': '胖女人', '苗條': '苗条', '孕婦': '孕妇', '成熟的女人': '成熟的女人',
                    '蘿莉塔': '萝莉塔', '貧乳・微乳': '贫乳・微乳', '巨乳': '巨乳',

                    '顏面騎乘': '颜面骑乘', '食糞': '食粪', '足交': '足交', '母乳': '母乳', '手指插入': '手指插入', '按摩': '按摩',
                    '女上位': '女上位', '舔陰': '舔阴', '拳交': '拳交', '深喉': '深喉', '69': '69', '淫語': '淫语',
                    '潮吹': '潮吹', '乳交': '乳交', '排便': '排便', '飲尿': '饮尿', '口交': '口交', '濫交': '滥交',
                    '放尿': '放尿', '打手槍': '打手枪', '吞精': '吞精', '肛交': '肛交', '顏射': '颜射', '自慰': '自慰',
                    '顏射x': '颜射', '中出': '中出', '肛内中出': '肛内中出',

                    '立即口交': '立即口交', '女優按摩棒': '演员按摩棒', '子宮頸': '子宫颈', '催眠': '催眠', '乳液': '乳液', '羞恥': '羞耻',
                    '凌辱': '凌辱', '拘束': '拘束', '輪姦': '轮奸', '插入異物': '插入异物', '鴨嘴': '鸭嘴', '灌腸': '灌肠',
                    '監禁': '监禁', '紧缚': '紧缚', '強姦': '强奸', '藥物': '药物', '汽車性愛': '汽车性爱', 'SM': 'SM',
                    '糞便': '粪便', '玩具': '玩具', '跳蛋': '跳蛋', '緊縛': '紧缚', '按摩棒': '按摩棒', '多P': '多P',
                    '性愛': '性爱', '假陽具': '假阳具', '逆強姦': '逆强奸',

                    '合作作品': '合作作品', '恐怖': '恐怖', '給女性觀眾': '女性向', '教學': '教学', 'DMM專屬': 'DMM专属', 'R-15': 'R-15',
                    'R-18': 'R-18', '戲劇': '戏剧', '3D': '3D', '特效': '特效', '故事集': '故事集', '限時降價': '限时降价',
                    '複刻版': '复刻版', '戲劇x': '戏剧', '戀愛': '恋爱', '高畫質': 'xxx', '主觀視角': '主观视角', '介紹影片': '介绍影片',
                    '4小時以上作品': '4小时以上作品', '薄馬賽克': '薄马赛克', '經典': '经典', '首次亮相': '首次亮相', '數位馬賽克': '数位马赛克', '投稿': '投稿',
                    '纪录片': '纪录片', '國外進口': '国外进口', '第一人稱攝影': '第一人称摄影', '業餘': '业余', '局部特寫': '局部特写', '獨立製作': '独立制作',
                    'DMM獨家': 'DMM独家', '單體作品': '单体作品', '合集': '合集', '高清': 'xxx', '字幕': 'xxx', '天堂TV': '天堂TV',
                    'DVD多士爐': 'DVD多士炉', 'AV OPEN 2014 スーパーヘビー': 'AV OPEN 2014 S级',
                    'AV OPEN 2014 ヘビー級': 'AV OPEN 2014重量级',
                    'AV OPEN 2014 ミドル級': 'AV OPEN 2014中量级',
                    'AV OPEN 2015 マニア/フェチ部門': 'AV OPEN 2015 狂热者/恋物癖部门', 'AV OPEN 2015 熟女部門': 'AV OPEN 2015 熟女部门',
                    'AV OPEN 2015 企画部門': 'AV OPEN 2015 企画部门', 'AV OPEN 2015 乙女部門': 'AV OPEN 2015 少女部',
                    'AV OPEN 2015 素人部門': 'AV OPEN 2015 素人部门', 'AV OPEN 2015 SM/ハード部門': 'AV OPEN 2015 SM/硬件',
                    'AV OPEN 2015 女優部門': 'AV OPEN 2015 演员部门', 'AVOPEN2016人妻・熟女部門': 'AVOPEN2016人妻・熟女部门',
                    'AVOPEN2016企画部門': 'AVOPEN2016企画部', 'AVOPEN2016ハード部門': 'AVOPEN2016ハード部',
                    'AVOPEN2016マニア・フェチ部門': 'AVOPEN2016疯狂恋物科', 'AVOPEN2016乙女部門': 'AVOPEN2016少女部',
                    'AVOPEN2016女優部門': 'AVOPEN2016演员部', 'AVOPEN2016ドラマ・ドキュメンタリー部門': 'AVOPEN2016电视剧纪录部',
                    'AVOPEN2016素人部門': 'AVOPEN2016素人部', 'AVOPEN2016バラエティ部門': 'AVOPEN2016娱乐部',
                    'VR専用': 'VR専用', '堵嘴·喜劇': '堵嘴·喜剧', '幻想': '幻想', '性別轉型·女性化': '性别转型·女性化',
                    '為智能手機推薦垂直視頻': '为智能手机推荐垂直视频', '設置項目': '设置项目', '迷你係列': '迷你系列',
                    '體驗懺悔': '体验忏悔', '黑暗系統': '黑暗系统',

                    'オナサポ': '手淫', 'アスリート': '运动员', '覆面・マスク': '蒙面具', 'ハイクオリティVR': '高品质VR', 'ヘルス・ソープ': '保健香皂', 'ホテル': '旅馆',
                    'アクメ・オーガズム': '绝顶高潮', '花嫁': '花嫁', 'デート': '约会', '軟体': '软体', '娘・養女': '养女', 'スパンキング': '打屁股',
                    'スワッピング・夫婦交換': '夫妇交换', '部下・同僚': '部下・同僚', '旅行': '旅行', '胸チラ': '露胸', 'バック': '后卫', 'エロス': '爱的欲望',
                    '男の潮吹き': '男人高潮', '女上司': '女上司', 'セクシー': '性感美女', '受付嬢': '接待小姐', 'ノーブラ': '不穿胸罩',
                    '白目・失神': '白眼失神', 'M女': 'M女', '女王様': '女王大人', 'ノーパン': '不穿内裤', 'セレブ': '名流', '病院・クリニック': '医院诊所',
                    '面接': '面试', 'お風呂': '浴室', '叔母さん': '叔母阿姨', '罵倒': '骂倒', 'お爺ちゃん': '爷爷', '逆レイプ': '强奸小姨子',
                    'ディルド': 'ディルド', 'ヨガ': '瑜伽', '飲み会・合コン': '酒会、联谊会', '部活・マネージャー': '社团经理', 'お婆ちゃん': '外婆',
                    'ビジネススーツ': '商务套装',
                    'チアガール': '啦啦队女孩', 'ママ友': '妈妈的朋友', 'エマニエル': '片商Emanieru熟女塾', '妄想族': '妄想族', '蝋燭': '蜡烛', '鼻フック': '鼻钩儿',
                    '放置': '放置', 'サンプル動画': '范例影片', 'サイコ・スリラー': '心理惊悚片', 'ラブコメ': '爱情喜剧', 'オタク': '御宅族',

                    ## JAVDB

                    '可播放': '可播放', '可下載': '可下载', '含字幕': '含字幕', '單體影片': '单体影片', '含預覽圖': '含预览图',
                    '含預覽視頻': '含预览视频', '2020': '2020', '2019': '2019', '2018': '2018', '2017':
                    '2017', '2016': '2016', '2015': '2015', '2014': '2014', '2013': '2013', '2012':
                    '2012', '2011': '2011', '2010': '2010', '2009': '2009', '2008': '2008', '2007':
                    '2007', '2006': '2006', '2005': '2005', '2004': '2004', '2003': '2003', '2002':
                    '2002', '2001': '2001', '淫亂，真實': '淫乱，真实', '出軌': '出轨', '強姦': '强奸', '亂倫': '乱伦',
                    '溫泉': '温泉', '女同性戀': '女同性恋', '企畫': '企画', '戀腿癖': '恋腿癖', '獵豔': '猎艳', '偷窺': '偷窥',
                    '洗澡': '洗澡', '其他戀物癖': '其他恋物癖', '處女': '处女', '性愛': '性爱', '男同性戀': '男同性恋', '學校作品':
                    '学校作品', '妄想': '妄想', '韓國': '韩国', '形象俱樂部': '形象俱乐部', '友誼': '友谊', '亞洲': '亚洲', '暗黑系':
                    '暗黑系', 'M男': 'M男', '天賦': '天赋', '跳舞': '跳舞', '被外國人幹': '被外国人干', '戀物癖': '恋物癖',
                    '戀乳癖': '恋乳癖', '惡作劇': '恶作剧', '運動': '运动', '倒追': '倒追', '女同接吻': '女同接吻', '美容院':
                    '美容院', '奴隸': '奴隶', '白天出軌': '白天出轨', '流汗': '流汗', '性騷擾': '性骚扰', '情侶': '情侣',
                    '爛醉如泥的': '烂醉如泥的', '魔鬼系': '魔鬼系', '處男': '处男', '殘忍畫面': '残忍画面', '性感的': '性感的', '曬黑':
                    '晒黑', '雙性人': '双性人', '全裸': '全裸', '正太控': '正太控', '觸手': '触手', '正常': '正常', '奇異的':
                    '奇异的', '蠻橫嬌羞': '蛮横娇羞', '高中女生': '高中女生', '美少女': '美少女', '已婚婦女': '已婚妇女', '藝人': '艺人',
                    '姐姐': '姐姐', '各種職業': '各种职业', '蕩婦': '荡妇', '母親': '母亲', '女生': '女生', '妓女': '妓女',
                    '新娘，年輕妻子': '新娘，年轻妻子', '女教師': '女教师', '白人': '白人', '公主': '公主', '童年朋友': '童年朋友',
                    '婆婆': '婆婆', '飛特族': '飞特族', '亞洲女演員': '亚洲女演员', '女大學生': '女大学生', '偶像': '偶像', '明星臉':
                    '明星脸', '痴漢': '痴汉', '大小姐': '大小姐', '秘書': '秘书', '護士': '护士', '角色扮演者': '角色扮演者',
                    '賽車女郎': '赛车女郎', '家教': '家教', '黑人演員': '黑人演员', '妹妹': '妹妹', '寡婦': '寡妇', '女醫生':
                    '女医生', '老闆娘，女主人': '老板娘，女主人', '女主播': '女主播', '其他學生': '其他学生', '模特兒': '模特儿', '格鬥家':
                    '格斗家', '展場女孩': '展场女孩', '禮儀小姐': '礼仪小姐', '女檢察官': '女检察官', '講師': '讲师', '服務生': '服务生',
                    '伴侶': '伴侣', '車掌小姐': '车掌小姐', '女兒': '女儿', '年輕女孩': '年轻女孩', '眼鏡': '眼镜', '角色扮演':
                    '角色扮演', '內衣': '内衣', '制服': '制服', '水手服': '水手服', '泳裝': '泳装', '和服，喪服': '和服，丧服',
                    '連褲襪': '连裤袜', '女傭': '女佣', '運動短褲': '运动短裤', '女戰士': '女战士', '校服': '校服', '制服外套':
                    '制服外套', '修女': '修女', 'COSPLAY服飾': 'COSPLAY服饰', '裸體圍裙': '裸体围裙', '女忍者': '女忍者',
                    '身體意識': '身体意识', 'OL': 'OL', '貓耳女': '猫耳女', '學校泳裝': '学校泳装', '迷你裙': '迷你裙', '浴衣':
                    '浴衣', '猥褻穿著': '猥亵穿着', '緊身衣': '紧身衣', '娃娃': '娃娃', '蘿莉角色扮演': '萝莉角色扮演', '女裝人妖':
                    '女装人妖', '及膝襪': '及膝袜', '泡泡襪': '泡泡袜', '空中小姐': '空中小姐', '旗袍': '旗袍', '兔女郎': '兔女郎',
                    '女祭司': '女祭司', '動畫人物': '动画人物', '迷你裙警察': '迷你裙警察', '成熟的女人': '成熟的女人', '巨乳': '巨乳',
                    '蘿莉塔': '萝莉塔', '無毛': '无毛', '屁股': '屁股', '苗條': '苗条', '素人': '素人', '乳房': '乳房',
                    '巨大陰莖': '巨大阴茎', '胖女人': '胖女人', '平胸': '平胸', '高': '高', '美腳': '美脚', '孕婦': '孕妇',
                    '巨大屁股': '巨大屁股', '瘦小身型': '瘦小身型', '變性者': '变性者', '肌肉': '肌肉', '超乳': '超乳', '乳交':
                    '乳交', '中出': '中出', '多P': '多P', '69': '69', '淫語': '淫语', '女上位': '女上位', '自慰': '自慰',
                    '顏射': '颜射', '潮吹': '潮吹', '口交': '口交', '舔陰': '舔阴', '肛交': '肛交', '手指插入': '手指插入',
                    '手淫': '手淫', '放尿': '放尿', '足交': '足交', '按摩': '按摩', '吞精': '吞精', '剃毛': '剃毛',
                    '二穴同時挿入': '二穴同时插入', '母乳': '母乳', '濫交': '滥交', '深喉': '深喉', '接吻': '接吻', '拳交': '拳交',
                    '飲尿': '饮尿', '騎乗位': '骑乘位', '排便': '排便', '食糞': '食粪', '凌辱': '凌辱', '捆綁': '捆绑', '緊縛':
                    '紧缚', '輪姦': '轮奸', '玩具': '玩具', 'SM': 'SM', '戶外': '户外', '乳液': '乳液', '羞恥': '羞耻',
                    '女優按摩棒': '女优按摩棒', '拘束': '拘束', '調教': '调教', '立即口交': '立即口交', '跳蛋': '跳蛋', '監禁':
                    '监禁', '導尿': '导尿', '按摩棒': '按摩棒', '插入異物': '插入异物', '灌腸': '灌肠', '藥物': '药物', '露出':
                    '露出', '汽車性愛': '汽车性爱', '催眠': '催眠', '鴨嘴': '鸭嘴', '糞便': '粪便', '脫衣': '脱衣', '子宮頸':
                    '子宫颈', '4小時以上作品': '4小时以上作品', '戲劇': '戏剧', '第一人稱攝影': '第一人称摄影', 'HDTV': 'HDTV',
                    '首次亮相': '首次亮相', '薄馬賽克': '薄马赛克', '數位馬賽克': '数位马赛克', '業餘': '业余', '故事集': '故事集',
                    '經典': '经典', '戀愛': '恋爱', 'VR': 'VR', '給女性觀眾': '给女性观众', '精選，綜合': '精选，综合', '國外進口':
                    '国外进口', '科幻': '科幻', '行動': '行动', '成人電影': '成人电影', '綜合短篇': '综合短篇', '滑稽模仿': '滑稽模仿',
                    '男性': '男性', '介紹影片': '介绍影片', '冒險': '冒险', '模擬': '模拟', '愛好，文化': '爱好，文化', '懸疑':
                    '悬疑', 'R-15': 'R-15', '美少女電影': '美少女电影', '感官作品': '感官作品', '觸摸打字': '触摸打字', '投稿':
                    '投稿', '紀錄片': '纪录片', '去背影片': '去背影片', '獨立製作': '独立制作', '主觀視角': '主观视角', '戰鬥行動':
                    '战斗行动', '特效': '特效', '16小時以上作品': '16小时以上作品', '局部特寫': '局部特写', '重印版': '重印版', '歷史劇':
                    '历史剧', '寫真偶像': '写真偶像', '3D': '3D', '訪問': '访问', '教學': '教学', '恐怖': '恐怖', '西洋片':
                    '西洋片', '45分鍾以內': '45分钟以内', '45-90分鍾': '45-90分钟', '90-120分鍾': '90-120分钟',
                    '120分鍾以上': '120分钟以上',

                    # FANZA

                    '動画': '视频', '電子書籍': '电子书', '同人': '同人志', 'アダルトPCゲーム': '成人PC游戏', 'DVD/CD':
                        ' DVD / CD', 'コミック': '漫画', 'いろいろレンタル': '各种租赁', '通販': '购物', 'マーケットプレイス': '市场',
                    '3Dプリント': ' 3D打印', 'ロボット': '机器人', '巨乳': '大乳房', '熟女': '成熟女人', 'ギャル': '美少女',
                    '人妻・主婦': '已婚妇女', '女子校生': '高中女生', '中出し': '中出', 'アナル': '肛门', 'ニューハーフ': '变性人',
                    'VR専用': '仅VR', 'ハイクオリティVR': '高质量VR', 'アイドル・芸能人': '偶像/名人', 'アクメ・オーガズム':
                        'Acme性高潮', 'アスリート': '运动员', '姉・妹': '姐妹', 'イタズラ': '恶作剧', 'インストラクター': '指导员',
                    'ウェイトレス': '服务员', '受付嬢': '接待员', 'エステ': 'Este', 'M男': 'M人', 'M女': 'M女', 'OL':
                        'OL', 'お母さん': '妈妈', '女将・女主人': '房东/情妇', '幼なじみ': '儿时的朋友', 'お爺ちゃん': '爷爷', 'お嬢様・令嬢':
                        '女士/女儿', 'オタク': '极客', 'オナサポ': '奥纳萨波', 'お姉さん': '姐姐', 'お婆ちゃん': '祖母', '叔母さん': '阿姨',
                    'お姫様': '公主', 'お風呂': '浴', '温泉': '温泉', '女教師': '女老师', '女上司': '女老板', '女戦士': '女战士',
                    '女捜査官': '女调查员', 'カーセックス': '汽车性', '格闘家': '战斗机', 'カップル': '情侣', '家庭教師': '戴绿帽',
                    '看護婦・ナース': '护士/护士', 'キャバ嬢・風俗嬢': '戴绿帽小姐/海关小姐', 'キャンギャル': '戴绿帽', '近親相姦': '乱伦',
                    '義母': '岳母', '逆ナン': '反向南', 'くノ一': 'Kunoichi', 'コンパニオン': '同伴', '主観': '主观', '職業色々':
                        '各种职业', 'ショタ': '肖塔', '白目・失神': '白眼/戴绿帽子', '時間停止': '戴绿帽子', '女医': '女医生', '女王様':
                        '女王', '女子アナ': '女安娜', '女子大生': '女大学生', 'スチュワーデス': '空姐', 'スワッピング・夫婦交換': '交换/戴绿帽子',
                    '性転換・女体化': '性/女性化', 'セレブ': '名人', 'チアガール': '欢呼女孩', '痴女': '荡妇', 'ツンデレ': '戴绿帽子',
                    'デート': '约会', '盗撮・のぞき': '戴绿帽子/窥视', 'ドール': '娃娃', '寝取り・寝取られ・NTR': '戴绿帽子/戴绿帽子/ NTR',
                    'ノーパン': '无锅', 'ノーブラ': '无胸罩', '飲み会・合コン': '饮酒党/联合党', 'ハーレム': '哈林', '花嫁': '新娘',
                    'バスガイド': '巴士指南', '秘書': '秘书', 'ビッチ': 'B子', '病院・クリニック': '医院/诊所', 'ファン感謝・訪問':
                        '球迷欣赏/探访', '不倫': '外遇', '部活・マネージャー': '俱乐部/经理', '部下・同僚': '下属/同事', 'ヘルス・ソープ':
                        '健康皂', '変身ヒロイン': '转型女主人公', 'ホテル': '酒店', 'マッサージ・リフレ': '按摩咨询', '魔法少女': '魔术女郎',
                    'ママ友': '妈妈朋友', '未亡人': '女人', '娘・養女': '女儿/被收养的女人', '胸チラ': '胸部希拉', 'メイド': '制作',
                    '面接': '面试', 'モデル': '模特', '野外・露出': '户外/曝光', 'ヨガ': '瑜伽', '乱交': '狂欢', '旅行': '旅行',
                    'レースクィーン': '种族女王', '若妻・幼妻': '年轻妻子/年轻妻子', 'アジア女優': '亚洲女演员', '巨尻': '大屁股', '筋肉':
                        '肌肉', '小柄': '娇小', '黒人男優': '黑人演员', '処女': '处女', '女装・男の娘': '女人和男人的女儿', 'スレンダー':
                        '苗条', '早漏': '早泄', 'そっくりさん': '相似', '長身': '高大', '超乳': '超级牛奶', 'デカチン・巨根':
                        '大鸡巴/大鸡巴', '童貞': '处女', '軟体': '柔软的身体', '妊婦': '孕妇', '白人女優': '白人女演员', 'パイパン': '剃光',
                    '日焼け': '晒伤', '貧乳・微乳': '小乳房/小乳房', '美少女': '美丽的女孩l', '美乳': ' Beautiful Breasts',
                    'ふたなり': ' Futanari', 'ぽっちゃり': ' Chubby', 'ミニ系': ' Mini', '学生服':
                        'Student Clothes', '競泳・スクール水着': ' Swimming / School Swimsuits', 'コスプレ':
                        'Cosplay', 'COSPLAY服饰': ' COSPLAY服饰', '制服': ' Uniforms', '体操着・ブルマ':
                        'Gymnastics / Bloomers', 'チャイナドレス': '中国服饰', 'ニーソックス': '过膝袜', 'ネコミミ・獣系':
                        'Nekomimi / Beast', '裸エプロン': '裸围裙', 'バニーガール': '兔女郎', 'パンスト・タイツ': '连裤袜/裤袜',
                    'ビジネススーツ': '西装', '覆面・マスク': '面罩/面罩', 'ボディコン': ' Body Con', 'ボンテージ': ' Bontage',
                    '巫女': '神社少女', '水着': '泳装', 'ミニスカ': '超短裙', 'ミニスカポリス': '超短裙警察', 'めがね': '眼镜',
                    'ランジェリー': '女用贴身内衣裤', 'ルーズソックス': '松散的袜子', 'レオタード': '紧身连衣裤', '和服・浴衣': '日式服装/浴衣',
                    'アクション・格闘': '动作/格斗', '脚フェチ': '腿恋物癖', 'アニメ': '动漫', 'イメージビデオ': '图像视频',
                    'イメージビデオ（男性）': '图像视频（男）', '淫乱・ハード系': '讨厌/困难', 'SF': ' SF', 'SM': ' SM', '学園もの':
                        '学校事物', '企画': '计划', '局部アップ': '本地化', '巨乳フェチ': '大恋物癖', 'ギャグ・コメディ': '堵嘴喜剧',
                    'クラシック': '经典', 'ゲイ': '同性恋', '原作コラボ': '原始协作', 'コラボ作品': '协作工作', 'サイコ・スリラー':
                        '心理惊悚片', '残虐表現': '残酷表情', '尻フェチ': '屁眼恋物癖', '素人': '业余爱好者', '女性向け': '女士',
                    '女優ベスト・総集編': '女演员最佳/摘要', 'スポーツ': '运动', 'セクシー': '性感', 'その他フェチ': '其他恋物癖', '体験告白':
                        '自白', '単体作品': '单身', 'ダーク系': '黑暗', 'ダンス': '舞蹈', '着エロ': '穿着色情', 'デビュー作品': '首次亮相',
                    '特撮': '特殊效果', 'ドキュメンタリー': '纪录片', 'ドラマ': '戏剧', 'ナンパ': '南帕', 'HowTo': ' HowTo',
                    'パンチラ': '内衣', 'ファンタジー': '幻想', '復刻': ' Reprint', 'Vシネマ': ' V Cinema', 'ベスト・総集編':
                        '最佳/摘要', 'ホラー': '恐怖', 'ボーイズラブ': ' Boys Love', '妄想': ' Delusion', '洋ピン・海外輸入':
                        ' Western Pin / Overseas Import', 'レズ': ' Lesbian', '恋愛': ' Love', '足コキ':
                        ' Footjob', '汗だく': ' Sweaty', 'アナルセックス': '肛交', '異物挿入': '异物插入', 'イラマチオ':
                        'Iramachio', '淫語': '脏话', '飲尿': '喝尿', '男の潮吹き': '人喷', 'オナニー': '手淫', 'おもちゃ': '玩具',
                    '監禁': '禁闭', '浣腸': '灌肠', '顔射': '恋物癖', '顔面騎乗': '面部骑行', '騎乗位': '女牛仔', 'キス・接吻':
                        '接吻和亲吻', '鬼畜': '恶魔', 'くすぐり': '发痒', 'クスコ': '库斯科', 'クンニ': '坤妮', 'ゲロ': '下吕', '拘束':
                        '拘束', '拷問': '酷刑', 'ごっくん': '暨', '潮吹き': '喷', 'シックスナイン': '六十九', '縛り・緊縛': '绑/束缚',
                    '羞恥': '羞耻', '触手': '触觉', '食糞': '食物粪便', 'スカトロ': '蹲', 'スパンキング': '打屁股', '即ハメ':
                        '立即鞍', '脱糞': '排便', '手コキ': '打手枪', 'ディルド': '假阳具', '電マ': '电ma', 'ドラッグ': '拖动', '辱め':
                        '屈辱', '鼻フック': '鼻子钩', 'ハメ撮り': '颜射', '孕ませ': '构思', 'バイブ': '盛传', 'バック': '后背', '罵倒':
                        '辱骂', 'パイズリ': '乳交', 'フィスト': '拳头', 'フェラ': '吹', 'ぶっかけ': '颜射', '放置': '离开',
                    '放尿・お漏らし': '小便/泄漏', '母乳': '母乳', 'ポルチオ': 'Porchio', '指マン': '手指男人', 'ラブコメ': '爱来',
                    'レズキス': '女同性恋之吻', 'ローション・オイル': '乳液油', 'ローター': '转子', '蝋燭': '蜡烛', '3P・4P':
                        ' 3P / 4P', 'インディーズ': '印度', 'エマニエル': '伊曼妮尔', '期間限定セール': '限时特卖', 'ギリモザ': '最小马赛克',
                    'ゲーム実写版': '游戏直播版', '新人ちゃん続々デビュー': '新移民出道', 'スマホ推奨縦動画': 'Sma rtphone推荐垂直视频',
                    'セット商品': '固定产品', 'その他': '其他', 'デジモ': ' Digimo', '投稿': '发布', '独占配信': '独家发行',
                    'ハイビジョン': '高清', 'パラダイスTV': '天堂电视', 'FANZA配信限定': ' FANZA发行有限公司', '複数話': '多个情节',
                    '妄想族': 'Delusion组', '16時間以上作品': '16小时或以上的工作', '3D': '3D', '4時間以上作品':
                        '4小时或以上的工作', 'プレステージ30％OFF': 'Prestige 30％OFF', '豊彦・山と空・ヒプノシスRASH他30％OFF':
                        'Toyohiko,高山和天空催眠RASH等30％OFF', '熟女JAPAN・人妻援護会他30％OFF':
                        '日本成熟女性/已婚妇女支持协会等。30％OFF', 'ブランドストア30％OFF！': '品牌商店30％OFF！ ',

                    # mgstage

                    'ギャル': '辣妹', 'ナンパ': '搭讪', 'カップル': '情侣', 'スレンダー': '身材苗条', 'エステ・マッサージ': '美容按摩',
                    '3P・4P': '3P・4P', '4時間以上作品': '曝光', 'MGSだけのおまけ映像付き': '只附带MGS的赠品影像', '中出し': '中出',
                    '乱交': '进口洋销', '人妻': '穿孔货', '企画': '计划', 'デビュー作品': '出道作品', '初撮り': '白人女演员', '単体作品':
                        '单体作品', '即ハメ': '马上就发', 'キャバ嬢・風俗嬢': '陪酒女郎', '巨乳': '巨乳', '投稿': '投稿', 'ハメ撮り':
                        '新娘子', '潮吹き': '鲸鱼喷水', '熟女': '熟女', '独占配信': '独家发布', '痴女': '痴女', '童顔': '童颜',
                    '競泳・スクール水着': '游泳学校的游泳衣', '素人': '门外汉', 'ベスト・総集編': 'VR', '美乳': '美臀', '美少女': '美腿',
                    '職業色々': '各种职业', '配信専用': '配信专用', '電マ': '电码', '顔射': '颜射', 'アイドル・芸能人': '偶像艺人',
                    'アクション・格闘': '格斗动作', '足コキ': '脚钩子', '脚フェチ': '脚控', 'アジア女優': '亚洲女演员', '汗だく': '汗流浃背',
                    'アナルセックス': '肛门性爱', 'アナル': '肛门', '姉・妹': '姐姐、妹妹', 'Eカップ': 'E罩杯', 'イタズラ': '恶作剧',
                    '異物挿入': '插入异物', 'イメージビデオ': '视频图像', '色白': '白皙', '淫語': '淫语', '淫語モノ': '淫语故事',
                    'インストラクター': '教练', '飲尿': '饮用水', '淫乱・ハード系': '淫乱硬系', 'ウェイトレス': '女服务生', 'Hカップ':
                        'H罩杯', 'SF': 'SF', 'SM': 'SM', 'Fカップ': 'F罩杯', 'M男': 'M男', 'お母さん': '妈妈',
                    '女将・女主人': '女主人', 'お嬢様・令嬢': '大小姐', 'オナニー': '自慰', 'お姉さん': '姐姐', 'オモチャ': '玩具',
                    '温泉': '温泉', '女戦士': '女战士', '女捜査官': '女搜查官', 'カーセックス': '汽车做爱', '介護': '看护', '格闘家':
                        '格斗家', '家庭教師': '家庭教师', '監禁': '监禁', '看護婦・ナース': '护士护士', '浣腸': '灌肠', '学園もの': '校园剧',
                    '顔面騎乗': '颜面骑乘', '局部アップ': '局部提高', '巨尻': '巨臀', '巨乳フェチ': '巨乳恋物癖', '騎乗位': '骑乘位',
                    'キス': '沙鮻', 'キス・接吻': '接吻', '鬼畜': '鬼畜', '着物・浴衣': '和服、浴衣', '近親相姦': '近亲通奸', '筋肉':
                        '肌肉', '金髪・ブロンド': '金发', '逆ナン': '逆搭讪', '義母': '岳母', 'くノ一': '九一', 'ゲイ・ホモ': '同性恋',
                    '拘束': '拘束', '口内射精': '口里射精', '口内発射': '口里发射', '黒人男優': '黑人男演员', 'コスプレ': 'COSPLAY',
                    'コンパニオン': '接待员', 'ごっくん': '捉迷藏', '羞恥': '羞耻', '羞恥・辱め': '羞辱', '主観': '主观', '触手':
                        '触手', '食糞': '饭桶', '処女': '处女', 'ショタ': '正太', '縛り・緊縛': '束缚', '尻フェチ': '屁股恋物癖', '女医':
                        '女大夫', '女教師': '女教师', '女子アナ': '女主播', '女子校生': '女学生', '女子大生': '女大学生', '女性向け':
                        '面向女性', '女装・男の娘': '伪娘', 'Gカップ': 'G罩杯', 'スカトロ': '水平多关节', 'スチュワーデス・CA': '空姐CA',
                    'スポーツ': '体育运动', '清楚': '清秀', '制服': '制服', 'その他フェチ': '其他恋物癖', '体操着・ブルマ': '运动服',
                    '多人数': '很多人', '着エロ': '色情', '長身': '高个子', '痴漢': '色狼', '手コキ': '手锯', '手マン': '手艺人',
                    'Dカップ': 'D罩杯', '泥酔': '烂醉如泥', 'デカチン・巨根': '巨根', '盗撮': '偷拍', '盗撮・のぞき': '偷拍', '童貞':
                        '处男', 'ドキュメンタリー': '记录片', 'ドラッグ・媚薬': '药局', 'ドラマ': '电视剧', 'ニューハーフ': '变性人',
                    'ニーソックス': '过膝袜', '妊婦': '孕妇', '寝取り・寝取られ': '睡下', 'HowTo': 'How', '白人女優': 'To',
                    '花嫁・若妻': '首次拍摄', 'バイブ': '拍鸽子', '爆乳': '振动', 'パイズリ': '乳交', 'パイパン': '裁缝', 'パンチラモノ':
                        '菠萝', '貧乳・微乳': '人妻', '美脚': '贫奶', '美尻': '美少女', 'ファン感謝・訪問': '美乳', 'フィスト':
                        '粉丝感谢访问', '復刻': '结束', '風俗': '复刻', 'ふたなり': '风俗', '不倫': '双胞胎', 'ぶっかけ': '不伦', 'VR':
                        '泼', '放尿・失禁': '精选集', 'ホラー': '放尿、失禁', '母乳': '恐怖', 'ボンテージ': '母乳', 'ぽっちゃり': '气瓶',
                    '巫女': '丰满', '水着': '巫女', 'ミニスカ': '游泳衣', '未亡人': '迷你裙', 'メイド': '遗孀', 'メガネ': '女仆',
                    'モデル': '眼镜', '野外・露出': '模型', '洋ピン・海外輸入': '野外露出', 'ランジェリー': '乱交', 'レースクィーン': '内衣',
                    'レオタード': '花边皇后', 'レズ': '紧身衣', 'ローション・オイル': '女士', '露出': '化妆油',


                    #fc2
                    '素人': '素人', '美女': '美人', '拍鸽子': 'ハメ撮り', '恋物癖': 'フェチ', '巨乳': '巨乳', 'COSPLAY':
                        'コスプレ・制服', '自拍': '自分撮り', '其他': 'その他', 'OL姐姐': 'OL・お姉さん', '同性恋': 'ゲイ', '3P・乱交':
                        '３P・乱交', '野外露出': '野外・露出', '国外': '海外', 'SM': 'SM', '女士': 'レズ', '动画': 'アニメ', 'BL':
                        'BL', '成人': 'アダルト', '空闲': 'アイドル', '门外汉': '素人', 'cosplay制服': 'コスプレ・制服', '个人摄影':
                        '個人撮影', '不修改': '無修正', '角色扮演': 'コスプレ', '内衣': '下着', '美乳': '美乳', '游泳衣': '水着', '流出':
                        '流出', '制服': '制服', '小册子': 'パンチラ', '口交': 'フェラ', '模型': 'モデル', '中出': '中出し', '可爱':
                        '可愛い', '人妻': '人妻', '美少女': '美少女', '原始': 'オリジナル', '贫奶': '貧乳', '自慰': 'オナニー', '菠萝':
                        'パイパン','ロリ':'萝莉','生ハメ':'第一人称',
                    }
        try:
            return dict_gen[tag]
        except:
            return tag
    else:
        return tag

def translate(src:str,target_language:str="zh_cn"):
    url = "https://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=" + target_language + "&q=" + src
    result = get_html(url=url,return_type="object")

    translate_list = [i["trans"] for i in result.json()["sentences"]]

    return "".join(translate_list)

# ========================================================================是否为无码
def is_uncensored(number):
    if re.match('^\d{4,}', number) or re.match('n\d{4}', number) or 'HEYZO' in number.upper():
        return True
    configs = config.Config().get_uncensored()
    prefix_list = str(configs).split(',')
    for pre in prefix_list:
        if pre.upper() in number.upper():
            return True
    return False
