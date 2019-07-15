from urllib import request
from xml.etree import ElementTree as ET

SEARCH_WORD = 'FAIRIES'

SOLR_Q_PARAM = '%2B(FAIRIES)'

SOLR_QUERY = "http://nrhctnsolr05.bgeltd.com:8983/solr/US_items_core/select?f.Themes_TREE_2_facet.facet.mincount=1&df=_text_&f.Product_Types_TREE_1_facet.facet.mincount=1&bf=field(popularityBoost)&f.More_Ways_To_Shop_TREE_0_facet.facet.mincount=1&fq=DISPLAY:Y&fq=STORE_AVAILABLE:Y&fq=MARKET_CLASS:P&fq=MARKET_CLASS:P&fq=DISPLAY:Y&fq=STORE_AVAILABLE:Y&autocorrection.spellmode=ALL&bq=(KEYWORDS:train)^100.0&bq=(KEYWORDS:bag)^1000.0&f.Themes_TREE_0_facet.facet.mincount=1&defType=edismax&spellcheck.q=FAIRIES&qf=EXTERNAL_PRODUCT_IDS_search^1.0+title_search^1.0+SHORT_NAME_search^1.0+shortdesc_search^1.0+FEATURE_VALUES_search^1.0+KEYWORDS_search^1.0+MANUFACTURER^1.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^1.0+code_search^1.0+Product_Types_TREE_fsearch^1.0+Themes_TREE_fsearch^1.0&wt=xml&facet.field=Themes_TREE_0_facet&facet.field=Themes_TREE_1_facet&facet.field=Themes_TREE_2_facet&facet.field=Themes_TREE_3_facet&facet.field=Product_Types_TREE_0_facet&facet.field=Product_Types_TREE_1_facet&facet.field=Product_Types_TREE_2_facet&facet.field=More_Ways_To_Shop_TREE_0_facet&facet.field=More_Ways_To_Shop_TREE_1_facet&facet.field=More_Ways_To_Shop_TREE_2_facet&f.Product_Types_TREE_2_facet.facet.mincount=1&f.More_Ways_To_Shop_TREE_1_facet.facet.mincount=1&start=0&f.Themes_TREE_1_facet.facet.mincount=1&sort=&10006&f.Product_Types_TREE_0_facet.facet.mincount=1&q={}&spellcheck=true&pf=EXTERNAL_PRODUCT_IDS_search^1.0+title_search^1.0+SHORT_NAME_search^1.0+shortdesc_search^1.0+FEATURE_VALUES_search^1.0+KEYWORDS_search^1.0+MANUFACTURER^1.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^1.0+code_search^1.0&f.Themes_TREE_3_facet.facet.mincount=1&f.More_Ways_To_Shop_TREE_2_facet.facet.mincount=1&facet=on&rows=1000".format(SOLR_Q_PARAM)

ENDECA_PRIMARY_SEARCH_FIELDS = [
    'code',
    'extprdid',
    'title',
    'SHORT_NAME',
    'Product',
    'shortdesc',
    'FEATURE_VALUES',
    'keywords',
    'MANUFACTURER',
    'artist',
    'OTHER_COUNTRY_PROD_ID',
    'EMAIL_SUBJECT_TITLE',
]


SOLR_SEARCH_FIELDS = [
    'code',
    'EXTERNAL_PRODUCT_IDS',
    'title',
    'SHORT_NAME',
    'shortdesc',
    'FEATURE_VALUES',
    'KEYWORDS',
    'MANUFACTURER',
    'ARTIST',
    'OTHER_COUNTRY_PROD_ID',
]

ENDECA_SEARCH_DIMENSIONS = [
    'Product Types',
    'Themes'
]


SOLR_SEARCH_FIELDS = [
    'EXTERNAL_PRODUCT_IDS',
    'title',
    'SHORT_NAME',
    'shortdesc',
    'FEATURE_VALUES',
    'KEYWORDS',
    'MANUFACTURER',
    'THEMES',
    'PRODUCT_TYPE',
    'PRODUCT_TYPE_2',
    'ARTIST',
    'OTHER_COUNTRY_PROD_ID',
    'scode',
    'Product_Types_TREE_fsearch',
    'Themes_TREE_fsearch'
]


