#!/usr/bin/env python

# Importamos algunas dependencias de python
import urllib2  # para abrir URLs, EN python 3 se divide en urllib.request y urllib.error
import json  # para usar JSON
import io # para poder dar formato al JSON 
import datetime  # para manejar fechas
import csv # para el archivo excell a la salida
import time
import random


# Genero el access_token con el fin de que no caduque en el tiempo. Creo una aplicacion en facebook para generar
# el app_id y su clave secreta.
app_id = "1352103248145811"
app_secret= "ee1c01590f72108218e533f67c955454"

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

# Reducimos a 1 las stories, con el fin de poder procesarla facilmente
# La llamare una vez por pagina que quiera analizar
# FIELDS:
#   - message : texto de la noticia
#   - link : enlace url a la noticia en si
#   - created_time : fecha de publicacion de la noticia
#   - type : tipo de contenido (foto, video...)
#   - name : nombre de la publicacion (?)
#   - id : id de la publicacion
#   - reactions.type(LIKE).summary(total_count).limit(0).as(like)) : extrae el numero de likes (total_count) 
#   - comments.limit(1).summary(true) : extrae numero de comentarios y el ultimo (+ usuario + contenido + info)
#   - shares&limit= : extrae el numero de veces que se ha compartido la noticia

#reactions.limit(200)
def getFBPageFeedData (page_id,access_token,num_status):
    base = "https://graph.facebook.com/v2.9"
    node = "/" + page_id + "/feed"
    parameters = "/?fields=created_time,reactions.type(LIKE).summary(total_count).limit(0).as(like),reactions.type(LOVE).summary(total_count).limit(0).as(love),reactions.type(HAHA).summary(total_count).limit(0).as(haha),reactions.type(ANGRY).summary(total_count).limit(0).as(angry)&access_token=%s&num_status=%s&until=2017-06-10&since=2017-06-09" % (access_token,num_status)
    url = base + node + parameters
    data = json.loads(request_until_succeed(url))
    print "Reacciones de %s extraidas!" %page_id
    return data

#testFBPagesData(ids, access_token)
#testFBPageFeedData(ids,access_token)

test_status_pp = getFBPageFeedData(ids[0], access_token, 10)
#print json.dumps(test_status_pp, indent=4, sort_keys=True)
test_status_psoe = getFBPageFeedData(ids[1], access_token,10) 
#print json.dumps(test_status_psoe, indent=4, sort_keys=True)
test_status_podemos = getFBPageFeedData(ids[2], access_token,10) 
#print json.dumps(test_status_podemos, indent=4, sort_keys=True)
test_status_ciudadanos = getFBPageFeedData(ids[3], access_token,10)
#print json.dumps(test_status_ciudadanos, indent=4, sort_keys=True)

#Obtengo la fecha actual
dateActual = datetime.date.today()#- datetime.timedelta(days=1)
print dateActual


#print test_status_pp["data"][0]["like"]["summary"]["total_count"]


# Almacena en un json toda la informacion necesaria para sacar los likes de la publicacion

