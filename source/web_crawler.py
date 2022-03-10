# module 
from os import makedirs
import os.path,time,re
import hashlib

# ssl module
import socket, ssl
from webbrowser import get
import OpenSSL

# other
import urllib
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

test_files = {}
WORKDIR = "./data/"

# get link
def enum_links(html,base):
    soup = BeautifulSoup(html,"html.parser")
    links = soup.select("link[ref='stylesheet']")
    links += soup.select("a[href]")
    result = []

    for a in links:
        href = a.attrs['href']
        url = urljoin(base,href)
        result.append(url)

    result = list(set(result))

    return result


def make_savepath(url):

    o = urlparse(url)
    savepath = WORKDIR + o.netloc + o.path
    if re.search(r"/$",savepath):
        savepath += "index.html"
        
    if savepath.find('.',savepath.rfind('/')) == -1 :
        savepath += "/index.html"

    if savepath.count('/') == 1:
        savepath += "/index.html"

    return savepath

def get_md5hs(str):

    return hashlib.md5(str.encode()).hexdigest()

# download
def download_file(url):
    
    savepath = make_savepath(url)
    savedir = os.path.dirname(savepath)

    if os.path.exists(savepath): return savepath

    if not os.path.exists(savedir):
        print("mkdir=",savedir)
        makedirs(savedir)

    try:
        print("download=",url)
        urlretrieve(url,savepath)
        time.sleep(1)
        return savepath
    except:
        print("download failed:",url)
        return None

# get x509
def get_server_certificate(hostname):
    context = ssl.create_default_context()
    path = WORKDIR + hostname + '/' + hostname + '.cer'
    if os.path.exists(path): return

    savedir = os.path.dirname(path)
    if not os.path.exists(savedir):
        print("mkdir=",savedir)
        makedirs(savedir)

    with socket.create_connection((hostname,443)) as sock:
        with context.wrap_socket(sock,server_hostname=hostname) as sslsock:
            der_cert = sslsock.getpeercert(True)

            path = WORKDIR + hostname + '/' + hostname + '.cer'
            
            with open(path, mode='w') as f:
                f.write(ssl.DER_cert_to_PEM_cert(der_cert))

    return 

# リンクを再帰的に取得
def analize_html(url):

    o = urlparse(url)
    root_url = o.scheme + '://' + o.hostname

    savepath = download_file(url)
    if savepath is None: return False
    if savepath in test_files: return False

    test_files[savepath] = True
    print("analize_html=",url)

    html = open(savepath,"r",encoding="utf-8").read()
    links = enum_links(html,url)
    #for link_url in links:
        # 別ドメイン 
        #if link_url.find(root_url) != 0:
        #    if not re.search(r".css$",link_url):continue

        # リンク先を再帰的に取得する場合
        #if re.search(r".(html|html)$",link_url):
        #    analize_html(link_url)
        #    continue

        #download_file(link_url)

    # get certificate 
    if o.scheme == 'https':
        get_server_certificate(o.hostname)

    return True

from selenium import webdriver
import chromedriver_binary

def get_screen(url):
    
    #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36' 

    #dcap = {"phantomjs.page.settings.userAgent" : user_agent,'marionette' : True}
    
    #driver = webdriver.PhantomJS(desired_capabilities=dcap)

    driver = webdriver.Chrome()
    driver.set_window_size(1200, 800)
    driver.get(url)

    
    savepath = WORKDIR + get_md5hs(url)
    
    
    driver.save_screenshot(savepath + '.png')

    t = driver.page_source
    
    with open(savepath + '.txt', 'w', encoding='utf-8') as f:
        f.write(t)
    

    driver.close()


# debug
if __name__ =="__main__":

    ret = ''

    url = 'www.yahoo.co.jp'
    get_server_certificate(url)

    print(ret)





