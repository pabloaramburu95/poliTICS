#!/usr/bin/env python

import os

os.system("python facebookScrapper.py")
os.system("python facebookFeedComentarios.py")
os.system(" python facebookReacciones.py")

#Despues facebookNumComentarios

# revisar comas finales y comillas simples -> dobles en comentarios

# Subes a elasticsearch:
# reacciones,  y facebookSc
#  			sudo python pipeline-pablo.py Elasticsearch --filename aaa.json --index blabla --doc-type blanla --local-scheduler
# comentarios
#  			python3 -m luigi --module sefarad Elasticsearch --index blabla --doc-type blabla --filename aaa.json --local-scheduler

# hacer ./mapping.sh

