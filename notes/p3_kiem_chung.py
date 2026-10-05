"""Kiểm chứng P3; không thay src/atpg/podem.py của P5.
Chạy: python3 notes/p3_kiem_chung.py. Chỉ thư viện chuẩn.
Phần mô phỏng nhị phân dưới đây tách biệt với tham chiếu tìm kiếm.
"""
from itertools import product
PI=['1','2','3','6','7']; PO=['22','23']
G={'10':['1','3'],'11':['3','6'],'16':['2','11'],'19':['11','7'],'22':['10','16'],'23':['16','19']}
pairs={'0':(0,0),'1':(1,1),'D':(1,0),"D'":(0,1),'X':(None,None)}
TYPES=dict.fromkeys(G,'NAND')
def gate(kind,a):
 # Mô phỏng ba giá trị cho tham chiếu thứ tự quyết định.
 if kind=='NOT': return None if a[0] is None else 1-a[0]
 if kind in ('AND','NAND'):
  x=0 if 0 in a else None if None in a else 1
 else:
  x=1 if 1 in a else None if None in a else 0
 return None if x is None else 1-x if kind in ('NAND','NOR') else x
def sim(p,f):
 v=dict(p)
 for n in PI+list(G):
  if n in G:
   a=[pairs[v[i]] for i in G[n]]; t=tuple(gate(TYPES[n],[i[k] for i in a]) for k in (0,1));v[n]=next((s for s,pair in pairs.items() if pair==t),'X')
  if n==f[0]:
   good=pairs[v[n]][0]; t=(good,f[1]);v[n]=next((s for s,pair in pairs.items() if pair==t),'X')
 return v

def run(f):
 p=dict.fromkeys(PI,'X'); rows=[]; flips=0
 def front(v):return [n for n,ins in G.items() if v[n]=='X' and any(v[i] in ('D',"D'") for i in ins)]
 def xp(n,v):return n in PO or any(v[g]=='X' and xp(g,v) for g,ins in G.items() if n in ins)
 def state(v):
  if any(v[o] in ('D',"D'") for o in PO):return 'success'
  if v[f[0]]==str(f[1]):return 'fail'
  if v[f[0]] in ('D',"D'") and not any(xp(n,v) for n in front(v)):return 'fail'
  return 'continue'
 def rec(depth=0):
  nonlocal flips
  v=sim(p,f);s=state(v)
  if s!='continue':return s=='success'
  if v[f[0]]=='X':obj=(f[0],1-f[1])
  else:
   n=next(n for n in front(v) if xp(n,v));obj=(next(i for i in G[n] if v[i]=='X'),int(TYPES[n] in ('AND','NAND')))
  n,b=obj
  while n not in PI:
   b=1-b if TYPES[n] in ('NAND','NOR','NOT') else b;n=next(i for i in G[n] if v[i]=='X')
  for flip in [False,True]:
   if flip:flips+=1
   p[n]=str(b if not flip else 1-b);v=sim(p,f)
   rows.append({'obj':obj if not flip else None,'pi':n,'value':p[n],'flip':flip,'v':v.copy(),'front':front(v),'state':state(v),'depth':depth})
   if rec(depth+1):return True
  p[n]='X';return False
 ok=rec();return ok,p,flips,rows


def binary(pattern,fault=None):
 # Mô phỏng đầy đủ 0/1 độc lập với bảng logic năm giá trị.
 values=dict(pattern)
 for name in PI+list(G):
  if name in G:
   inputs=[values[i] for i in G[name]]
   kind=TYPES[name]
   if kind=='NAND': value=int(not all(inputs))
   elif kind=='AND': value=int(all(inputs))
   elif kind=='OR': value=int(any(inputs))
   elif kind=='NOR': value=int(not any(inputs))
   elif kind=='NOT': value=1-inputs[0]
   else: raise ValueError(kind)
   values[name]=value
  if fault and fault[0]==name: values[name]=fault[1]
 return values

def completions(pattern):
 unknown=[p for p in PI if pattern[p]=='X']
 for bits in product((0,1),repeat=len(unknown)):
  result={p:int(v) for p,v in pattern.items() if v!='X'}
  result.update(zip(unknown,bits));yield result

def detects(pattern,fault):
 good= binary(pattern);bad=binary(pattern,fault)
 return any(good[o]!=bad[o] for o in PO)

