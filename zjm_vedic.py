# -*- coding: utf-8 -*-
import swisseph as swe
from datetime import datetime, timedelta

swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
LAT, LON = 23.08, 113.16  # 广州

SIGNS=["白羊 Mesha","金牛 Vrishabha","双子 Mithuna","巨蟹 Karka","狮子 Simha","处女 Kanya",
       "天秤 Tula","天蝎 Vrishchika","射手 Dhanu","摩羯 Makara","水瓶 Kumbha","双鱼 Meena"]
S3="Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi".split()
GRAHA=[("太阳 Surya",swe.SUN),("月亮 Chandra",swe.MOON),("火星 Mangala",swe.MARS),
       ("水星 Budha",swe.MERCURY),("古鲁 Guru",swe.JUPITER),("金星 Shukra",swe.VENUS),
       ("土星 Shani",swe.SATURN)]
NAK=["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
     "Magha","P.Phalguni","U.Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
     "Mula","P.Ashadha","U.Ashadha","Shravana","Dhanishta","Shatabhisha","P.Bhadra","U.Bhadra","Revati"]
NAK_LORD=["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]*3
ORDER=["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
YRS={"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,"Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}

def nav(lon):
    s=int(lon)//30; n=int((lon%30)/(30/9.0)); mode=s%3
    base={0:s,1:(s+8)%12,2:(s+4)%12}[mode]
    return (base+n)%12

def d10(lon):
    s=int(lon)//30; part=int((lon%30)//3)
    start=s if s%2==0 else (s+8)%12
    return (start+part)%12

# 上升窗口检查
for hh,mm in [(16,0),(16,30),(17,0)]:
    dt=datetime(2001,12,27,hh,mm)-timedelta(hours=8)
    jd=swe.julday(dt.year,dt.month,dt.day,dt.hour+dt.minute/60.0)
    asc=swe.houses_ex(jd,LAT,LON,b"P",swe.FLG_SIDEREAL)[1][0]
    print(f"{hh:02d}:{mm:02d} 上升 {asc:6.2f} -> {S3[int(asc)//30]} {asc%30:.2f}°")

# 基准 16:30
dt=datetime(2001,12,27,16,30)-timedelta(hours=8)
jd=swe.julday(dt.year,dt.month,dt.day,dt.hour+dt.minute/60.0)
print("\n=== D1 九曜 (2001-12-27 16:30 北京, Lahiri) ===")
lons={}
for name,pid in GRAHA:
    xx,_=swe.calc_ut(jd,pid,swe.FLG_SIDEREAL|swe.FLG_SPEED)
    lon=xx[0]; spd=xx[3]; lons[pid]=lon
    print(f"{name:14s} {lon%30:6.2f}° {SIGNS[int(lon)//30]:14s}"+("  逆行R" if spd<0 else ""))
rahu=swe.calc_ut(jd,swe.MEAN_NODE,swe.FLG_SIDEREAL)[0][0]
ketu=(rahu+180)%360
print(f"{'罗睺 Rahu':14s} {rahu%30:6.2f}° {SIGNS[int(rahu)//30]}")
print(f"{'计都 Ketu':14s} {ketu%30:6.2f}° {SIGNS[int(ketu)//30]}")

seven=[(lons[p]%30,n) for n,p in GRAHA]
seven.sort(reverse=True)
print("\n度数排序(卡拉卡):",[(n,f"{d:.1f}") for d,n in seven])
print("Atmakaraka:",seven[0][1]," Amatyakaraka:",seven[1][1])

moon=lons[swe.MOON]; span=360/27.0
nidx=int(moon//span); within=moon-nidx*span; pada=int(within//(span/4))+1
print(f"\n月亮宿: {NAK[nidx]} 第{pada}足  宿主 {NAK_LORD[nidx]}  宿内 {within:.2f}°  距宿尾 {span-within:.2f}°")

print("\n=== D9 Navamsa / D10 Dasamsa ===")
for name,pid in GRAHA:
    lon=lons[pid]
    print(f"{name:14s} D1 {S3[int(lon)//30]:2s}{lon%30:5.1f}  D9 {S3[nav(lon)]:2s}  D10 {S3[d10(lon)]:2s}")
print(f"{'罗睺 Rahu':14s} D1 {S3[int(rahu)//30]:2s}{rahu%30:5.1f}  D9 {S3[nav(rahu)]:2s}  D10 {S3[d10(rahu)]:2s}")

lord=NAK_LORD[nidx]; frac=within/span
first_left=YRS[lord]*(1-frac)
birth=datetime(2001,12,27)
cur=birth; li=ORDER.index(lord)
today=datetime(2026,9,18)
md_list=[]
for k in range(9):
    nm=ORDER[(li+k)%9]; yrs=first_left if k==0 else YRS[nm]
    end=cur+timedelta(days=yrs*365.2425)
    md_list.append((nm,cur,end)); cur=end
print("\n=== Vimshottari 大运 ===")
for nm,s,e in md_list:
    mk=" <<<" if s<=today<e else ""
    print(f"{nm:8s} {s:%Y-%m} ~ {e:%Y-%m}{mk}")

for nm,s,e in md_list:
    if s<=today<e:
        li2=ORDER.index(nm); c2=s
        print(f"\n=== {nm} 大运内小运 ===")
        for j in range(9):
            sub=ORDER[(li2+j)%9]; seg=(e-s).days*YRS[sub]/120.0
            e2=c2+timedelta(days=seg)
            mk=" <<<" if c2<=today<e2 else ""
            print(f"{nm}/{sub:8s} {c2:%Y-%m-%d} ~ {e2:%Y-%m-%d}{mk}")
            c2=e2
        nxt=ORDER[(li2+1)%9]; ns=e; li3=ORDER.index(nxt); c3=ns
        print(f"\n=== 下一大运 {nxt} 小运(前5段) ===")
        for j in range(5):
            sub=ORDER[(li3+j)%9]; seg=YRS[nxt]*YRS[sub]/120.0*365.2425
            e3=c3+timedelta(days=seg)
            print(f"{nxt}/{sub:8s} {c3:%Y-%m-%d} ~ {e3:%Y-%m-%d}")
            c3=e3
