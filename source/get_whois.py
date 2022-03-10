#modules
import time
import whois

# my modules
import connect_mysql

def sani(o):
    if type(o) is list:
        return(rep_quote(",".join(o)))
    elif o is None:
        return 'None'
    else:
        return rep_quote(o)

def unld(o):
    ret = ''
    if type(o) is list:
        for d in o:
            if ret != '': ret = ret + ','
            ret = ret +  d.strftime('%Y-%m-%d %H:%M:%S')
    elif o is None:
        ret = '' 
    else:
        ret = o.strftime('%Y-%m-%d %H:%M:%S')
    
    return ret 

def rep_quote(s):
    return s.replace('\'','\\\'')

def check_whois(url):

    whois_info = whois.whois(url)

    base_sql = 'insert into '+ connect_mysql.TABLE_WHOIS + \
    '(domain, registrar, whois_server'\
    ',referral_url, updated_date, creation_date, expiration_date'\
    ',name_servers, status, emails, dnssec'\
    ',name, org, address, city'\
    ',state, zipcode, country)'\
    'values '
    
    sql = base_sql + '(\'%s\',\'%s\',\'%s\''\
        ',\'%s\',\'%s\',\'%s\',\'%s\''\
        ',\'%s\',\'%s\',\'%s\',\'%s\''\
        ',\'%s\',\'%s\',\'%s\',\'%s\''\
        ',\'%s\',\'%s\',\'%s\')'\
        % (domain,whois_info.registrar, whois_info.whois_server\
        ,whois_info.referral_url, unld(whois_info.updated_date), unld(whois_info.creation_date), unld(whois_info.expiration_date)\
        ,sani(whois_info.name_servers), sani(whois_info.status), sani(whois_info.emails), sani(whois_info.dnssec)\
        ,sani(whois_info.name), sani(whois_info.org), sani(whois_info.address), sani(whois_info.city)\
        ,sani(whois_info.state), sani(whois_info.zipcode), sani(whois_info.country))

    return sql


insert_sql = []
conn = connect_mysql.connect_mysql()

sql = 'create table if not exists ' + connect_mysql.TABLE_WHOIS + \
    '(domain_id int NOT NULL auto_increment, domain varchar(255), registrar varchar(255), whois_server varchar(255) '\
    ',referral_url varchar(255), updated_date varchar(255), creation_date varchar(255), expiration_date varchar(255)'\
    ',name_servers varchar(500), status varchar(1000), emails varchar(1000), dnssec varchar(255)'\
    ',name varchar(500), org varchar(500), address varchar(500), city varchar(500)'\
    ',state varchar(500), zipcode varchar(500), country varchar(500) ,primary key(domain_id))'

with conn.cursor() as cursor:
    cursor.execute(sql)

sql = 'select f.domain from '  + connect_mysql.TABLE_FEATURES + ' as f '\
    'left join ' + connect_mysql.TABLE_WHOIS + ' as w '\
    'on (f.domain = w.domain) '\
    'where w.domain is null '\
    'group by f.domain '\
    'limit 10'

with conn.cursor() as cursor:
    cursor.execute(sql)

    row = cursor.fetchone()

    while row is not None:
        domain = row[0]
        err = False

        time.sleep(1)
        try:
            
            sql = check_whois(domain)

            insert_sql.append(sql)

        except Exception as e:
            print('error:%s' % domain)
            print(e)
            err = True
            pass

        if err == True:
            try:
                test_domain = domain[(domain.find('.')+1):]
                sql = check_whois(test_domain)
                insert_sql.append(sql)

            except:
                print('error:%s' % test_domain)
                pass

        row = cursor.fetchone()

with conn.cursor() as cursor:    
    for sql in insert_sql:    
        cursor.execute(sql)
    conn.commit()

conn.close()

print('whois ok')

    
