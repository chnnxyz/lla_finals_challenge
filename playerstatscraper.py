# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 12:25:10 2020
Web scrapes gamepedia draft pages
@author: Santiago "Cohenn" Ruiz de Aguirre
"""


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

n_rows=0
n_columns=0
column_names=[]
# Download chromedriver and set your directory here
driver=webdriver.Chrome("C:\\Users\\santi\\chromedriver.exe")
# Set lol gamepedia link here
driver.get("https://lol.gamepedia.com/LLA/2020_Season/Opening_Season/Player_Statistics")
content=driver.page_source
soup=BeautifulSoup(content)

tbl=soup.findAll("tbody")
for i, table in enumerate(tbl):
    print("#"*10 + "Table {}".format(i) + '#'*10)
    print(table.text[:100])
    print('.'*80)
print("#"*80)

player=[]
gm=[]
w=[]
l=[]
wr=[]
k=[]
d=[]
a=[]
kdar=[]
cs=[]
cspm=[]
g=[]
gpm=[]
kpar=[]
ks=[]
gs=[]
cpool=[]


table = soup.find(lambda tag: tag.name=='div' and tag.has_attr('class') and tag['class']=="wide-content-scroll")
table2=BeautifulSoup(str(soup.find_all("tbody")[10:]))


for tr in table2.find_all("tr")[0:]:
    tds=tr.find_all("td")
    if not tds:
        continue
    player.append(str(tds[1]))
    gm.append(str(tds[2]))
    w.append(str(tds[3]))
    l.append(str(tds[4]))
    wr.append(str(tds[5]))
    k.append(str(tds[6]))
    d.append(str(tds[7]))
    a.append(str(tds[8]))
    kdar.append(str(tds[9]))
    cs.append(str(tds[10]))
    cspm.append(str(tds[11]))
    g.append(str(tds[12]))
    gpm.append(str(tds[13]))
    kpar.append(str(tds[14]))
    ks.append(str(tds[15]))
    gs.append(str(tds[16]))
    cpool.append(str(tds[17]))
    
def cleanhtml(x):
    cleanr=re.compile("<.*?>")
    clean=re.sub(cleanr,"",x)
    return clean

def cleanhtml2(x):
    cleanr=re.compile("<.*?>")
    clean=re.sub(cleanr,"",x)
    clean=clean.replace("\xa0","").lower()
    clean=clean.replace("%","")
    #clean=clean.replace("k","")
    return clean

def cleanhtml3(x):
    cleanr=re.compile("<.*?>")
    clean=re.sub(cleanr,"",x)
    clean=clean.replace("\xa0","").lower()
    clean=clean.replace("%","")
    clean=clean.replace("k","")
    return clean

playerc=pd.Series(list(map(cleanhtml2,player)))
gmc=pd.Series(list(map(int,list(map(cleanhtml2,gm)))))
wc=pd.Series(list(map(int,list(map(cleanhtml2,w)))))
lc=pd.Series(list(map(int,list(map(cleanhtml2,w)))))
wrc=pd.Series(list(map(cleanhtml2,wr))).replace("-",np.nan).astype(float)
kc=pd.Series(list(map(cleanhtml2,k))).replace("-",np.nan).astype(float)
dc=pd.Series(list(map(cleanhtml2,d))).replace("-",np.nan).astype(float)
ac=pd.Series(list(map(cleanhtml2,a))).replace("-",np.nan).astype(float)
kdarc=pd.Series(list(map(cleanhtml2,kdar))).replace("-",np.nan).astype(float)
csc=pd.Series(list(map(cleanhtml2,cs))).replace("-",np.nan).astype(float)
cspmc=pd.Series(list(map(cleanhtml2,cspm))).replace("-",np.nan).astype(float)
gc=pd.Series(list(map(cleanhtml3,g))).replace("-",np.nan).astype(float)*1000
gpmc=pd.Series(list(map(cleanhtml2,gpm))).replace("-",np.nan).astype(float)
kparc=pd.Series(list(map(cleanhtml2,kpar))).replace("-",np.nan).astype(float)/100
ksc=pd.Series(list(map(cleanhtml2,ks))).replace("-",np.nan).astype(float)/100
gsc=pd.Series(list(map(cleanhtml2,gs))).replace("-",np.nan).astype(float)/100
cpc=pd.Series(list(map(int,list(map(cleanhtml2,cpool)))))

data=pd.concat([playerc,gmc,wc,lc,wrc,kc,dc,ac,
                kdarc,csc,cspmc,gc,gpmc,kparc,ksc,gsc,cpc],axis=1)
data.columns="""
player
games
wins
losses
winrate
kills
deaths
assists
kdar
cs
cspm
gold
gpm
killpart
killshare
goldhsare
champpool
""".split()

data.to_csv("LLA_playerstats_regular.csv")

