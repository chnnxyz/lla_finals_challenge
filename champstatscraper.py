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
driver.get("https://lol.gamepedia.com/LLA/2020_Season/Opening_Season/Champion_Statistics")
content=driver.page_source
soup=BeautifulSoup(content)

tbl=soup.findAll("tbody")
for i, table in enumerate(tbl):
    print("#"*10 + "Table {}".format(i) + '#'*10)
    print(table.text[:100])
    print('.'*80)
print("#"*80)

champion=[]
gm=[]
pbp=[]
ban=[]
pck=[]
byteams=[]
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


table = soup.find(lambda tag: tag.name=='div' and tag.has_attr('class') and tag['class']=="wide-content-scroll")
table2=BeautifulSoup(str(soup.find_all("tbody")[10:]))


for tr in table2.find_all("tr")[0:]:
    tds=tr.find_all("td")
    if not tds:
        continue
    champion.append(str(tds[0]))
    gm.append(str(tds[1]))
    pbp.append(str(tds[2]))
    ban.append(str(tds[3]))
    pck.append(str(tds[4]))
    byteams.append(str(tds[5]))
    w.append(str(tds[6]))
    l.append(str(tds[7]))
    wr.append(str(tds[8]))
    k.append(str(tds[9]))
    d.append(str(tds[10]))
    a.append(str(tds[11]))
    kdar.append(str(tds[12]))
    cs.append(str(tds[13]))
    cspm.append(str(tds[14]))
    g.append(str(tds[15]))
    gpm.append(str(tds[16]))
    kpar.append(str(tds[17]))
    ks.append(str(tds[18]))
    gs.append(str(tds[19]))
    
def cleanhtml(x):
    cleanr=re.compile("<.*?>")
    clean=re.sub(cleanr,"",x)
    return clean

def cleanhtml2(x):
    cleanr=re.compile("<.*?>")
    clean=re.sub(cleanr,"",x)
    clean=clean.replace("\xa0","").lower()
    clean=clean.replace("%","")
    clean=clean.replace("-","nan")
    return clean

championc=pd.Series(list(map(cleanhtml2,champion)))
gmc=pd.Series(list(map(int,list(map(cleanhtml2,gm)))))
pbpc=list(map(float,list(map(cleanhtml2,pbp))))
pbpc=pd.Series(list(map(lambda x:x/100,pbpc)))
banc=pd.Series(list(map(cleanhtml2,ban))).replace("-",np.nan).astype(float)
pckc=pd.Series(list(map(cleanhtml2,pck))).replace("-",np.nan).astype(float)
byteamsc=pd.Series(list(map(cleanhtml2,byteams))).replace("-",np.nan).astype(float)
wc=pd.Series(list(map(int,list(map(cleanhtml2,w)))))
lc=pd.Series(list(map(int,list(map(cleanhtml2,w)))))
wrc=pd.Series(list(map(cleanhtml2,wr))).replace("-",np.nan).astype(float)
kc=pd.Series(list(map(cleanhtml2,k))).replace("-",np.nan).astype(float)
dc=pd.Series(list(map(cleanhtml2,d))).replace("-",np.nan).astype(float)
ac=pd.Series(list(map(cleanhtml2,a))).replace("-",np.nan).astype(float)
kdarc=pd.Series(list(map(cleanhtml2,kdar))).replace("-",np.nan).astype(float)
csc=pd.Series(list(map(cleanhtml2,cs))).replace("-",np.nan).astype(float)
cspmc=pd.Series(list(map(cleanhtml2,cspm))).replace("-",np.nan).astype(float)
gc=pd.Series(list(map(cleanhtml2,g))).replace("-",np.nan).astype(float)
gpmc=pd.Series(list(map(cleanhtml2,gpm))).replace("-",np.nan).astype(float)
kparc=pd.Series(list(map(cleanhtml2,kpar))).replace("-",np.nan).astype(float)/100
ksc=pd.Series(list(map(cleanhtml2,ks))).replace("-",np.nan).astype(float)/100
gsc=pd.Series(list(map(cleanhtml2,gs))).replace("-",np.nan).astype(float)/100

data=pd.concat([championc,gmc,pbpc,banc,pckc,byteamsc,wc,lc,wrc,kc,dc,ac,
                kdarc,csc,cspmc,gc,gpmc,kparc,ksc,gsc],axis=1)
data.columns="""
champion
games
presence
bans
picks
byteams
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
""".split()

data.to_csv("LLA_champstats_regular.csv")

