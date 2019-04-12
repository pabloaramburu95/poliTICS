#!/bin/sh
curl -XPUT 'http://localhost:9200/reacciones/_mapping/angry?update_all_types' -d '
{
  "properties": {
    "partido": { 
      "type":"text",
      "fielddata": true
    }
  }
}'
curl -XPUT 'http://localhost:9200/reacciones/_mapping/loves?update_all_types' -d '
{
  "properties": {
    "partido": { 
      "type":"text",
      "fielddata": true
    }
  }
}'
curl -XPUT 'http://localhost:9200/reacciones/_mapping/likes?update_all_types' -d '
{
  "properties": {
    "partido": { 
      "type":"text",
      "fielddata": true
    }
  }
}'
curl -XPUT 'http://localhost:9200/reacciones/_mapping/hahas?update_all_types' -d '
{
  "properties": {
    "partido": { 
      "type":"text",
      "fielddata": true
    }
  }
}'
curl -XPUT 'http://localhost:9200/politicos/_mapping/facebook?update_all_types' -d '
{
  "properties": {
    "partido": { 
      "type":"text",
      "fielddata": true
    }
  }
}'
curl -XPUT 'http://localhost:9200/comentarios/_mapping/facebook?update_all_types' -d '
{
  "properties": {
    "text": { 
      "type":"text",
      "fielddata": true
    }
  }
}'
curl -XPUT 'http://localhost:9200/comentarios/_mapping/facebook?update_all_types' -d '
{
  "properties": {
    "partido": { 
      "type":"text",
      "fielddata": true
    }
  }
}'

curl -XPUT 'http://localhost:9200/comentarios/_mapping/facebook?update_all_types' -d '
{
  "properties": {
    "sentiment": { 
      "type":"text",
      "fielddata": true
    }
  }
}'