# modules
from datetime import datetime
import pathlib

# my modules
import web_crawler
import connect_mysql

insert_sql = []


# select 
conn = connect_mysql.connect_mysql()
time = datetime.now()

with conn.cursor() as cursor:

    sql = 'create table if not exists ' + connect_mysql.TABLE_VISIT + \
        ' (phish_id int,isalive boolean,savepath varchar(512),visitdate datetime);'

    cursor.execute(sql)
    # for
    sql = 'select o.phish_id,o.url from ' + connect_mysql.TABLE_OVPHISH + ' as o '\
        ' left join ' + connect_mysql.TABLE_VISIT +  ' as v '\
        ' on (o.phish_id = v.phish_id) '\
        ' where v.phish_id is null '\
        ' order by verification_time desc'\
        ' limit 10'
    cursor.execute(sql)

    row = cursor.fetchone()

    while row is not None:
        #get
        pid = row[0]
        url = row[1]
        
        # download 
        try:
            isalive = web_crawler.analize_html(url)
        except:
            isalive = False
            pass

        if isalive == True:
            #スクリーンショット
            #web_crawler.get_screen(url)
            try:                    
                web_crawler.get_screen(url)
            except Exception as e:
                print(e)
                pass
            
        savepath = web_crawler.WORKDIR + web_crawler.get_md5hs(url)
        savepath = str((pathlib.Path(savepath)).resolve())
        savepath = savepath.replace('\\','/')

        # insert into
        sql = 'insert into ' + connect_mysql.TABLE_VISIT +\
            '(phish_id, isalive, savepath, visitdate) '\
            'values '\
            '(%s,%s,\'%s\',\'%s\')'\
            % (pid,isalive,savepath,time.strftime('%Y-%m-%d %H:%M:%S'))

        insert_sql.append(sql)

        row = cursor.fetchone()

    for sql in insert_sql:
        cursor.execute(sql)

    conn.commit()

conn.close()


