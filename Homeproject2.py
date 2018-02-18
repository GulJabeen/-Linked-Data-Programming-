#!/usr/bin/python
# -*- coding: utf-8 -*-



import urllib2
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper('https://query.wikidata.org/sparql')
sparql.setQuery("""
PREFIX  dbp:  <http://dbpedia.org/property/>
PREFIX  movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX  owl:  <http://www.w3.org/2002/07/owl#>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  foaf: <http://xmlns.com/foaf/0.1/>
PREFIX  dc:   <http://purl.org/dc/terms/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX  wdt:  <http://www.wikidata.org/prop/direct/>
PREFIX  dbo:  <http://dbpedia.org/ontology/>


SELECT DISTINCT ?Actor ?Death_date ?birth_Place ?birthDate ?Starring ?Cause_Of_Death ?award_received
WHERE {
SERVICE <http://dbpedia.org/sparql> {
?c rdf:type <http://umbel.org/umbel/rc/Actor> . 
?c rdfs:label ?Actor.
FILTER (LANG(?Actor)="en").

FILTER ( xsd:date(?Death_date) >= "1990 - 01 - 01"^^xsd:date )
    ?b  rdfs:label  ?birth_Place
    FILTER ( lang(?birth_Place) = "en" )
    ?Starring  rdf:type       dbo:Film ;
              dbo:starring    ?c .
    ?c        dbo:deathCause  ?d .
    ?d        dbp:name        ?Cause_Of_Death .
    ?c        owl:sameAs      ?wikidata_actor
    FILTER strstarts(str(?wikidata_actor), "http://www.wikidata.org")
    ?wikidata_actor wdt:P166 ?award_received.
 



}

""")

# Create HTML output

print '<html><head><title>Actors who died in 1950</title></head>'

# extract Weekday %A / Month %B / Day of the Month %d by formatting today's date accordingly

datum = datetime.today().strftime('%A  %B %d')
print '<body><h1>Actors Deaths of {}</h1>'.format(datum)

print '<ul>'

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results['results']['bindings']:
    if 'Actor' in result:
        print result['Actor']['value']
    else:
        url = 'NONE'
    if 'Death_date' in result:
        print result['Death_date']['value']
    else:
        name = 'NONE'
    if 'birth_Place' in result:
        print result['birth_Place']['value']
    else:
        name = 'NONE'
    if 'birthDate' in result:
        print result['birthDate']['value']
    else:
        name = 'NONE'
    if 'Starring' in result:
        print result['Starring']['value']
    else:
        name = 'NONE'
    if 'Cause_Of_Death' in result:
        print result['Cause_Of_Death']['value']
    else:
        name = 'NONE'
    if 'award_received' in result:
        print result['award_received']['value']
    else:
        name = 'NONE'

# print '<li><b>{}</b> --  <a href="{}">{}</a>, {} </li>'.format(Actor, url, Death_date, birth_place, birthDate, Starring,Cause_Of_Death, award_received)

        print '<li><b>{}</b> -- <img src="{}" height="60px"> <a href="{}">{}</a>, {} </li>'.format(
            Actor,
            url,
            Death_date,
            birth_place,
            birthDate,
            Starring,
            Cause_Of_Death,
            award_received,
            )

print '</ul>'
print '</body></html>'


			
