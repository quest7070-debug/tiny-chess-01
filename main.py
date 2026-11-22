import json,os,urllib.request as U
V=[0,100,320,330,500,975,0]
S="aaaaaaaakkkkkkkkcceggeccbbcffcbbaaaeeaaab98aa89bbcc66ccbaaaaaaaa0244442026aaaa624acddca44bdeedb44adeeda44bcddcb426abba6202444420688888868aaaaaa88abccba88bbccbb88acccca88cccccc88baaaab868888886422002244220022442200224422002246442244686666668eeaaaaeeegcaacge"
S=S[:192]+"a"*128+S[192:]
P=[[(int(S[i*64+q^56],21)-10)*5 for q in range(64)]for i in range(6)]
Q=[i for i in range(128)if not i&0x88]
K=[-33,-31,-18,-14,14,18,31,33]
G=[-17,-15,15,17];O=[-16,-1,1,16];K8=G+O
M={0:2,7:1,4:3,112:8,119:4,116:12}
B=[0]*128;W=[0,0];NC=5e3
def parse(fen):
 global T,C,E
 q=fen.split();s=112;B[:]=[0]*128
 for c in q[0]:
  if c=="/":s-=24
  elif c.isdigit():s+=int(c)
  else:
   v="PNBRQKpnbrqk".index(c)%6+1
   if c>"Z":v=-v
   B[s]=v
   if abs(v)==6:W[v<0]=s
   s+=1
 T=1 if q[1]=="w"else -1
 C=sum(1<<i for i,x in enumerate("KQkq")if x in q[2]);E=-1
 if q[3]!="-":E=(int(q[3][1])-1)*16+ord(q[3][0])-97
def atk(s,by):
 if any(not(s+o)&0x88 and B[s+o]==by for o in(-17*by,-15*by)):return True
 for ds,ks,sl in((K,"2",0),(K8,"6",0),(G,"35",1),(O,"45",1)):
  for o in ds:
   t=s+o
   while not t&0x88:
    p=B[t]
    if p:
     if p*by>0 and str(abs(p))in ks:return True
     break
    if not sl:break
    t+=o
 return False
def gen():
 ms=[]
 ad=lambda s,t:ms.extend([(s,t,pr)for pr in(5,4,3,2)]if t>>4 in(0,7)else[(s,t,0)])
 for s in Q:
  p=B[s]
  if p*T<=0:continue
  a=abs(p)
  if a==1:
   d=16*T
   if not B[s+d]:
    ad(s,s+d)
    if s>>4==3.5-2.5*T and not B[s+2*d]:ms.append((s,s+2*d,0))
   for o in(15,17):
    t=s+o*T
    if t&0x88:continue
    tp=B[t]
    if tp*T<0:ad(s,t)
    elif t==E:ms.append((s,t,0))
  else:
   ds,sl=((K,0),(G,1),(O,1),(K8,1),(K8,0))[a-2]
   for o in ds:
    t=s+o
    while not t&0x88:
     tp=B[t]
     if tp:
      if tp*T<0:ms.append((s,t,0))
      break
     ms.append((s,t,0))
     if not sl:break
     t+=o
   if a==6 and s==60-56*T:
    for dsg,bit,rq in((1,1,3),(-1,2,-4))if T>0 else((1,4,3),(-1,8,-4)):
     if C&bit and B[s+rq]==4*T and not(B[s+dsg]or B[s+2*dsg]or(rq<0 and B[s-3]))and not any(atk(s+x*dsg,-T)for x in(0,1,2)):ms.append((s,s+2*dsg,0))
 return ms
def rmv(f,t):
 if abs(t-f)==2:r=f+(3 if t>f else -4);q=f+(1 if t>f else -1);B[q],B[r]=B[r],B[q]
def mk(m):
 global T,C,E
 f,t,pr=m;p=B[f];cap=B[t];ec=0
 if abs(p)==1 and t==E and not cap and f&7!=t&7:ec=B[z:=t-16*T];B[z]=0
 u=(cap,ec,C,E);B[t]=p if not pr else pr*T;B[f]=0
 if abs(p)==6:W[T<0]=t;rmv(f,t)
 C&=~(M.get(f,0)|M.get(t,0));E=(f+t)//2 if abs(p)==1 and abs(t-f)==32 else -1;T=-T
 return u
def un(m,u):
 global T,C,E
 f,t,pr=m;cap,ec,C,E=u;T=-T;p=T if pr else B[t]
 B[f]=p;B[t]=cap
 if ec:B[t-16*T]=ec
 if abs(p)==6:W[T<0]=f;rmv(f,t)
def ev():
 return T*sum((V[abs(p)]+P[abs(p)-1][i^(p>>31&56)])*((p>0)*2-1)for i,s in enumerate(Q)if(p:=B[s]))
okey=lambda m:V[abs(B[m[0]])]//16-10*V[abs(B[m[1]])]-V[m[2]]
def lg(ms):
 for m in ms:
  u=mk(m)
  if atk(W[T>0],T):un(m,u);continue
  try:yield m
  finally:un(m,u)
def sr(d,a,b):
 global N
 N+=1
 if N>=NC:return ev()
 if d<=0:
  ic=atk(W[T<0],-T)
  if not ic and(a:=max(a,ev()))>=b:return a
 ms=list(lg(sorted(gen(),key=okey)))
 if d<=0 and not ic:ms=[m for m in ms if B[m[1]]or m[2]or m[1]==E]
 if not ms:return -100000-d if atk(W[T<0],-T)else a*(d<=0)
 for m in ms:
  u=mk(m);sc=-sr(d-1,-b,-a);un(m,u)
  if sc>a:a=sc
  if a>=b:break
 return a
def uci(m):
 f,t,pr=m;s=chr(97+(f&7))+str(1+(f>>4))+chr(97+(t&7))+str(1+(t>>4))
 return s+("nbrq"[pr-2]if pr else"")
def choose(fen,legal):
 global N
 parse(fen);ms=list(lg(gen()))
 ms=[m for m in ms if uci(m)in legal]or ms
 bm=ms[0]
 for d in range(64):
  N=0;a=-9**9;cur=bm
  for m in ms:
   u=mk(m);sc=-sr(d-1,-9**9,-a);un(m,u)
   if sc>a:a=sc;cur=m
   if N>=NC:break
  if N>=NC:break
  bm=cur;ms.remove(cur);ms.insert(0,cur)
 return uci(bm)
URL=os.environ["MAKEFUN_ENV_URL"]
def post(p,d={}):
 return json.load(U.urlopen(U.Request(URL+p,data=json.dumps(d).encode())))
g=post("/game")
while g["status"]!="done":
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
 g=post("/game")
