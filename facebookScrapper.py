#!/usr/bin/env python

# Importamos algunas dependencias de python
import urllib2  # para abrir URLs, EN python 3 se divide en urllib.request y urllib.error
import json  # para usar JSON
import io # para poder dar formato al JSON 
import datetime  # para manejar fechas
import csv # para el archivo excell a la salida
import time


# I generate the access_token by creating an empty Facebook App which gives me
# the app_id and app_secret needed.
app_id = "ENTER YOUR OWN"
app_secret= "ENTER YOUR OWN"
# Concatening them I am sure it won`t expire.
access_token= app_id + "|" + app_secret

# We store the ids we are going to analyse
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
#	- message : texto de la noticia
#	- link : enlace url a la noticia en si
# 	- created_time : fecha de publicacion de la noticia
# 	- type : tipo de contenido (foto, video...)
#	- name : nombre de la publicacion (?)
#	- id : id de la publicacion
#	- reactions.type(LIKE).summary(total_count).limit(0).as(like)) : extrae el numero de likes (total_count) 
#	- comments.limit(1).summary(true) : extrae numero de comentarios y el ultimo (+ usuario + contenido + info)
#	- shares&limit= : extrae el numero de veces que se ha compartido la noticia
def getFBPageFeedData (page_id,access_token,num_status):
	base = "https://graph.facebook.com/v2.9"
	node = "/" + page_id + "/feed"
	parameters = "/?fields=created_time,story,message,name,id,comments.limit(100).summary(true)&limit=%s&access_token=%s&until=2017-06-10&since=2017-06-09" % (num_status, access_token)
	url = base + node + parameters
	data = json.loads(request_until_succeed(url))
	print "Analisis de %s realizado!" %page_id
	return data

#testFBPagesData(ids, access_token)
#testFBPageFeedData(ids,access_token)

test_status_pp = getFBPageFeedData(ids[0], access_token, 10)
#print json.dumps(test_status_pp, indent=4, sort_keys=True)
test_status_psoe = getFBPageFeedData(ids[1], access_token,50) 
#print json.dumps(test_status_psoe, indent=4, sort_keys=True)
test_status_podemos = getFBPageFeedData(ids[2], access_token,50) 
#print json.dumps(test_status_podemos, indent=4, sort_keys=True)
test_status_ciudadanos = getFBPageFeedData(ids[3], access_token,90)
#print json.dumps(test_status_ciudadanos, indent=4, sort_keys=True)


#Obtengo la fecha actual
dateActual = datetime.date.today()#- datetime.timedelta(days=1)
print dateActual 

# Almacena en un json toda la informacion necesaria para sacar los likes de la publicacion
with io.open ('pp.json', 'w', encoding='utf-8') as f:
	for j in range(len(test_status_pp["data"])):
		
		nid = test_status_pp["data"][j]["id"]
		ndate = test_status_pp["data"][j]["created_time"]
		nname = "PP"
		try:
			nmessage = test_status_pp["data"][j]["message"]
		except:
			nmessage = test_status_pp["data"][j]["story"]
		try:
			numcoment = len(test_status_pp["data"][j]["comments"]["data"])
			ncomentarios = test_status_pp["data"][j]["comments"]["summary"]["total_count"]
		except:
			ncomentarios = 0
		try:
			comentar = '['
			for i in range(numcoment):
				ncoments = '  "'+ test_status_pp["data"][j]["comments"]["data"][i]["id"] +'"  , '
				comentar = comentar + ncoments
			comentar = comentar + "]"
		except:
			comentar = "[]"
		try:
			likes = test_status_pp["data"][j]["like"]["summary"]["total_count"]
		except:
			likes = 0
		
		# COMPRUEBO QUE LA PUBLICACION ES DEL DIA ACTUAL Y HAGO EL JSON SI ES ASI 
	
		if ndate.find(dateActual.isoformat()) == 0:
			
			datos = json.dumps({"@timestamp": ndate, "message": nmessage, "text": comentar, "ncomments": ncomentarios, "id": nid, "partido": nname}, sort_keys=True)
			datosx = json.loads(datos)
			#f.write(unicode(json.dumps({"index":{"_id":test_status_pp["data"][j]["id"]}})))
			#f.write(unicode('\n'))
			f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
			f.write(unicode(','))
			f.write(unicode('\n'))

with io.open ('psoe.json', 'w', encoding='utf-8') as f:
	for j in range(len(test_status_psoe["data"])):
		nid = test_status_psoe["data"][j]["id"]
		ndate = test_status_psoe["data"][j]["created_time"]
		nname = "PSOE"
		try:
			nmessage = test_status_psoe["data"][j]["message"]
		except:
			nmessage = test_status_psoe["data"][j]["story"]
		try:
			numcoment = len(test_status_psoe["data"][j]["comments"]["data"])
			ncomentarios = test_status_psoe["data"][j]["comments"]["summary"]["total_count"]
		except:
			ncomentarios = 0
		try:
			comentar = "["
			for i in range(numcoment):
				ncoments =  '  "'+ test_status_psoe["data"][j]["comments"]["data"][i]["id"] +'"  , '
				comentar = comentar + ncoments
			comentar = comentar + "]"
		except:
			comentar = "[]"
		
		# COMPRUEBO QUE LA PUBLICACION ES DEL DIA ACTUAL Y HAGO EL JSON SI ES ASI 
		if ndate.find(dateActual.isoformat()) == 0:
			
			datos = json.dumps({"@timestamp": ndate, "message": nmessage, "text": comentar, "ncomments": ncomentarios, "id": nid, "partido": nname}, sort_keys=True)
			datosx = json.loads(datos)
			#f.write(unicode(json.dumps({"index":{"_id":test_status_pp["data"][j]["id"]}})))
			#f.write(unicode('\n'))
			f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
			f.write(unicode(','))
			f.write(unicode('\n'))