def find_endeca_props():
    r = request.urlopen('http://nrhctnwebit03.bgeltd.com:15005/graph?node=9040+9044+9037&group=0&offset=0&nbins=1000&attrs=primary_search+{}|mode+matchall&irversion=601&format=xml&sort=code'.format(SEARCH_WORD))
    doc = r.read()
    root = ET.fromstring(doc)
    erecs = root.findall('.//ERec')
    erec_properties = { x.find('./Property[@Key=\'code\']').text: { y.attrib['Key']: y.text for y in x.findall('./Property') } for x in erecs }
    erec_dimension_matches = {erec.find('./Property[@Key=\'code\']').text: 
                            { assocDimLocation.find('./DimVal').attrib['Name']: 
                                [dimLocation.find('./DimVal').attrib['Name'] for dimLocation in assocDimLocation.findall('./DimLocationList/DimLocation')] 
                            for assocDimLocation in erec.findall('./AssocDimLocations') } 
                      for erec in erecs}    
    return erec_properties, erec_dimension_matches


def find_solr_props():
    r = request.urlopen(SOLR_QUERY.format(SEARCH_WORD))
    doc = r.read()
    root = ET.fromstring(doc)
    solr_docs = root.findall('.//result/doc')
    solr_properties = {x.find('./str[@name=\'code\']').text: { y.attrib['name']: y.text if y.tag != 'arr' else [z.text for z in y.findall('./str') ] for y in x.findall('./*[@name]') }  for x in solr_docs}
    return solr_properties


def print_endeca_only_props(codes, erec_properties, erec_dimension_matches) -> list:
    result = []
    for code in codes:
        print("--------- item: {} ------------".format(code))
        result.append("--------- item: {} ------------".format(code))
        props, dim_matches = erec_properties[code], erec_dimension_matches[code]
        for endeca_search_prop in ENDECA_PRIMARY_SEARCH_FIELDS:
            if endeca_search_prop in props:
                result.append("{}: {}: {}".format(code, endeca_search_prop, props[endeca_search_prop]))
            else:
                result.append("{} not found in props of code {}".format(endeca_search_prop, code))
        for endeca_search_dim in ENDECA_SEARCH_DIMENSIONS:
            if endeca_search_dim in dim_matches:
                result.append("{}: {}".format(endeca_search_dim, dim_matches[endeca_search_dim]))
            else:
                result.append("{} not found in dimensions of code {}".format(endeca_search_dim, code))
    return result


def print_solr_only_props(codes, solr_records) -> list:
    result = []
    for code in codes:
        result.append("--------- item: {} ------------".format(code))
        props = solr_records[code]
        for solr_search_field in SOLR_SEARCH_FIELDS:
            if solr_search_field in props:
                result.append("{}: {}: {}".format(code, solr_search_field, props[solr_search_field]))
            else:
                result.append("{} not found in props of code {}".format(solr_search_field, code))
    return result


def write_to_file(results):
    with open('result.txt', 'w') as f:
        for line in results:
            f.write(line + '\n')


def main():
    erec_properties, erec_dimension_matches = find_endeca_props()
    solr_properties = find_solr_props()
    
    endeca_codes = set(erec_properties.keys())
    solr_codes = set(solr_properties.keys())
    
    endeca_only = endeca_codes.difference(solr_codes)
    solr_only = solr_codes.difference(endeca_codes)

    print("Endeca unique codes: {}".format(endeca_only))
    print("Solr unique codes: {}".format(solr_only))

    result = []

    if(endeca_only):
        result.extend(print_endeca_only_props(endeca_only, erec_properties, erec_dimension_matches))
    if solr_only:
        result.extend(print_solr_only_props(solr_only, solr_properties))
    
    write_to_file(result)

    print('Done.')


if __name__ == "__main__":
    main()
    