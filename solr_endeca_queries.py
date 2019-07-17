from urllib import request, parse
from xml.etree import ElementTree as ET
import re


SOLR_QUERY = "http://nrhctnsolr05.bgeltd.com:8983/solr/US_items_core/select?f.Themes_TREE_2_facet.facet.mincount=1&df=_text_&f.Product_Types_TREE_1_facet.facet.mincount=1&bf=field(popularityBoost)&f.More_Ways_To_Shop_TREE_0_facet.facet.mincount=1&fq=DISPLAY:Y&fq=STORE_AVAILABLE:Y&fq=MARKET_CLASS:P&fq=MARKET_CLASS:P&fq=DISPLAY:Y&fq=STORE_AVAILABLE:Y&autocorrection.spellmode=ALL&bq=(KEYWORDS:train)^100.0&bq=(KEYWORDS:bag)^1000.0&f.Themes_TREE_0_facet.facet.mincount=1&defType=edismax&spellcheck.q=FAIRIES&qf=EXTERNAL_PRODUCT_IDS_search^1.0+title_search^1.0+SHORT_NAME_search^1.0+shortdesc_search^1.0+FEATURE_VALUES_search^1.0+KEYWORDS_search^1.0+MANUFACTURER^1.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^1.0+code_search^1.0+PRODUCT_TYPE^1.0+PRODUCT_TYPE_2^1.0+THEMES^1.0&wt=xml&facet.field=Themes_TREE_0_facet&facet.field=Themes_TREE_1_facet&facet.field=Themes_TREE_2_facet&facet.field=Themes_TREE_3_facet&facet.field=Product_Types_TREE_0_facet&facet.field=Product_Types_TREE_1_facet&facet.field=Product_Types_TREE_2_facet&facet.field=More_Ways_To_Shop_TREE_0_facet&facet.field=More_Ways_To_Shop_TREE_1_facet&facet.field=More_Ways_To_Shop_TREE_2_facet&f.Product_Types_TREE_2_facet.facet.mincount=1&f.More_Ways_To_Shop_TREE_1_facet.facet.mincount=1&start=0&f.Themes_TREE_1_facet.facet.mincount=1&sort=&10006&f.Product_Types_TREE_0_facet.facet.mincount=1&spellcheck=true&pf=EXTERNAL_PRODUCT_IDS_search^1.0+title_search^1.0+SHORT_NAME_search^1.0+shortdesc_search^1.0+FEATURE_VALUES_search^1.0+KEYWORDS_search^1.0+MANUFACTURER^1.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^1.0+code_search^1.0&f.Themes_TREE_3_facet.facet.mincount=1&f.More_Ways_To_Shop_TREE_2_facet.facet.mincount=1&facet=on&rows=1000"


def _create_solr_url(search_word):
    return "{}&{}".format(SOLR_QUERY, _create_solr_q_param(search_word))


def find_endeca_props(search_word):
    r = request.urlopen('http://nrhctnwebit03.bgeltd.com:15005/graph?node=9040+9044+9037&group=0&offset=0&nbins=1000&attrs=primary_search+{}|mode+matchall&irversion=601&format=xml&sort=code'.format(re.sub(r'\s', '+', search_word)))
    doc = r.read()
    root = ET.fromstring(doc)
    erecs = root.findall('.//ERec')
    erec_properties = { x.find('./Property[@Key=\'code\']').text: { y.attrib['Key']: y.text for y in x.findall('./Property') } for x in erecs }
    erec_dimension_matches = {erec.find('./Property[@Key=\'code\']').text:
                            {assocDimLocation.find('./DimVal').attrib['Name']:
                                [dimLocation.find('./DimVal').attrib['Name'] for dimLocation in assocDimLocation.findall('./DimLocationList/DimLocation')] 
                            for assocDimLocation in erec.findall('./AssocDimLocations') } 
                      for erec in erecs}    
    return erec_properties, erec_dimension_matches


def find_solr_props(search_word):
    r = request.urlopen(_create_solr_url(search_word))
    doc = r.read()
    root = ET.fromstring(doc)
    solr_docs = root.findall('.//result/doc')
    solr_properties = {x.find('./str[@name=\'code\']').text: { y.attrib['name']: y.text if y.tag != 'arr' else [z.text for z in y.findall('./str') ] for y in x.findall('./*[@name]') }  for x in solr_docs}
    return solr_properties


def _create_solr_search_string(solr_query):
    if re.match(r'\w+\s+\w+', solr_query):
        return re.sub(r'(\w+)', r'+\1', solr_query) + " \"{}\"".format(solr_query)
    else:
        return solr_query


def test_create_solr_query():
    assert _create_solr_search_string('BEAUTY AND THE BEAST') == '+BEAUTY +AND +THE +BEAST "BEAUTY AND THE BEAST"'
    assert _create_solr_search_string('FAIRIES') == "FAIRIES"


def _create_solr_q_param(search_string):
    return parse.urlencode( {'q': "+({})".format(_create_solr_search_string(search_string))}, safe="()\"")


def test_create_solr_q_param():
    assert _create_solr_q_param("BEAUTY AND THE BEAST") == "q=%2B(%2BBEAUTY+%2BAND+%2BTHE+%2BBEAST+\"BEAUTY+AND+THE+BEAST\")"

