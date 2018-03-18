#gerekli kutuphaneleri import et
import os
import subprocess
import mysql.connector
import logging


#renkleri tanimla
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#ekrani temizle ve karsilama ekrani goster
os.system("clear")
print
os.system("figlet -f smblock ORTA DOGU TEKNIK UNIVERSITESI")
print bcolors.WARNING + ("#############################################################################") + bcolors.ENDC
os.system("cat asd.txt")
print
print bcolors.WARNING + ("Bu yazilim sistem verilerini toplar ve veritabanina yazar.") + bcolors.ENDC
print bcolors.WARNING + ("Program basliyor...") + bcolors.ENDC
os.system("date")                                                              
print

#veritabani degiskenlerini tanimla [CONSTANTS]
DATABASE_NAME = 'metu_db'
TABLE_NAME    = 'makine'
#veritabani bilgilerini ayarla
db_config = {	
			'user':'root',
			'password':'toor123',
			'host':'localhost',
			'database': DATABASE_NAME,
}

#veritabanina baglan
try:
	cnx = mysql.connector.connect(**db_config)
	cursor = cnx.cursor(buffered=True)
except BaseException as e:
	print ("veritabani baglantisi saglanamadi.")
print bcolors.BOLD + DATABASE_NAME + bcolors.OKGREEN + " veritabanina baglanildi." + bcolors.ENDC

#veritabanina veri ekleyecek fonksiyon
def commit_db(parm, val):
	#Eklenecek veriler icin tablo yapisini belirle
	query = ("INSERT INTO makine "
				"(parametre, deger) "
				"VALUES (%(parametre)s, %(deger)s)")


	data = {
			'parametre':parm,
			'deger':val,
		   }

	cursor.execute(query,data)
	cnx.commit()



#parametre isimlerini belirt
par1="Sunucu ismi"
par2="Isletim Sistemi"
par3="Kernel"
par4="IP"
par5="DNS"


#parametrenin degerlerini belirt
try:
	val1=os.popen("hostname").read().strip()
	val2=os.popen("lsb_release -a | head -n3 | tail -n1 | awk '{print $2,$3}'").read().strip()
	val3=os.popen("uname -r").read().strip()
	val4=os.popen("hostname -I").read().strip()
	val5=os.popen("cat /etc/resolv.conf | grep 'nameserver ' | awk '{print $2}'").read().strip()
except BaseException as e:
	print ("bash komutlari duzgun calismadi.")
print bcolors.OKGREEN + ("bash komutlari calistirildi.") + bcolors.ENDC

#degiskenleri bir array a at
pars = []
vals = []
try:
	for i in [par1, par2, par3, par4, par5]:
		pars.append(i)

	for i in [val1, val2, val3, val4, val5]:
		vals.append(i)
except BaseException as e:
	print ("degiskenler array e yuklenemedi.")


#Once tablo icerisindekileri bosaltki eski veriler silinsin, yenileri eklensin.
try:
	truncate_table = ("truncate table makine")
	cursor.execute(truncate_table)
except BaseException as e:
	print ("tablo icerisi bosaltilamadi.")
print bcolors.OKGREEN + ("tablodaki eski degerler temizlendi.") + bcolors.ENDC



#verileri veritabanina yaz
try:
	for i in xrange(0,5):
		commit_db(pars[i],vals[i])
except BaseException as e:
	print ("veriler veritabanina yazilamadi.")
print bcolors.OKGREEN + ("sistem verileri " + bcolors.ENDC + bcolors.BOLD + TABLE_NAME + bcolors.OKGREEN + " tablosuna yazildi." ) + bcolors.ENDC


#baglantiyi kapat
try:
	cursor.close()
	cnx.close()
except BaseException as e:
	print ("veritabani baglantisi duzgun kapatilamadi.")
print bcolors.OKGREEN + ("veri tabani baglantisi kapatildi.") + bcolors.ENDC
