# Keyword quantity comparison script

### Prerequisites

* Python v3

## Installing

Download ZIP file or clone the repository.

## Running

### Qty comparison by keyword list

1. Put the file with keywords list into the /data folder. The file should have name like **'keyword_1.txt'** where 1 is the index of a file.
2. Run the **compare_keyword_qtys.py** script

```
python compare_keyword_qtys.py
```
3. The script will generate an output .csv file into the **/output** folder. For an input file with name **keyword_1.txt**, it will have name like **qty_compare_1_2019-08-08T15:09:18.309247.txt** (i.e. 'qty_compare_${index}_${date}.txt').

### By-word qty differences

1. Set the keyword(s) for comparison on line 5 of **find_differences_by_word.py** script:

```python
SEARCH_WORDS = ['FIGURINES']
```
2. Run **find_differences_by_word.py** script.
3. The script will generate an output file with name **result_FIGURINES_2019-08-12T15:10:06.859998.txt**. The endeca-only items will be listed under ---Endeca only--- header. The same is for solr-only items.

```
KEYWORD: SNOWGLOBES WATER GLOBES
---Endeca Only---
--------- item: 129704001 ------------
129704001: code: 129704001
extprdid not found in props of code 129704001
129704001: title: Illuminated Musical Snowglobe Tabletop Tree
129704001: SHORT_NAME: Thomas Kinkade The Magic Of The Season Tabletop Tree
Product not found in props of code 129704001
129704001: shortdesc: Thomas Kinkade The Magic Of The Season Tabletop Tree
129704001: FEATURE_VALUES: Test
129704001: keywords: Thomas Kinkade
129704001: MANUFACTURER: The Bradford Exchange
artist not found in props of code 129704001
129704001: OTHER_COUNTRY_PROD_ID: None
129704001: EMAIL_SUBJECT_TITLE: Thomas Kinkade Tabletop Tree
Product Types: ['Christmas Trees']
Themes: ['Christmas', 'Snowmen', 'Thomas Kinkade']
--------- item: 909558 ------------
909558: code: 909558
extprdid not found in props of code 909558
909558: title: Kayomi Harai Cats With Glitter Globes Figurine Collection
909558: SHORT_NAME: Kayomi Harai Cat-tivating Purr-sonality Figurine Collection
Product not found in props of code 909558
909558: shortdesc: Kayomi Harai Cat-tivating Purr-sonality Glitter Globe Figurine Collection
909558: FEATURE_VALUES: New Arrivals Hamilton
909558: keywords: Waterglobes
909558: MANUFACTURER: The Hamilton Collection
artist not found in props of code 909558
909558: OTHER_COUNTRY_PROD_ID: None
909558: EMAIL_SUBJECT_TITLE: Kayomi Harai Glitter Globe Cat Figurine Collection
Product Types: ['Figurines']
Themes: ['Cats', 'Cats', 'Cats']
```

# Changing Solr or Endeca queries

**solr_endeca_queries.py** script contains logic which forms Solr and Endeca queries. 
Keywords will be automatically put to Solr and Endeca queries.

####solr
Solr query is static, so just take it from Solr log.
Solr query is formed by _create_solr_url function. It will use the SOLR_QUERY constant and _create_solr_q_param function to form a query.
```python
SOLR_QUERY = "http://dev.bradfordexchange.com:8983/solr/US_items_core/select?f.Themes_TREE_2_facet.facet.mincount=1&df=_text_&f.Product_Types_TREE_1_facet.facet.mincount=1&bf=field(popularityBoost)&f.More_Ways_To_Shop_TREE_0_facet.facet.mincount=1&fq=DISPLAY:Y&fq=STORE_AVAILABLE:Y&fq=MARKET_CLASS:P&autocorrection.spellmode=ALL&f.Themes_TREE_0_facet.facet.mincount=1&defType=edismax&spellcheck.q=disney&qf=EXTERNAL_PRODUCT_IDS_search^200.0+title_search^240.0+SHORT_NAME_search^190.0+shortdesc_search^210.0+FEATURE_VALUES_search^200.0+KEYWORDS_search^190.0+MANUFACTURER^20.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^0.8+code_search^0.7+EMAIL_SUBJECT_TITLE_search+Product_Types_TREE_fsearch^240.0+Themes_TREE_fsearch^160.0&wt=xml&facet.field=Themes_TREE_0_facet&facet.field=Themes_TREE_1_facet&facet.field=Themes_TREE_2_facet&facet.field=Themes_TREE_3_facet&facet.field=Product_Types_TREE_0_facet&facet.field=Product_Types_TREE_1_facet&facet.field=Product_Types_TREE_2_facet&facet.field=More_Ways_To_Shop_TREE_0_facet&facet.field=More_Ways_To_Shop_TREE_1_facet&facet.field=More_Ways_To_Shop_TREE_2_facet&f.Product_Types_TREE_2_facet.facet.mincount=1&f.More_Ways_To_Shop_TREE_1_facet.facet.mincount=1&start=0&f.Themes_TREE_1_facet.facet.mincount=1&rows=10000&f.Product_Types_TREE_0_facet.facet.mincount=1&spellcheck=true&pf=EXTERNAL_PRODUCT_IDS_search^200.0+title_search^240.0+SHORT_NAME_search^190.0+shortdesc_search^210.0+FEATURE_VALUES_search^200.0+KEYWORDS_search^190.0+MANUFACTURER^20.0+ARTIST_search^1.0+OTHER_COUNTRY_PROD_ID^0.8+code_search^0.7+EMAIL_SUBJECT_TITLE_search&f.Themes_TREE_3_facet.facet.mincount=1&f.More_Ways_To_Shop_TREE_2_facet.facet.mincount=1&facet=on"


def _create_solr_url(search_word):
    return "{}&{}".format(SOLR_QUERY, _create_solr_q_param(search_word))
```

####Endeca

Endeca query is set on line 14 of **solr_endeca_queries.py** module:

```python
r = request.urlopen('http://nrhctnwebit03.bgeltd.com:15005/graph?node=9040+9044+9037&group=0&offset=0&nbins=10000&attrs=primary_search+{}|mode+matchall&irversion=601&format=xml&sort=code'.format(re.sub(r'\s', '+', search_word)))
```