with io.open("basedatos/likesPoliticos.json", 'w', encoding='utf-8') as f:
    #f.write(unicode('['))
   # f.write(unicode('\n'))
    for j in range(len(test_status_pp["data"])):
        ndate = test_status_pp["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nlikes = test_status_pp["data"][j]["like"]["summary"]["total_count"]
            except: nlikes = 0
            for i in range(nlikes):
                nidpp = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpp,"partido": "PP"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_psoe["data"])):
        ndate = test_status_psoe["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nlikes = test_status_psoe["data"][j]["like"]["summary"]["total_count"]
            except: nlikes = 0
            for i in range(nlikes):
                nidpsoe = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpsoe,"partido": "PSOE"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_podemos["data"])):
        ndate = test_status_podemos["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nlikes = test_status_podemos["data"][j]["like"]["summary"]["total_count"]
            except: nlikes = 0
            for i in range(nlikes):
                nidpod = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpod,"partido": "PODEMOS"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_ciudadanos["data"])):
        ndate = test_status_ciudadanos["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nlikes = test_status_ciudadanos["data"][j]["like"]["summary"]["total_count"]
            except: nlikes = 0
            for i in range(nlikes):
                nidciu = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidciu,"partido": "CIUDADANOS"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    #f.write(unicode(']'))

with io.open("basedatos/lovesPoliticos.json", 'w', encoding='utf-8') as f:
    #f.write(unicode('['))
    #f.write(unicode('\n'))
    for j in range(len(test_status_pp["data"])):
        ndate = test_status_pp["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nloves = test_status_pp["data"][j]["love"]["summary"]["total_count"]
            except: nloves = 0
            for i in range(nloves):
                nidpp = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpp,"partido": "PP"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_psoe["data"])):
        ndate = test_status_psoe["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nloves = test_status_psoe["data"][j]["love"]["summary"]["total_count"]
            except: nloves = 0
            for i in range(nloves):
                nidpsoe = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpsoe,"partido": "PSOE"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_podemos["data"])):
        ndate = test_status_podemos["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nloves = test_status_podemos["data"][j]["love"]["summary"]["total_count"]
            except: nloves = 0
            for i in range(nloves):
                nidpod = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpod,"partido": "PODEMOS"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_ciudadanos["data"])):
        ndate = test_status_ciudadanos["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nloves = test_status_ciudadanos["data"][j]["love"]["summary"]["total_count"]
            except: nloves = 0
            for i in range(nloves):
                nidciu = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidciu,"partido": "CIUDADANOS"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    #f.write(unicode(']'))

with io.open("basedatos/hahasPoliticos.json", 'w', encoding='utf-8') as f:
    #f.write(unicode('['))
    #f.write(unicode('\n'))
    for j in range(len(test_status_pp["data"])):
        ndate = test_status_pp["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nhahas = test_status_pp["data"][j]["haha"]["summary"]["total_count"]
            except: nhahas = 0
            for i in range(nhahas):
                nidpp = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpp,"partido": "PP"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_psoe["data"])):
        ndate = test_status_psoe["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nhahas = test_status_psoe["data"][j]["haha"]["summary"]["total_count"]
            except: nhahas = 0
            for i in range(nhahas):
                nidpsoe = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpsoe,"partido": "PSOE"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_podemos["data"])):
        ndate = test_status_podemos["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nhahas = test_status_podemos["data"][j]["haha"]["summary"]["total_count"]
            except: nhahas = 0
            for i in range(nhahas):
                nidpod = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidpod,"partido": "PODEMOS"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
    for j in range(len(test_status_ciudadanos["data"])):
        ndate = test_status_ciudadanos["data"][j]["created_time"]
        if ndate.find(dateActual.isoformat()) == 0:
            try: nhahas = test_status_ciudadanos["data"][j]["haha"]["summary"]["total_count"]
            except: nhahas = 0
            for i in range(nhahas):
                nidciu = str(random.randint(1,1000000000000000000000000))
                datos = json.dumps({"id":nidciu,"partido": "CIUDADANOS"}, sort_keys=True)
                datosx = json.loads(datos)
                f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                f.write(unicode(','))
                f.write(unicode('\n'))
   # f.write(unicode(']'))


    with io.open("basedatos/angryPoliticos.json", 'w', encoding='utf-8') as f:
       # f.write(unicode('['))
        #f.write(unicode('\n'))
        for j in range(len(test_status_pp["data"])):
            ndate = test_status_pp["data"][j]["created_time"]
            if ndate.find(dateActual.isoformat()) == 0:
                try: nangrys = test_status_pp["data"][j]["angry"]["summary"]["total_count"]
                except: nangrys = 0
                for i in range(nangrys):
                    nidpp = str(random.randint(1,1000000000000000000000000))
                    datos = json.dumps({"id":nidpp,"partido": "PP"}, sort_keys=True)
                    datosx = json.loads(datos)
                    f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                    f.write(unicode(','))
                    f.write(unicode('\n'))
        for j in range(len(test_status_psoe["data"])):
            ndate = test_status_psoe["data"][j]["created_time"]
            if ndate.find(dateActual.isoformat()) == 0:
                try: nangrys = test_status_psoe["data"][j]["angry"]["summary"]["total_count"]
                except: nangrys = 0
                for i in range(nangrys):
                    nidpsoe = str(random.randint(1,1000000000000000000000000))
                    datos = json.dumps({"id":nidpsoe,"partido": "PSOE"}, sort_keys=True)
                    datosx = json.loads(datos)
                    f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                    f.write(unicode(','))
                    f.write(unicode('\n'))
        for j in range(len(test_status_podemos["data"])):
            ndate = test_status_podemos["data"][j]["created_time"]
            if ndate.find(dateActual.isoformat()) == 0:
                try: nangrys = test_status_podemos["data"][j]["angry"]["summary"]["total_count"]
                except: nangrys = 0
                for i in range(nlikes):
                    nidpod = str(random.randint(1,1000000000000000000000000))
                    datos = json.dumps({"id":nidpod,"partido": "PODEMOS"}, sort_keys=True)
                    datosx = json.loads(datos)
                    f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                    f.write(unicode(','))
                    f.write(unicode('\n'))
        for j in range(len(test_status_ciudadanos["data"])):
            ndate = test_status_ciudadanos["data"][j]["created_time"]
            if ndate.find(dateActual.isoformat()) == 0:
                try: nangrys = test_status_ciudadanos["data"][j]["angry"]["summary"]["total_count"]
                except: nangrys = 0
                for i in range(nangrys):
                    nidciu = str(random.randint(1,1000000000000000000000000))
                    datos = json.dumps({"id":nidciu,"partido": "CIUDADANOS"}, sort_keys=True)
                    datosx = json.loads(datos)
                    f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
                    f.write(unicode(','))
                    f.write(unicode('\n'))
      #  f.write(unicode(']'))




