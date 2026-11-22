import json,os,urllib.request as U
V=[0,100,320,330,500,975,0]
S="aaaaaaaakkkkkkkkcceggeccbbcffcbbaaaeeaaab98aa89bbcc66ccbaaaaaaaa0244442026aaaa624acddca44bdeedb44adeeda44bcddcb426abba6202444420688888868aaaaaa88abccba88bbccbb88acccca88cccccc88baaaab868888886422002244220022442200224422002246442244686666668eeaaaaeeegcaacge"
S=S[:192]+"a"*128+S[192:]
P=[[(int(S[i*64+q^56],21)-10)*5 for q in range(64)]for i in range(6)]
Q=[i for i in range(128)if not i&0x88]
K=[-33,-31,-18,-14,14,18,31,33]
G=[-17,-15,15,17];O=[-16,-1,1,16];K8=G+O
M={0:2,7:1,4:3,112:8,119:4,116:12}
X=[0]*128;H=[0,0];NC=5e3
def fp(fen):
 global Y,R,Z
 q=fen.split();s=112;X[:]=[0]*128
 for c in q[0]:
  if c=="/":s-=24
  elif c.isdigit():s+=int(c)
  else:
   v="PNBRQKpnbrqk".index(c)%6+1
   if c>"Z":v=-v
   X[s]=v
   if abs(v)==6:H[v<0]=s
   s+=1
 Y=1 if q[1]=="w"else -1
 R=sum(1<<i for i,x in enumerate("KQkq")if x in q[2]);Z=-1
 if q[3]!="-":Z=(int(q[3][1])-1)*16+ord(q[3][0])-97
def ak(s,by):
 if any(not(s+o)&0x88 and X[s+o]==by for o in(-17*by,-15*by)):return True
 for ds,ks,sl in((K,"2",0),(K8,"6",0),(G,"35",1),(O,"45",1)):
  for o in ds:
   t=s+o
   while not t&0x88:
    p=X[t]
    if p:
     if p*by>0 and str(abs(p))in ks:return True
     break
    if not sl:break
    t+=o
 return False
def gn():
 ms=[]
 ad=lambda s,t:ms.extend([(s,t,pr)for pr in(5,4,3,2)]if t>>4 in(0,7)else[(s,t,0)])
 for s in Q:
  p=X[s]
  if p*Y<=0:continue
  a=abs(p)
  if a==1:
   d=16*Y
   if not X[s+d]:
    ad(s,s+d)
    if s>>4==3.5-2.5*Y and not X[s+2*d]:ms.append((s,s+2*d,0))
   for o in(15,17):
    t=s+o*Y
    if t&0x88:continue
    tp=X[t]
    if tp*Y<0:ad(s,t)
    elif t==Z:ms.append((s,t,0))
  else:
   ds,sl=((K,0),(G,1),(O,1),(K8,1),(K8,0))[a-2]
   for o in ds:
    t=s+o
    while not t&0x88:
     tp=X[t]
     if tp:
      if tp*Y<0:ms.append((s,t,0))
      break
     ms.append((s,t,0))
     if not sl:break
     t+=o
   if a==6 and s==60-56*Y:
    for dsg,bit,rq in((1,1,3),(-1,2,-4))if Y>0 else((1,4,3),(-1,8,-4)):
     if R&bit and X[s+rq]==4*Y and not(X[s+dsg]or X[s+2*dsg]or(rq<0 and X[s-3]))and not any(ak(s+x*dsg,-Y)for x in(0,1,2)):ms.append((s,s+2*dsg,0))
 return ms
def rv(f,t):
 if abs(t-f)==2:r=f+(3 if t>f else -4);q=f+(1 if t>f else -1);X[q],X[r]=X[r],X[q]
def ma(m):
 global Y,R,Z
 f,t,pr=m;p=X[f];cap=X[t];ec=0
 if abs(p)==1 and t==Z and not cap and f&7!=t&7:ec=X[z:=t-16*Y];X[z]=0
 u=(cap,ec,R,Z);X[t]=p if not pr else pr*Y;X[f]=0
 if abs(p)==6:H[Y<0]=t;rv(f,t)
 R&=~(M.get(f,0)|M.get(t,0));Z=(f+t)//2 if abs(p)==1 and abs(t-f)==32 else -1;Y=-Y
 return u
def um(m,u):
 global Y,R,Z
 f,t,pr=m;cap,ec,R,Z=u;Y=-Y;p=Y if pr else X[t]
 X[f]=p;X[t]=cap
 if ec:X[t-16*Y]=ec
 if abs(p)==6:H[Y<0]=f;rv(f,t)
def vv():
 return Y*sum((V[abs(p)]+P[abs(p)-1][i^(p>>31&56)])*((p>0)*2-1)for i,s in enumerate(Q)if(p:=X[s]))
ok=lambda m:V[abs(X[m[0]])]//16-10*V[abs(X[m[1]])]-V[m[2]]
def lm(ms):
 for m in ms:
  u=ma(m)
  if ak(H[Y>0],Y):um(m,u);continue
  try:yield m
  finally:um(m,u)
def ng(d,a,b):
 global J
 J+=1
 if J>=NC:return vv()
 if d<=0:
  ic=ak(H[Y<0],-Y)
  if not ic and(a:=max(a,vv()))>=b:return a
 ms=list(lm(sorted(gn(),key=ok)))
 if d<=0 and not ic:ms=[m for m in ms if X[m[1]]or m[2]or m[1]==Z]
 if not ms:return -100000-d if ak(H[Y<0],-Y)else a*(d<=0)
 for m in ms:
  u=ma(m);sc=-ng(d-1,-b,-a);um(m,u)
  if sc>a:a=sc
  if a>=b:break
 return a
def uc(m):
 f,t,pr=m;s=chr(97+(f&7))+str(1+(f>>4))+chr(97+(t&7))+str(1+(t>>4))
 return s+("nbrq"[pr-2]if pr else"")
def ch(fen,legal):
 global J
 fp(fen);ms=list(lm(gn()))
 ms=[m for m in ms if uc(m)in legal]or ms
 bm=ms[0]
 for d in range(64):
  J=0;a=-9**9;cur=bm
  for m in ms:
   u=ma(m);sc=-ng(d-1,-9**9,-a);um(m,u)
   if sc>a:a=sc;cur=m
   if J>=NC:break
  if J>=NC:break
  bm=cur;ms.remove(cur);ms.insert(0,cur)
 return uc(bm)
URL=os.environ["MAKEFUN_ENV_URL"]
def po(p,d={}):
 return json.load(U.urlopen(U.Request(URL+p,data=json.dumps(d).encode())))
g=po("/game")
while g["status"]!="done":
 while g["status"]=="your_move":g=po("/move",{"game":g["game"],"move":ch(g["fen"],g["legal_moves"])})
 g=po("/game")
