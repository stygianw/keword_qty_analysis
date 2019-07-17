import solr_endeca_queries as se


SEARCH_WORD = 'WOMENS JEWELRY'


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
    erec_properties, erec_dimension_matches = se.find_endeca_props(SEARCH_WORD)
    solr_properties = se.find_solr_props(SEARCH_WORD)
    
    endeca_codes = set(erec_properties.keys())
    solr_codes = set(solr_properties.keys())
    
    endeca_only = endeca_codes.difference(solr_codes)
    solr_only = solr_codes.difference(endeca_codes)

    print("Endeca unique codes: {}; qty: {}".format(endeca_only, len(erec_properties)))
    print("Solr unique codes: {}; qty: {}".format(solr_only, len(solr_properties)))

    result = []

    if(endeca_only):
        result.append('---Endeca Only---')
        result.extend(print_endeca_only_props(endeca_only, erec_properties, erec_dimension_matches))
    if solr_only:
        result.append('---Solr Only---')
        result.extend(print_solr_only_props(solr_only, solr_properties))
    
    write_to_file(result)

    print('Done.')


if __name__ == "__main__":
    main()
    