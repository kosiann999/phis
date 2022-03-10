# modules
import pandas
import pymysql

# my modules
import web_crawler
import connect_mysql

def yesno_bool(s):
    return s.lower() in ["true", "t", "yes", "1"]

def rep_quote(s):
    return s.replace('\'','\\\'')


url = 'http://data.phishtank.com/data/online-valid.csv'

# test
#path = './data.phishtank.com/data/online-valid.csv'
path = web_crawler.download_file(url)

dt = pandas.read_csv(path)

conn = connect_mysql.connect_mysql()

# create table
with conn.cursor() as cursor:

    sql = 'create table if not exists ' + connect_mysql.TABLE_OVPHISH + \
        '(phish_id int ,url varchar(2083),phish_detail_url varchar(2083),submission_time datetime,'\
        'verified boolean,verification_time datetime,online boolean,target varchar(512));'
    cursor.execute(sql)

    sql = 'create table if not exists ' + connect_mysql.TABLE_TEMP + \
        '(phish_id int ,url varchar(2083),phish_detail_url varchar(2083),submission_time datetime,'\
        'verified boolean,verification_time datetime,online boolean,target varchar(512));'
    cursor.execute(sql)

    

with conn.cursor() as cursor:

    for index,data in dt.iterrows():

        sql = 'insert into ' + connect_mysql.TABLE_TEMP + \
            '(phish_id,url,phish_detail_url,submission_time,verified,'\
            'verification_time,online,target)'\
            'values'\
            '(%s,\'%s\',\'%s\',\'%s\',%s,\'%s\',%s,\'%s\');'\
            %(data.phish_id,rep_quote(data.url),data.phish_detail_url,data.submission_time,yesno_bool(data.verified),\
            data.verification_time,yesno_bool(data.online), rep_quote(data.target)) 
        try:
            cursor.execute(sql)
        except:
            #print('error(%s)' % sql)
            pass

    conn.commit()

    sql = 'insert into ' +  connect_mysql.TABLE_OVPHISH  + '(phish_id,url,phish_detail_url,submission_time,verified,verification_time,online,target) '\
        'select t.phish_id,t.url,t.phish_detail_url,t.submission_time,t.verified,t.verification_time,t.online,t.target '\
        'from phishtank.temp as t '\
        'left join '\
        'phishtank.ovphish '\
        'on (t.phish_id = ovphish.phish_id) '\
        'where ovphish.phish_id is null ;'\

    cursor.execute(sql)

    sql = 'drop table ' + connect_mysql.TABLE_TEMP + ';'
    
    cursor.execute(sql)
          
    conn.commit()

conn.close()

print('ok')


