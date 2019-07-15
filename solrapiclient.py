import requests
import json


PROVIDER_URL = 'http://dev.bradfordexchange.com/catalog/'


def provide_xml_response(search_word):
    params = {'vid': '20091217001',
                'dataEngineQuery': { 
                'searchKeyword': search_word,
                'interfaceName': "Primary Search",
                'refinements': [],
                'rowsCount': 1000,
                'offset': 0,
                'mobileFlag': False,
                'searchMode': 'MATCH_ALL'
            }
        }
    r = requests.post(PROVIDER_URL, json=params)
    params = json.loads(r.text)['response']
    flat_params = {key: value[0] for (key, value) in params.items()}
    print(flat_params)
    if 'wt' in flat_params:
        del(flat_params['wt'])
    if 'version' in flat_params:
        del(flat_params['version'])
    flat_params['wt'] = 'xml'
    solr_r = requests.get('http://nrhctnsolr05.bgeltd.com:8983/solr/US_items_core/select', params=flat_params)
    return solr_r.text


if __name__ == "__main__":
    provide_xml_response('FAIRIES')
    