import urllib
import urllib.request
from urllib.parse import urlparse,urlencode

import re
import whois
import ipaddress

from datetime import datetime
from bs4 import BeautifulSoup


# mymodule
import connect_mysql


# Domain 
def getDomain(url):  
    domain = urlparse(url).netloc
    if re.match(r"^www.",domain):
        domain = domain.replace("www.","")
    return domain

# is IP address
def haveIP(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip

# have @mark
def haveAt(url):
    if "@" in url:
        at = 1    
    else:
        at = 0    
    return at

# length 
# todo check length
def getLength(url):
    return len(url)

# Web traffic
def web_traffic(url):
    try:
    #Filling the whitespaces in the URL if any
        url = urllib.parse.quote(url)
        pg = urllib.request.urlopen("http://data.alexa.com/data?cli=10&url=" + url).read()
        rank = BeautifulSoup(pg, "xml").find("REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return -1
    return rank

# Survival time of domain
# todo how long   
def domainAge(domain_name):
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
        try:
            creation_date = datetime.strptime(creation_date,'%Y-%m-%d %H:%M:%S')
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d %H:%M:%S")
        except:
            return 1
    
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        creation_date = datetime.strptime(str(creation_date[0]),'%Y-%m-%d %H:%M:%S')
        expiration_date = datetime.strptime(str(expiration_date[0]),'%Y-%m-%d %H:%M:%S')
        ageofdomain = abs((expiration_date - creation_date).days)
    
        if ((ageofdomain/30) < 6):
            age = 1
        else:
            age = 0

    else:
        ageofdomain = abs((expiration_date - creation_date).days)
    if ((ageofdomain/30) < 6):
        age = 1
    else:
        age = 0
    return age




insert_sql = []

conn = connect_mysql.connect_mysql()
time = datetime.now()

sql = 'create table if not exists ' + connect_mysql.TABLE_FEATURES + \
    ' (phish_id int,domain varchar(255), haveip int, haveat int, '\
    ' length int, flength int,wsla int, hyphen int, webtraffic int,'\
    ' explan varchar(1024), isphish int ,updatetime datetime);'

with conn.cursor() as cursor:
    cursor.execute(sql)


#analyze
sql = 'select o.phish_id,o.url from ' + connect_mysql.TABLE_OVPHISH + ' as o '\
    'inner join ' + connect_mysql.TABLE_VISIT + ' as v '\
    'on (o.phish_id = v.phish_id) ' \
    'left join ' + connect_mysql.TABLE_FEATURES + ' as f '\
    'on (o.phish_id = f.phish_id) '\
    'where v.isalive = true and f.phish_id is null '\
    'limit 200'


with conn.cursor() as cursor:
    cursor.execute(sql)

    row  = cursor.fetchone()

    while row is not None:
        pid = row[0] 
        url = row[1]
        dom= getDomain(url)
        leng = getLength(url)
        

        if leng >= 54:
            flen = 1
        else:
            flen = 0

        if url.count('//') > 1:
            wsla = 1
        else:
            wsla = 0

        if url.count('-') > 0:
            hyph = 1
        else:
            hyph = 0

        sql = 'insert into ' + connect_mysql.TABLE_FEATURES + \
        ' (phish_id, domain, haveip, haveat,'\
        ' length, flength, wsla, hyphen, webtraffic, '\
        ' explan, isphish, updatetime) '\
        'values '\
        '(%s, \'%s\', %s, %s,'\
        ' %s, %s, %s, %s, %s,"",0, \'%s\');'\
        % (pid, dom, haveIP(dom), haveAt(url), \
        leng,flen,wsla,hyph,web_traffic(dom),\
        time.strftime('%Y-%m-%d %H:%M:%S'))

        insert_sql.append(sql)

        row  = cursor.fetchone()

i = 0

with conn.cursor() as cursor:
    
    for sql in insert_sql:
        cursor.execute(sql)
        i = i + 1

    conn.commit()

conn.close()

print('analyze ok(%s)' % i)