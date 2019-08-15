import re
from urllib import parse

SOLR_QUERY = "http://dev.bradfordexchange.com:8983/solr/US_items_core/select?f.Themes_TREE_2_facet.facet.mincount=1&df=_text_&bf=field(popularityBoost)&fq=DISPLAY:Y&fq=STORE_AVAILABLE:Y&fq=MARKET_CLASS:P&f.Themes_TREE_0_facet.facet.mincount=1&defType=edismax&spellcheck.q=disney&qf=EXTERNAL_PRODUCT_IDS_search^200.0+title_search^240.0+SHORT_NAME_search^190.0+shortdesc_search^210.0+FEATURE_VALUES_search^200.0+KEYWORDS_search^190.0+MANUFACTURER^20.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^0.8+code_search^0.7+EMAIL_SUBJECT_TITLE_search+Product_Types_TREE_fsearch^240.0+Themes_TREE_fsearch^160.0&wt=xml&start=0&rows=10000&spellcheck=true&pf=EXTERNAL_PRODUCT_IDS_search^200.0+title_search^240.0+SHORT_NAME_search^190.0+shortdesc_search^210.0+FEATURE_VALUES_search^200.0+KEYWORDS_search^190.0+MANUFACTURER^20.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^0.8+code_search^0.7+EMAIL_SUBJECT_TITLE_search&ps=1000&qs=1000"


def make_alternate_solr_query(search_word):
    return "{}&{}".format(SOLR_QUERY, _create_solr_q_param(search_word))


def _create_solr_search_string(solr_query):
    if re.match(r'\w+\s+\w+', solr_query):
        return "({}) OR \"{}\"".format(re.sub(r'(\w+)', r'+\1', solr_query.lower()), solr_query.lower())
    else:
        return solr_query.lower()


def _create_solr_q_param(search_string):
    return parse.urlencode( {'q': "+({})".format(_create_solr_search_string(search_string))}, safe="()\"")


def test_create_solr_query():
    assert _create_solr_search_string('BEAUTY AND THE BEAST') == '(+beauty +and +the +beast) OR "beauty and the beast"'
    assert _create_solr_search_string('FAIRIES') == "fairies"


def test_create_solr_q_param():
    assert _create_solr_q_param("BEAUTY AND THE BEAST") == "q=%2B((%2Bbeauty+%2Band+%2Bthe+%2Bbeast)+OR+\"beauty+and+the+beast\")"


def test_make_alternate_solr_query():
    assert make_alternate_solr_query("HARRY POTTER") == 'http://dev.bradfordexchange.com:8983/solr/US_items_core/select?f.Themes_TREE_2_facet.facet.mincount=1&df=_text_&bf=field(popularityBoost)&fq=DISPLAY:Y&fq=STORE_AVAILABLE:Y&fq=MARKET_CLASS:P&f.Themes_TREE_0_facet.facet.mincount=1&defType=edismax&spellcheck.q=disney&qf=EXTERNAL_PRODUCT_IDS_search^200.0+title_search^240.0+SHORT_NAME_search^190.0+shortdesc_search^210.0+FEATURE_VALUES_search^200.0+KEYWORDS_search^190.0+MANUFACTURER^20.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^0.8+code_search^0.7+EMAIL_SUBJECT_TITLE_search+Product_Types_TREE_fsearch^240.0+Themes_TREE_fsearch^160.0&wt=xml&start=0&rows=10000&spellcheck=true&pf=EXTERNAL_PRODUCT_IDS_search^200.0+title_search^240.0+SHORT_NAME_search^190.0+shortdesc_search^210.0+FEATURE_VALUES_search^200.0+KEYWORDS_search^190.0+MANUFACTURER^20.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^0.8+code_search^0.7+EMAIL_SUBJECT_TITLE_search&ps=1000&qs=1000&q=%2B((%2Bharry+%2Bpotter)+OR+\"harry+potter\")'