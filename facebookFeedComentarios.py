#!/usr/bin/env python

# Importamos algunas dependencias de python
import urllib2  # para abrir URLs, EN python 3 se divide en urllib.request y urllib.error
import json  # para usar json 
import datetime  # para manejar fechas
import csv # para el archivo excell a la salida
import time
import io


# Genero el access_token con el fin de que no caduque en el tiempo. Creo una aplicacion en facebook para generar
# el app_id y su clave secreta.
app_id = "ENTER YOUR OWN"
app_secret= "ENTER YOUR OWN"

access_token= app_id + "|" + app_secret

# Almacenamos los id de las paginas a analizar
ids = ["pp","psoe","ahorapodemos","Cs.Ciudadanos"]


# Funcion utilizada para captar posibles errores y reintentar tras 5 segundos
def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)
            print "Error for URL %s: %s" % (url, datetime.datetime.now())
    return response.read()


def getFBPageFeedData (page_id,access_token,num_status):
    base = "https://graph.facebook.com/v2.9"
    node = "/" + page_id + "/feed"
    parameters = "/?fields=message,created_time,comments&limit=%s&access_token=%s&until=2017-06-10&since=2017-06-09" % (num_status, access_token)
    url = base + node + parameters
    data = json.loads(request_until_succeed(url))
    print "Comentarios de %s extraidos!" %page_id
    return data
	
    
dateActual = datetime.date.today()#- datetime.timedelta(days=1)
print dateActual

test_status_pp = getFBPageFeedData(ids[0],access_token,10)
test_status_psoe = getFBPageFeedData(ids[1],access_token,10)
test_status_podemos = getFBPageFeedData(ids[2],access_token,10)
test_status_ciudadanos = getFBPageFeedData(ids[3],access_token,10)
# Almacena en un json toda la informacion necesaria para sacar los likes de la publicacion

#with io.open('comentariosFeedPP.json', 'w', encoding="utf-8") as f:
#print json.dumps(test_status_psoe, indent=4, sort_keys=True)

with io.open ('basedatos/comentariosPartidos.json', 'w', encoding='utf-8') as f:
    f.write(unicode('['))
    f.write(unicode('\n'))
    for j in range(len(test_status_pp["data"])):
        ndate = test_status_pp["data"][j]["created_time"]
        nname = "PP"
        try:
            nmessage = test_status_pp["data"][j]["message"]
        except:
            nmessage = "Has updated his profile"
        if ndate.find(dateActual.isoformat()) == 0:
            try: lon = len(test_status_pp["data"][j]["comments"]["data"])
            except: lon = 0
            for i in range(lon):
                nid = test_status_pp["data"][j]["comments"]["data"][i]["id"]
                nmes = test_status_pp["data"][j]["comments"]["data"][i]["message"]
                datos = json.dumps({"message": nmessage,"partido": nname,"@timestamp": ndate, "text": nmes, "id": nid}, sort_keys=True)
                datosx = json.loads(datos)
                #f.write(unicode(json.dumps({"index":{"_id":test_status_pp["data"][j]["id"]}})))
                #f.write(unicode('\n'))
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_psoe["data"])):
        ndate = test_status_psoe["data"][j]["created_time"]
        nname = "PSOE"
        try:
            nmessage = test_status_psoe["data"][j]["message"]
        except:
            nmessage = "Has updated his profile"
        if ndate.find(dateActual.isoformat()) == 0:
            try: lon = len(test_status_psoe["data"][j]["comments"]["data"])
            except: lon = 0
            for i in range(lon):
                nid = test_status_psoe["data"][j]["comments"]["data"][i]["id"]
                nmes = test_status_psoe["data"][j]["comments"]["data"][i]["message"]
                datos = json.dumps({"message": nmessage,"partido": nname, "@timestamp": ndate, "text": nmes, "id": nid}, sort_keys=True)
                datosx = json.loads(datos)
                #f.write(unicode(json.dumps({"index":{"_id":test_status_pp["data"][j]["id"]}})))
                #f.write(unicode('\n'))
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_podemos["data"])):
        ndate = test_status_podemos["data"][j]["created_time"]
        nname = "PODEMOS"
        try:
            nmessage = test_status_podemos["data"][j]["message"]
        except:
            nmessage = "Has updated his profile"
        if ndate.find(dateActual.isoformat()) == 0:
            try: lon = len(test_status_podemos["data"][j]["comments"]["data"])
            except: lon = 0
            for i in range(lon):
                nid = test_status_podemos["data"][j]["comments"]["data"][i]["id"]
                nmes = test_status_podemos["data"][j]["comments"]["data"][i]["message"]
                datos = json.dumps({"message": nmessage,"partido": nname, "@timestamp": ndate, "text": nmes, "id": nid}, sort_keys=True)
                datosx = json.loads(datos)
                #f.write(unicode(json.dumps({"index":{"_id":test_status_pp["data"][j]["id"]}})))
                #f.write(unicode('\n'))
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_ciudadanos["data"])):
        ndate = test_status_ciudadanos["data"][j]["created_time"]
        nname = "CIUDADANOS"
        try:
            nmessage = test_status_ciudadanos["data"][j]["message"]
        except:
            nmessage = "Has updated his profile"
        if ndate.find(dateActual.isoformat()) == 0:
            try: lon = len(test_status_ciudadanos["data"][j]["comments"]["data"])
            except: lon = 0
            for i in range(lon):
                nid = test_status_ciudadanos["data"][j]["comments"]["data"][i]["id"]
                nmes = test_status_ciudadanos["data"][j]["comments"]["data"][i]["message"]
                datos = json.dumps({"message": nmessage,"partido": nname, "@timestamp": ndate, "text": nmes, "id": nid}, sort_keys=True)
                datosx = json.loads(datos)
                #f.write(unicode(json.dumps({"index":{"_id":test_status_pp["data"][j]["id"]}})))
                #f.write(unicode('\n'))
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))

    f.write(unicode(']'))
    