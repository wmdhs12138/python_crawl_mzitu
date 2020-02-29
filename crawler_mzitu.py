import urllib.request
import re
import pickle


def get_html(target_url, header=[]):
    print('获取HTML中...')
    try:
        req = urllib.request.Request(target_url)
        req.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
            )
        if header != []:
            req.add_header(header[0], header[1])
        response = urllib.request.urlopen(req)
        html = response.read()
        return html
    except:
        return 0


def ragular(p=r'', html='', i=1):
    print('计算正则表达式中...')
    if i == 1:
        return re.search(p, html).group()
    elif i == 0:
        return re.findall(p, html)


def decode_html(html):
    print('解码HTML中...')
    return html.decode('utf-8')


def get_url(html):
    print('获取URL中...')
    p = r'https://www.mzitu.com/(\d+)'
    i = 0
    return ragular(p, html, i)


def handle_url(url):
    print('优化URL中...')
    new_url = []
    for i in url:
        if i not in new_url:
            new_url.append(i)
    for i in new_url:
        j = 'https://www.mzitu.com/' + i + '/'
        new_url[new_url.index(i)] = j
    return new_url


def search_url(url):
    print('检查网页中...')
    try:
        urllib.request.urlopen(url)
        return 0
    except urllib.error.HTTPError:
        pass


def get_picaddr(url):
    print('获取套图地址中...')
    picaddr = []
    for each in url:
        html = decode_html(get_html(each))
        p = r'"https://i3.mmzztt.com/(.*?)"'
        i = 1
        picaddr.append(ragular(p, html, i).replace('"', ''))
    return picaddr


def downloadit(url, picaddr):
    print('下载中...')
    for j in range(len(url)):
        for i in range(200):
            new_url = url[j] + str(i+1)
            if i < 9:
                new_picaddr = picaddr[j][:33] + '0' + str(i+1) + '.' + picaddr[j].split('.')[-1]
            else:
                new_picaddr = picaddr[j][:33] + str(i+1) + '.' + picaddr[j].split('.')[-1]
            html = get_html(new_picaddr, ['Referer', new_url])
            if html == 0:
                break
            path = '下载路径（ps：文件夹路径，必须以/结尾）' + new_picaddr.split('/')[-1]
            with open(path, 'wb') as f:
                f.write(html)
                print('第{}张图片已下载'.format(i+1))
        print('套图{}全部下载完成！'.format(j+1))
    print('全部套图下载完成！')


def unpkl():
    with open('保存路径/mzitu.pkl', 'rb') as f:
        data = pickle.load(f)
    return data


def pkl(data):
    with open('保存路径/mzitu.pkl', 'wb') as f:
        pickle.dump(data, f)
        print('数据保存完成！')


def update(url, data):
    print('检查更新中...')
    update = []
    for i in url:
        if i not in data:
            data.append(i)
            update.append(i)
    if update != []:
        print('发现新的内容，共{}套'.format(len(update)))
        for j in update:
            print(j)
        temp = input('主人，要更新吗？[y/n]')
        if temp == 'y':
            return update
        else:
            update = []
            return update
    else:
        return update


if __name__ == '__main__':
    target_url = 'https://mzitu.com/'
    html = decode_html(get_html(target_url))
    url = handle_url(get_url(html))
    data = unpkl()
    sth = update(url, data)
    if sth != []:
        print('更新中...')
        picaddr = get_picaddr(sth)
        downloadit(sth, picaddr)
        print('更新完成！')
        pkl(url)
    else:
        print('没有新的内容！')
