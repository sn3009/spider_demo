#encoding=utf-8
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from ffmpy3 import FFmpeg

#list_url = "http://www.jisutiyu.com/shipin/xijia"
main_domain = "http://www.jisutiyu.com/"

def visit_list_page(pageNum):
    list_url = "http://www.jisutiyu.com/shipin/xijia"
    if(pageNum > 1):
        list_url = list_url + "/" + pageNum + "/"
    opt = webdriver.ChromeOptions()
    opt.set_headless()
    opt.add_argument('--ignore-certificate-errors')
    opt.add_argument("--test-type")
    opt.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36")
    driver = webdriver.Chrome(options=opt, executable_path="/Users/shuttle/python/chromedriver")
    driver.get(list_url)
    soup = BeautifulSoup(driver.page_source)
    print("#####开始列表页######")
    lis = soup.find_all("li")
    i=0
    for li in lis:
        i = i + 1
        try:
            if(li.find("span") is None):
                continue
            print("#####解析第" + str(i) + "个详情页######")
            link = main_domain + li.find("a").get("href")
            driver.get(link)
            detail = BeautifulSoup(driver.page_source)
            mp4 = detail.find("video").get("src")
            t = time.time()
            _name = str(int(round(t * 1000000))) + '.mp4'
            title = detail.find("h1").contents[0]
            pub_time = detail.find("div", class_="info").get_text()
            if(mp4):
                f = "source.txt"
                print("#####第" + str(i) + "个详情页开始写入文件######")
                ffmpeg_path(mp4, "down/" + _name)
                with open(f, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
                    info = mp4 + "," + title + "," + pub_time
                    file.write(info + "\n")
            print("#####第" + str(i) + "个详情页解析结束######")
        except Exception as e:
            print("#####解析第" + str(i) + "个详情页解析错误######" + str(e))
            continue
    print("#####第" + str(pageNum) + "列表页爬取结束######")


def ffmpeg_path(inputs_path, outputs_path):
    '''
    :param inputs_path: 输入的文件传入字典格式{文件：操作}
    :param outputs_path: 输出的文件传入字典格式{文件：操作}
    :return:
    '''
    a = FFmpeg(
                inputs={inputs_path: None},
                outputs={outputs_path: '-c copy',
                         }
    )
    print(a.cmd)
    a.run()

if __name__ == '__main__':
    what = input("请输入分页，分页从1开始)：")
    visit_list_page(int(what))