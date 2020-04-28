# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 12:25:10 2020
Web scrapes gamepedia draft pages
@author: Santiago "Cohenn" Ruiz de Aguirre
"""


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

n_rows=0
n_columns=0
column_names=[]
# Download chromedriver and set your directory here
driver=webdriver.Chrome("C:\\Users\\santi\\chromedriver.exe")
# Set lol gamepedia link here
driver.get("https://lol.gamepedia.com/LLA/2020_Season/Opening_Season/Picks_and_Bans")
content=driver.page_source
soup=BeautifulSoup(content)

tbl=soup.findAll("table")
for i, table in enumerate(tbl):
    print("#"*10 + "Table {}".format(i) + '#'*10)
    print(table.text[:100])
    print('.'*80)
print("#"*80)
phase=[]
blue=[]
red=[]
score=[]
patch=[]
BB1=[]
RB1=[]
BB2=[]
RB2=[]
BB3=[]
RB3=[]
BP1=[]
RP1_2=[]
BP2_3=[]
RP3=[]
RB4=[]
BB4=[]
RB5=[]
BB5=[]
RP4=[]
BP4_5=[]
RP5=[]

table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="pbh-table")
table2=table.find_all("th")[1:]
table3=list(table2)
table3[i]=[str(table3[i]) for i in range(len(table3))]
colnames=[th.text.strip() for th in table2]

for tr in table.find_all("tr")[1:]:
    tds=tr.find_all("td")
    if not tds:
        continue
    phase.append(str(tds[0]))
    blue.append(str(tds[1]))
    red.append(str(tds[2]))
    score.append(str(tds[3]))
    patch.append(str(tds[4]))
    BB1.append(str(tds[5]))
    RB1.append(str(tds[6]))
    BB2.append(str(tds[7]))
    RB2.append(str(tds[8]))
    BB3.append(str(tds[9]))
    RB3.append(str(tds[10]))
    BP1.append(str(tds[11]))
    RP1_2.append(str(tds[12]))
    BP2_3.append(str(tds[13]))
    RP3.append(str(tds[14]))
    RB4.append(str(tds[15]))
    BB4.append(str(tds[16]))
    RB5.append(str(tds[17]))
    BB5.append(str(tds[18]))
    RP4.append(str(tds[19]))
    BP4_5.append(str(tds[20]))
    RP5.append(str(tds[21]))
scorecln=lambda x:x[4:9]    
score=list(map(scorecln,score))
wl=[]

for i in range(len(score)):
    if "pbh-winner" in blue[i]:
        wl.append("Blue")
    else:
        wl.append("Red")
# Add champions as riot adds them        
champions='aatrox ahri akali alistar amumu anivia annie aphelios ashe aurelionsol azir bard blitzcrank brand braum caitlyn camille cassiopeia chogath corki drmundo draven ekko elise evelynn ezreal fiddlesticks fiora fizz galio gangplank garen gnar gragas graves hecarim heimerdinger illaoi irelia ivern janna jarvaniv jax jayce jhin jinx kaisa kalista karma karthus kassadin katarina kayle kayn kennen khazix kindred kled kogmaw leblanc leesin leona lissandra lucian lulu lux malphite malzahar maokai masteryi missfortune mordekaiser morgana nami nasus nautilus neeko nidalee nocturne nunu olaf orianna ornn pantheon poppy pyke qiyana quinn rakan rammus reksai renekton rengar riven rumble ryze sejuani senna sett sion shaco shen shyvana sivir skarner sona soraka swain sylas syndra tahmkench taliyah talon taric teemo thresh tristana trundle tryndamere twistedfate twitch udyr urgot varus vayne veigar velkoz "vi" viktor vladimir volibear warwick wukong xayah xerath xinzhao yasuo yorick yuumi zac zed ziggs zilean zoe zyra'.split()

def bancleanup(x):
    xc=[]
    i=0
    for i in range(len(x)):
        for champ in champions:
            if str(champ) in str(x[i]):
                if champ=='"vi"':
                    xc.append("vi")
                else:
                    xc.append(champ)
        if len(xc)<(i+1):
            xc.append("nan")
    return xc
            
BB1c=bancleanup(BB1)
BB2c=bancleanup(BB2)
BB3c=bancleanup(BB3)
BB4c=bancleanup(BB4)
BB5c=bancleanup(BB5)
RB1c=bancleanup(RB1)
RB2c=bancleanup(RB2)
RB3c=bancleanup(RB3)
RB4c=bancleanup(RB4)
RB5c=bancleanup(RB5)

BP1c=bancleanup(BP1)
RP3c=bancleanup(RP3)
RP4c=bancleanup(RP4)
RP5c=bancleanup(RP5)
def dpcleanup(x):
    xc=[]
    i=0
    for i in range(len(x)):
        for champ in champions:
            if str(champ) in str(x[i]):
                if champ=='"vi"':
                    xc.append("vi")
                else:
                    xc.append(champ)
        if len(xc)<(i+1):
            xc.append("nan")
    xc1=[]
    xc2=[]
    for i in range(int(len(xc)/2)):
        xc1.append(xc[2*i])
        xc2.append(xc[2*i+1])
    return xc1,xc2

RP1c,RP2c=dpcleanup(RP1_2)
BP2c,BP3c=dpcleanup(BP2_3)
BP4c,BP5c=dpcleanup(BP4_5)

#Change patch list as necessary
s10p="10.3 10.4 10.5 10.6 10.7 10.8 10.9 10.10 10.11 10.12 10.13 10.14 10.15 10.16 10.17 10.18 10.19 10.20".split()
def patchcleanup(x):
    xc=[]
    i=0
    for i in range(len(x)):
        for patch in s10p:
            if str(patch) in str(x[i]):
                xc.append(patch)
    return xc

patchc=patchcleanup(patch)

draftdata=pd.DataFrame({
    "patch":patchc,
    "winside":wl,
    "BB1":BB1c,
    "RB1":RB1c,
    "BB2":BB2c,
    "RB2":RB2c,
    "BB3":BB3c,
    "BP1":BP1c,
    "RP1":RP1c,
    "RP2":RP2c,
    "BP2":BP2c,
    "BP3":BP3c,
    "RB4":RB4c,
    "BB4":BB4c,
    "RB5":RB5c,
    "BB5":BB5c,
    "RP4":RP4c,
    "BP4":BP4c,
    "BP5":BP5c,
    "RP5":RP5c
    })