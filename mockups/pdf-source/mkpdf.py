import re,sys,html,base64
D="/home/user/itax/content/client-docs/"
LOGO=base64.b64encode(open("/home/user/itax/mockups/pages/assets/itax-advisors-logo-reversed.svg","rb").read()).decode()
e=lambda s:html.escape(s,quote=False)
def inl(s):
    s=e(s.strip().replace(" ¦ "," "));s=re.sub(r"\*\*(.+?)\*\*",r"<b>\1</b>",s);return s
def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]
def parse(md):
    L0=md.split("\n");L=[];k=0
    while k<len(L0):
        x=L0[k]
        if x.startswith("|") and not x.rstrip().endswith("|"):
            while k+1<len(L0) and not x.rstrip().endswith("|"):
                k+=1;x=x+" ¦ "+L0[k]
        L.append(x);k+=1
    i=0;out=[]
    while i<len(L):
        l=L[i]
        if not l.strip():i+=1;continue
        if l.startswith("|"):
            rows=[];
            while i<len(L) and L[i].startswith("|"):
                if not re.match(r"^\|[-\s|]+\|?$",L[i]):rows.append(cells(L[i]))
                i+=1
            out.append(("table",rows));continue
        out.append(("line",l.rstrip()));i+=1
    return out
def render(name,sub_title):
    md=open(D+name,encoding="utf8").read()
    blocks=parse(md);h=[];title=None;tag=None;first=True
    n=0
    for kind,v in blocks:
        if kind=="line":
            if v.startswith("# ") and title is None:
                title=v[2:].strip();continue
            if title and tag is None and re.match(r"^[A-Z0-9 &•|.\-–/']+$",v) and len(v)<60:
                tag=v;continue
            m=re.match(r"^# (\d+)\. (.*)",v)
            if m: h.append('<h2 class="sec"><span>%s</span>%s</h2>'%(m.group(1),inl(m.group(2))));continue
            if v.startswith("## "): h.append('<h3 class="sub">%s</h3>'%inl(v[3:]));continue
            if v.startswith("# "): h.append('<h2 class="sec plain">%s</h2>'%inl(v[2:]));continue
            if v.startswith("GUIDANCE "): h.append('<div class="guide"><b>Guidance</b> %s</div>'%inl(v[9:]));continue
            if re.match(r"^[A-Za-z /]+:\s*_{3,}",v) or v.startswith("Issue /") or v.startswith("Outstanding action"):
                parts=[p for p in re.split(r"_{3,}",v)]
                lab=re.findall(r"([A-Za-z /]+):",v)
                h.append('<div class="fill">'+"".join('<span><b>%s</b><i></i></span>'%e(x.strip()) for x in lab)+'</div>');continue
            if v.startswith("Owner:"):
                lab=re.findall(r"([A-Za-z /]+):",v)
                h.append('<div class="fill">'+"".join('<span><b>%s</b><i></i></span>'%e(x.strip()) for x in lab)+'</div>');continue
            if re.match(r"^(This is a readiness|General information|This checklist provides|Technical basis|The first 48|Sources checked|HMRC guidance —)",v) or v.startswith("*"):
                h.append('<p class="note">%s</p>'%inl(v.lstrip("*").strip()));continue
            h.append('<p>%s</p>'%inl(v));continue
        rows=v
        if not rows: continue
        flat=" ".join(" ".join(r) for r in rows)
        if len(rows[0])==3 and ("CHECKED" in flat and "REVIEW" in flat):
            # legend or what-next
            cs=[]
            for c in rows[0]:
                m=re.match(r"^([✓?!]\s*[A-Z]+)\s*(?:¦\s*)?(.*)$",c,re.S)
                cs.append('<div><b>%s</b><span>%s</span></div>'%(e(m.group(1)),inl(m.group(2))) if m else '<div>%s</div>'%inl(c))
            h.append('<div class="tri legend">%s</div>'%"".join(cs));continue
        if len(rows[0])==3 and len(rows)==1:
            cs=[]
            for c in rows[0]:
                m=re.match(r"^(.*?)\s*¦\s*(.*)$",c,re.S) if "¦" in c else re.match(r"^([A-Z ]{6,})\s+(.*)$",c,re.S)
                cs.append('<div><b>%s</b><span>%s</span></div>'%(e(m.group(1).strip().capitalize()),inl(m.group(2))) if m else '<div>%s</div>'%inl(c))
            h.append('<div class="tri cards">%s</div>'%"".join(cs));continue
        if len(rows)==1 and len(rows[0])==1:
            c=rows[0][0]
            if c.startswith("GUIDANCE"):
                body=c[8:].strip()
                paras=[p for p in re.split(r"\s{2,}",body) if p]
                h.append('<div class="guide"><b>Guidance</b>%s</div>'%"".join("<p>%s</p>"%inl(p) for p in paras));continue
            m=re.match(r"^([A-Z ?]{6,}\?)\s+(.*)$",c,re.S)
            if m: h.append('<div class="cta"><b>%s</b><p>%s</p></div>'%(e(m.group(1).capitalize()),inl(m.group(2))));continue
            h.append('<div class="guide">%s</div>'%inl(c));continue
        if len(rows[0])==2 and re.match(r"^\d+$",rows[0][0]) and len(rows)==1:
            h.append('<h2 class="sec"><span>%s</span>%s</h2>'%(rows[0][0],inl(rows[0][1])));continue
        if all(len(r)==2 and r[1]=="☐" for r in rows):
            h.append('<table class="chk">'+"".join('<tr><td>%s</td><td class="bx"><i></i></td></tr>'%inl(r[0]) for r in rows)+'</table>');continue
        if len(rows)==1 and len(rows[0])==2 and re.match(r"^[?!]\s*[A-Z]+",rows[0][0]):
            lab=rows[0][0]
            h.append('<div class="call"><b>%s</b><span>%s</span></div>'%(e(lab),inl(rows[0][1])));continue
        h.append('<table class="gen">'+"".join("<tr>"+"".join("<td>%s</td>"%inl(c) for c in r)+"</tr>" for r in rows)+"</table>")
    body="\n".join(h)
    parts=re.split(r'(?=<h2 class="sec"><span>|<h3 class="sub">)',body)
    body=parts[0]+"".join('<section class="grp">%s</section>'%p for p in parts[1:])
    return title,tag,body
CSS=open("pdf.css").read()
def build(name,out,short,disclaimer_tag):
    title,tag,body=render(name,short)
    # split: intro paragraphs before first sec stay
    doc=f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>{e(title)}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Raleway:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap"><style>{CSS}</style></head><body>
<header class="top"><img src="data:image/svg+xml;base64,{LOGO}" alt="iTax Advisors" height="30"><span>R&amp;D tax incentive specialists</span></header>
<div class="titleblock"><div class="tag">{e(tag or "")}</div><h1>{e(title)}</h1></div>
{body}
</body></html>'''
    open(out+".html","w",encoding="utf8").write(doc)
if __name__=="__main__":
    for md,out,short in [("checklist-clinical-trials.md","clinical","Clinical Trials & R&D Tax Relief: Pre-Trial Checklist"),("checklist-claim-readiness.md","readiness","15-Point Claim Readiness Checklist"),("checklist-hmrc-enquiry.md","hmrc","HMRC R&D Enquiry Response Checklist")]:
        build(md,out,short,"");print(out)
