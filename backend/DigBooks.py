import pandas as pd
import requests
from lxml import etree
import time


def dig_books():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    book_data = []
    # 一共有10页
    base_url = 'https://book.douban.com/top250?start={}'
    result = pd.DataFrame()
    for num in range(0, 250, 25):
        url = base_url.format(num)
        html = requests.get(url, headers=headers)
        bs = etree.HTML(html.text)
        for i in bs.xpath('//tr[@class = "item"]'):
            item = {"name": "", "author": "", "description": "", "pic_url": ""}
            # 书籍中文名
            book_ch_name = i.xpath('td[2]/div[1]/a[1]/@title')[0]
            # # 评分
            # score = i.xpath('td[2]/div[2]/span[2]')[0].text
            # 书籍信息
            book_info = i.xpath('td[2]/p[@class = "pl"]')[0].text
            author = book_info.split('/')[0].replace('【', '[').replace('】', ']')  # 只取作者
            # 评价数量由于数据不规整，这里用PYTHON字符串方法对数据进行了处理
            comment_num = i.xpath('td[2]/div[2]/span[3]')[0].text.replace(' ', '').strip('(\n').strip('\n)')
            pic_url = i.xpath('td[1]/a/img/@src')[0]
            try:
                # 后面有许多书籍没有一句话概括
                # 一句话概括
                brief = i.xpath('td[2]/p[@class = "quote"]/span')[0].text
            except:
                brief = "暂时没有简介"
            # 设置书籍信息
            item['name'] = book_ch_name
            item['author'] = author
            item['description'] = brief
            item['pic_url'] = pic_url
            book_data.append(item)
            # 这里的cache是存储每一次循环的结果，然后通过下一步操作循环更新result里面的数据
            cache = pd.DataFrame({'name': [book_ch_name], \
                                  'author': [author], 'description': [brief],
                                  'pic_url': [pic_url]})
            # 把新循环中的cache添加到result下面
            result = pd.concat([result, cache])
        time.sleep(0.5)
        print('我们正在爬取：{}页'.format((num / 25) + 1))
    result.head()
    # 把结果一步存为EXCEL
    result.to_excel('豆瓣图书TOP250.xlsx', index=False)
    return book_data


if __name__ == '__main__':
    print(len(dig_books()))
