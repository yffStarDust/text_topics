# -*- coding: utf-8-*-
import re
from bs4 import BeautifulSoup


##过滤HTML中的标签
# 将HTML中标签等信息去掉
# @param htmlstr HTML字符串.
def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<![CDATA[[^>]*//]]>', re.I)  # 匹配CDATA
    re_script = re.compile('<s*script[^>]*>[^<]*<s*/s*scripts*>', re.I)  # Script
    re_style = re.compile('<s*style[^>]*>[^<]*<s*/s*styles*>', re.I)  # style
    re_br = re.compile('<brs*?/?>')  # 处理换行
    re_h = re.compile('</?w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('n+')
    s = blank_line.sub('n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s


##替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string, s)


def text_extract_html(html, label='p'):
    """
    Extract the text from the specified labels of the given html string
    :param html: Original html string
    :param label: Specified label in the html string
    :return: The concatenated Chinese text extracted from the specified labels of the html string
    """
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    links = soup.find_all(label)
    label_texts = []
    for link in links:
        line = link.text.strip().replace('\n', '')
        label_texts.append(line)
    return ' '.join(label_texts)


if __name__ == '__main__':
    html_str = \
    """
    <P class=Para>　　</p><p class=Para>　　中国客户联络中心奖是由中国电子商务协会客户联络中心专业委员会和第三方
    权威行业咨询研究和发展平台——才博(中国)主办，各级主管部门和行业协会提供官方指导。中国客户联络中心奖自2016年
    开始，立足于客户联络中心行业，在管理创新、服务创新、科技创新、客户口碑、客户体验等方面较优秀的单位与个人进行
    推荐和表彰。每年的1月-8月在全国范围内评选年度最佳客户联络中心和管理人，在每年的中国客户联络中心行业发展年会
    期间举行隆重的颁奖晚会，是客户联络中心行业最具影响力的年度评比活动，评审的专业度和权威性，以及公开，公平，
    公正的原则，被誉为是行业的最佳标杆评比。评审委员会从组织管理、运营管理、创新与品牌管理、职场建设、员工关怀等
    方面进行拨测和评估，经过现场测评、第三方拨测、机构推荐、专家评审四个流程，深入对标，最终评选出年度各大奖项，
    代表了当今客服行业的最高水平。</P>
    <img src="http://pic.finchina.com/Resource/6890631/RS0001-6890631947.jpg" alt="pic">
    <P class=Para>　　</p><p class=Para>　　2018年度“中国客户联络中心奖”权威发布（排名不分先后）</p><p class=Para>
    </p><p class=Para>　　2018年度客户口碑最佳客户联络中心（1000席以上）</p><p class=Para>　　</p><p class=Para>　
    北京京东世纪贸易有限公司</p><p class=Para>　　</p><p class=Para>　　美的集团用户交互中心</p><p class=Para>　　
    </p><p class=Para>　　中国电信股份有限公司浙江分公司10000号运营中心</p><p class=Para>　　</p><p class=Para>　　
    广州唯品会电子商务有限公司</p><p class=Para>　　</p><p class=Para>　　携程旅行网</p><p class=Para>　　
    </p><p class=Para>　　航天信息(600271,股吧)股份有限公司</p><p class=Para>　　</p><p class=Para>　　
    交通银行合肥金融服务中心</p><p class=Para>　　</p><p class=Para>　　北京鸿联九五信息产业有限公司</p><p class=Para>　　
    </p><p class=Para>　　广州点动信息科技股份有限公司</p><p class=Para>　　</p><p class=Para>　　
    中国工商银行远程银行中心(成都)</p><p class=Para>　　</p><p class=Para>　　VIPKID</p><p class=Para>　　</p><p class=Para>　　
    中国太平洋财产保险股份有限公司</p><p class=Para>　　</p><p class=Para>　　途牛旅游网</p><p class=Para>　　</p><p class=Para>　　
    国家电网公司客户服务中心北方分中心</p><p class=Para>　　</p><p class=Para>　　
    国家电网公司客户服务中心南方分中心</p><p class=Para>　　</p><p class=Para>　　北京百思特捷迅科技有限公司</p><p class=Para>　　
    </p><p class=Para>　　四川天翼呼叫科技有限公司</p>
    """
    html_str = text_extract_html(html_str)
    print(html_str)