def validate_rows(rows,fault):
 # Mỗi giá trị xác định trong trace phải đúng với mọi cách điền PI X.
 checks=0
 for row in rows:
  pattern={n:('X' if row['v'][n]=='X' else str(pairs[row['v'][n]][0])) for n in PI}
  for pattern_full in completions(pattern):
   good=binary(pattern_full);bad=binary(pattern_full,fault)
   for n,value in row['v'].items():
    if value!='X':
     assert (good[n],bad[n])==pairs[value], (fault,n,row)
     checks+=1
 return checks

if __name__=='__main__':
 from pathlib import Path
 root=Path(__file__).resolve().parents[1]
 main=run(('11',0));assert main[:3]==(True,{'1':'X','2':'1','3':'0','6':'X','7':'X'},0)
 assert [r['front'] for r in main[3]]==[['16','19'],['19','23']]
 assert [(r['obj'],r['pi'],r['value']) for r in main[3]]==[(('11',1),'3','0'),(('2',1),'2','1')]
 checks=validate_rows(main[3],('11',0))
 full=list(completions(main[1]));assert len(full)==8 and all(detects(p,('11',0)) for p in full)
 all_main=[p for p in completions(dict.fromkeys(PI,'X')) if detects(p,('11',0))]
 rows=[]
 for n in PI+list(G):
  for s in [0,1]:
   fault=(n,s);ok,pattern,bt,trace=run(fault)
   exhaustive=[p for p in completions(dict.fromkeys(PI,'X')) if detects(p,fault)]
   assert ok==bool(exhaustive)
   if ok:assert all(detects(p,fault) for p in completions(pattern))
   validate_rows(trace,fault)
   rows.append(f'| {n}/SA{s} | {"".join(pattern[i] for i in PI)} | {bt} | {len(exhaustive)} |')
 assert all(run((n,s))[2]==0 for n in PI+list(G) for s in (0,1))
 main_count=len(all_main)
 PI=['a','b'];PO=['out'];G={'t':['a','b'],'n':['a'],'out':['t','n']};TYPES={'t':'OR','n':'NOT','out':'AND'}
 aux=run(('t',0));assert aux[:3]==(True,{'a':'0','b':'1'},1)
 assert [(r['pi'],r['value'],r['state']) for r in aux[3]]==[('a','1','fail'),('a','0','continue'),('b','1','success')]
 assert [(r['v']['t'],r['v']['n'],r['v']['out']) for r in aux[3]]==[('D','0','0'),('X','1','X'),('D','1','D')]
 checks+=validate_rows(aux[3],('t',0))
 detected=[p for p in completions(dict.fromkeys(PI,'X')) if detects(p,('t',0))]
 assert detected==[{'a':0,'b':1}]
 text=f'''# Kết quả kiểm chứng P3

Đã chạy `python3 notes/p3_kiem_chung.py`; mọi assertion PASS.

- c17 11/SA0: duyệt toàn bộ 32 vector; có {main_count} vector phát hiện lỗi.
- Pattern X10XX là một tập con gồm 8 vector: tất cả đều phát hiện lỗi.
- Golden trace chính: objective, PI, net và frontier khớp kết quả tham chiếu; 2 bước, 0 backtrack.
- Golden trace phụ: 3 bước, 1 backtrack; vector phát hiện duy nhất 01 trong 4 vector.
- {checks} phép so sánh cặp tốt/lỗi cho giá trị net xác định của hai golden trace trên mọi cách điền X đều đúng.
- Kiểm tra bổ sung 22 lỗi stem c17: mọi pattern tham chiếu khớp oracle nhị phân, mọi hàng trace có giá trị xác định hợp lệ. Không phát sinh backtrack theo P3-v1.
- Phạm vi không bao gồm branch fault. Không phải kết quả thực thi code P5/P6.
- Các kỳ vọng ABORTED tại giới hạn 0 được suy ra từ hợp đồng, chưa chạy trên code P5 vì chưa nhận code đó.

| Lỗi stem c17 | Pattern tham chiếu | Backtracks | Số vector phát hiện /32 |
|---|---|---:|---:|
'''+ '\n'.join(rows)+'\n'
 (root/'results/p3_kiem_chung.md').write_text(text,encoding='utf-8')
 print(text)
