1.環境準備（必須）

　Pythonのインストール Ver.3.X
	https://www.python.org/downloads/

　Microsoft Visual C++ 2019 Redistributable Package (x64)のインストール
　※　MySQLのインストール前に必要

　MySQL（Community Edition）のインストール
　※　要Oracleアカウント
	https://dev.mysql.com/downloads/



2.環境準備（任意）

　システム環境変数（Path）の追加（Windowsの場合）
	C:\Users\(ユーザー名)\AppData\Local\Programs\Python\Python310
	C:\Users\(ユーザー名)\AppData\Local\Programs\Python\Python310\Scripts

　開発環境（IDE）のインストール
　Visual Studio Code
	https://azure.microsoft.com/ja-jp/products/visual-studio-code/


3.ライブラリの追加

pip install pandas
pip install pymysql
pip install python-whois
pip install pyOpenSSL
pip install beautifulsoup4
pip install lxml
pip install selenium
pip install chromedriver_binary==X.X.X.X.X
※　X.X.X.X.X = Chromeのバージョンに合わせる

4.例外設定の追加

　作業フォルダは、ウイルス対策ソフト、Windows Defenderの例外として設定

5.ファイル構成

　web_crawler.py	…Web巡回用モジュール
　connect_mysql.py	…データベース接続モジュール
　
　get_phishtank.py	…①　PhishTankからCSVファイル取得
　down_file.py		…②　ファイルダウンロード
　get_whois.py		…③　whois情報を取得
　analyze_features.py	…④　特徴量抽出（セキュリティの観点から一部のみ公開）

　


