import pymysql

TABLE_OVPHISH = 'phishtank.ovphish'
TABLE_OPENPH = 'phishtank.openphish'
TABLE_VISIT = 'phishtank.visit'
TABLE_FEATURES = 'phishtank.features'
TABLE_WHOIS = 'phishtank.whois'
TABLE_IPWHO = 'phishtank.ipwhois'
TABLE_TEMP = 'phishtank.temp'
TABLE_CERT = 'phishtank.certificate'

def connect_mysql():
    conn = pymysql.connect( host="127.0.0.1",
                        port=3306 ,
                        db="phishtank",
                        user="root",
                        password="%YOURPASSWORD%")
    
    return conn

