import json,urllib.request,urllib.parse,time,sys
p=json.load(open(sys.argv[1]))
out={}
for siren,name,seg in p:
    u="https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/ratios_inpi_bce/records?"+urllib.parse.urlencode({"where":f'siren="{siren}"',"limit":20,"order_by":"date_cloture_exercice desc"})
    r2="https://recherche-entreprises.api.gouv.fr/search?"+urllib.parse.urlencode({"q":siren})
    rec=[];ident={}
    for i in range(3):
        try: rec=json.load(urllib.request.urlopen(u,timeout=30))["results"];break
        except Exception as e: time.sleep(2)
    for i in range(3):
        try:
            rs=json.load(urllib.request.urlopen(r2,timeout=30))["results"]
            ident=rs[0] if rs else {};break
        except Exception: time.sleep(2)
    out[siren]={"name":name,"seg":seg,"ratios":rec,"ident":ident}
    print(siren,name,len(rec),file=sys.stderr)
    time.sleep(0.4)
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False)
