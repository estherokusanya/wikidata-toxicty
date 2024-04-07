import requests
import json

def get_wikidata_triples(entity_id):
    endpoint_url = "https://query.wikidata.org/sparql"
    query = f"""SELECT ?subjectLabel ?predicate ?object
        WHERE {{
        VALUES (?s) {{(wd:{entity_id})}}
        ?s ?wdt ?o .
        ?wd wikibase:directClaim ?wdt .
        ?wd rdfs:label ?predicate .
        OPTIONAL {{
            ?o rdfs:label ?object .
        }}
        FILTER (lang(?object) = "en")
        FILTER (lang(?predicate) = "en")
        wd:{entity_id} rdfs:label ?subjectLabel.
        FILTER(LANG(?subjectLabel) = "en")
        FILTER(CONTAINS(STR(?predicate), "ID") = false)
        FILTER(STRSTARTS(STR(?object), "http") =false)
        FILTER(CONTAINS(STR(?object), "/") = false)
        FILTER(CONTAINS(STR(?predicate), "ISNI") = false)
        BIND (COALESCE(?object, ?o) AS ?object)
        }} ORDER BY xsd:integer(STRAFTER(STR(?wd), "http://www.wikidata.org/entity/P"))
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Accept": "application/json"
    }
    params = {
        "query": query,
        "format": "json"
    }
    response = requests.get(endpoint_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        triples = [
            {
                "subject": result['subjectLabel']['value'],
                "predicate": result['predicate']['value'] ,
                "object": result['object']['value'],
            }
            for result in data['results']['bindings']
        ]
        return triples
    else:
        print(f"Error: {response.status_code}")
        return None

def process_entity_ids(entity_ids, output_file):
    all_results = []

    for entity_id in entity_ids:
        triples = get_wikidata_triples(entity_id)
        if triples:
            all_results.extend(triples)

    if all_results:
        with open(output_file, 'a', encoding='utf-8') as json_file:
            json.dump(all_results, json_file, ensure_ascii=False, indent=2)
        print(f"Results stored in {output_file}")
    else:
        print("No results to store.")


def get_items(p_value, wd_value, limit):
    endpoint_url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Accept": "application/json"
    }
    query = f"""
        SELECT DISTINCT (replace(str(?item), "http://www.wikidata.org/entity/", "") as ?itemID) 
        WHERE {{
        ?item p:{p_value} ?statement0.
        ?statement0 (ps:{p_value}) wd:{wd_value}.
        FILTER(EXISTS {{ ?statement0 prov:wasDerivedFrom ?reference. }})
        }}
        LIMIT {limit}
        """
    params = {
        "query": query,
        "format": "json"
    }
    try:
        response = requests.get(endpoint_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        results= data["results"]["bindings"]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        results= None

    if results:
        items_list = [result['itemID']['value'] for result in results]
        return items_list
    else:
        return None


low_income_countries = [
    'Q889','Q967','Q965','Q929','Q974','Q683',
    'Q986','Q115','Q1005','Q1007','Q1014','Q1019',
    'Q912','Q1029','Q1020','Q1032','Q423','Q1037',
    'Q1049','Q1044','Q1045','Q958','Q858','Q657',
    'Q945','Q1036','Q805','Q916','Q962','Q902',
    'Q750','Q917','Q1008','Q1009','Q971','Q970',
    'Q1011','Q977','Q262','Q79','Q702','Q117',
    'Q1006','Q783','Q790','Q668','Q794','Q810',
    'Q114','Q813','Q424','Q710','Q819','Q822',
    'Q854','Q1013','Q1028','Q836','Q711','Q1025',
    'Q1033','Q811','Q837','Q843','Q928','Q691',
    'Q1041','Q685','Q1039','Q1050','Q863','Q574',
    'Q948','Q924','Q212','Q265','Q881','Q686',
    'Q953','Q954']

high_income_countries = [
    'Q21203','Q228','Q878','Q16641','Q781','Q408',
    'Q40','Q31','Q398','Q778','Q23635','Q244',
    'Q921','Q16','Q39','Q42314','Q298','Q25279',
    'Q5785','Q229','Q213','Q183','Q35','Q29',
    'Q191','Q33','Q142','Q4628','Q145','Q1410',
    'Q41','Q223','Q16635','Q734','Q8646','Q224',
    'Q28','Q9676','Q27','Q189','Q801','Q38',
    'Q17','Q763','Q884','Q817','Q347','Q37',
    'Q32','Q211','Q14773','Q126125','Q235','Q233',
    'Q16644','Q33788','Q55','Q20','Q697','Q664',
    'Q842','Q804','Q36','Q1183','Q45','Q30971',
    'Q846','Q218','Q851','Q334','Q238','Q214',
    'Q215','Q34','Q26273','Q1042','Q18221','Q754',
    'Q865','Q77',
]

high_income_countries2 = [
    'Q30','Q25305','Q11703','Q222',
    'Q414','Q399','Q227','Q219','Q225','Q184',
    'Q242','Q155','Q963','Q148','Q739','Q800',
    'Q241','Q784','Q786','Q736','Q712','Q1000',
    'Q230','Q983','Q769','Q774','Q252','Q796',
    'Q766','Q232','Q1016','Q760','Q217','Q826',
    'Q96','Q709','Q221','Q236','Q1027','Q833',
    'Q1030','Q419','Q695','Q733','Q39760','Q159',
    'Q792','Q403','Q730','Q869','Q874','Q678',
    'Q43','Q672','Q757','Q1246','Q258'
]

process_entity_ids(low_income_countries, 'low_income_wiki_results.json')
print("low income complete")

process_entity_ids(high_income_countries, 'high_income_wiki_results.json')
print("high income complete")

process_entity_ids(get_items("P21", "Q6581097",500), 'male_wiki_results.json')
print("male results complete")

process_entity_ids(get_items("P21", "Q6581072",500), 'female_wiki_results.json')
print("female results complete")

process_entity_ids(get_items("P21", "Q189125",150), 'trans_wiki_results.json')#trans
process_entity_ids(get_items("P21", "Q1052281",150), 'trans_wiki_results.json')#trans_women
process_entity_ids(get_items("P21", "Q2449503",150), 'trans_wiki_results.json')#trans_man
process_entity_ids(get_items("P21", "Q48270",150), 'trans_wiki_results.json')#non-binary
print("trans results complete")