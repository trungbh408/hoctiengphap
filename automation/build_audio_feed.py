import json, re, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
URL="https://feed.ausha.co/KX2gVSmZXa67"
req=urllib.request.Request(URL,headers={"User-Agent":"MonProfFrancais/1.0"})
with urllib.request.urlopen(req,timeout=35) as response: data=response.read()
root=ET.fromstring(data)
items=[]
for item in root.findall("./channel/item"):
    title=(item.findtext("title") or "").strip()
    enclosure=item.find("enclosure")
    url=enclosure.get("url","") if enclosure is not None else ""
    desc=" ".join(item.itertext()).lower()
    if not url.startswith("https://"): continue
    # Prefer beginner episodes, exclude longer intermediate material.
    if not re.search(r"\b(a1|a2|d[eé]butant|beginner|niveau facile)\b",title+" "+desc,re.I): continue
    items.append({"title":title,"url":url,"source":"Le français c'est facile avec Adrien","page":item.findtext("link") or "https://francaisfacileadrien.com/","level":"A1–A2"})
Path("audio-a1a2.json").write_text(json.dumps(items[:300],ensure_ascii=False,indent=2),encoding="utf-8")
print("Selected episodes:",len(items[:300]))
