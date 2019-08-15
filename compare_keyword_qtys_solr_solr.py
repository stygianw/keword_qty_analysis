import solr_endeca_queries as se
from file_process import write_to_file, read_keywords
import logging


CURRENT_KEYWORDS_IDX = 2


def main():
    report_results = []
    for keyword in read_keywords(CURRENT_KEYWORDS_IDX):
        try:
            solr_props = se.find_solr_props(keyword)
            solr_props_second = se.find_alternate_solr_props(keyword)
            result_tuple = (keyword, len(solr_props), len(solr_props_second))
            report_results.append(result_tuple)
            print("Keyword: {}, Solr 1 qty: {}, Solr 2 qty: {}".format(result_tuple[0], result_tuple[1], result_tuple[2]))
        except Exception as e:
            print("Error processing keyword: {}".format(keyword))
            print(e)
            logging.exception(e)
    write_to_file(CURRENT_KEYWORDS_IDX, report_results, ('Solr 1 Qty', 'Solr 2 Qty'))


if __name__ == "__main__":
    main()