with io.open ('podemos.json', 'w', encoding='utf-8') as f:
	for j in range(len(test_status_podemos["data"])):
		nid = test_status_podemos["data"][j]["id"]
		ndate = test_status_podemos["data"][j]["created_time"]
		nname = "PODEMOS"
		try:
			nmessage = test_status_podemos["data"][j]["message"]
		except:
			nmessage = test_status_podemos["data"][j]["story"]
		try:
			numcoment = len(test_status_podemos["data"][j]["comments"]["data"])
			ncomentarios = test_status_podemos["data"][j]["comments"]["summary"]["total_count"]
		except:
			ncomentarios = 0
		try:
			comentar = "["
			for i in range(numcoment):
				ncoments =  '  "'+ test_status_podemos["data"][j]["comments"]["data"][i]["id"] +'"  , '
				comentar = comentar + ncoments
			comentar = comentar+ "]"
		except:
			comentar = "[]"
		
		# COMPRUEBO QUE LA PUBLICACION ES DEL DIA ACTUAL Y HAGO EL JSON SI ES ASI 
		if ndate.find(dateActual.isoformat()) == 0:
			
			datos = json.dumps({"@timestamp": ndate, "message": nmessage, "text": comentar, "ncomments": ncomentarios, "id": nid, "partido": nname}, sort_keys=True)
			datosx = json.loads(datos)
			#f.write(unicode(json.dumps({"index":{"_id":test_status_pp["data"][j]["id"]}})))
			#f.write(unicode('\n'))
			f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
			f.write(unicode(','))
			f.write(unicode('\n'))

contador = 0
with io.open ('ciudadanos.json', 'w', encoding='utf-8') as f:
	for j in range(len(test_status_ciudadanos["data"])):
		nid = test_status_ciudadanos["data"][j]["id"]
		ndate = test_status_ciudadanos["data"][j]["created_time"]
		nname = "CIUDADANOS"
		try:
			nmessage = test_status_ciudadanos["data"][j]["message"]
		except:
			nmessage = test_status_ciudadanos["data"][j]["story"]
		try:
			numcoment = len(test_status_ciudadanos["data"][j]["comments"]["data"])
			ncomentarios = test_status_ciudadanos["data"][j]["comments"]["summary"]["total_count"]
		except:
			ncomentarios = 0
		try:
			comentar = "["
			for i in range(numcoment):
				ncoments ='  "'+ test_status_ciudadanos["data"][j]["comments"]["data"][i]["id"] +'"  , '
				comentar = comentar + ncoments
			comentar = comentar + "]"
		except:
			comentar = "[]"
		
			
		if ndate.find(dateActual.isoformat()) == 0:	
			contador = contador + 1

		if contador < 1 and ndate.find(dateActual.isoformat()) == 0:
			datos = json.dumps({"@timestamp": ndate, "message": nmessage, "text": comentar, "ncomments": ncomentarios, "id": nid, "partido": nname}, sort_keys=True)
			datosx = json.loads(datos)
			f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
		elif contador >= 1 and ndate.find(dateActual.isoformat()) == 0:
			datos = json.dumps({"@timestamp": ndate, "message": nmessage, "text": comentar, "ncomments": ncomentarios, "id": nid, "partido": nname}, sort_keys=True)
			datosx = json.loads(datos)
			f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
			f.write(unicode(','))
			f.write(unicode('\n'))

		#if ndate.find(dateActual.isoformat()) == 0:	
		#	contador = contador + 1
		#	datos = json.dumps({"date": ndate, "comments": ncomentarios, "id": nid, "likes": nlikes, "message": nmessage, "name": nname, "love": nreacciones}, sort_keys=True)
		#	datosx = json.loads(datos)
		#	f.write(unicode(json.dumps(datosx, ensure_ascii=False)))
		#	f.write(unicode('\n'))
		#	if contador > 1: # si solo hay una publi,no pone la coma.
		#		f.write(unicode(','))
		#		f.write(unicode('\n'))

with io.open('basedatos/facebookSc.json', 'w', encoding='utf-8') as out:
	out.write(unicode('['))
	out.write(unicode('\n'))
	with io.open('pp.json', 'r', encoding='utf-8') as inT:
		for i in inT:
			out.write(i)
			#out.write(unicode(','))
	with io.open('psoe.json', 'r', encoding='utf-8') as inT:
		for i in inT:
			out.write(i)
		#out.write(unicode(','))
	with io.open('podemos.json', 'r', encoding='utf-8') as inT:
		for i in inT:
			out.write(i)
		#out.write(unicode(','))
	with io.open('ciudadanos.json', 'r', encoding='utf-8') as inT:
		for i in inT:
			out.write(i)
	out.write(unicode('\n'))
	out.write(unicode(']'))

		


		

