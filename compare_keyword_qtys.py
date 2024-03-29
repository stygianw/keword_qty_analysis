import solr_endeca_queries as se
from file_process import write_to_file, read_keywords
import logging


CURRENT_KEYWORDS_IDX = 2


def main():
    report_results = []
    for keyword in read_keywords(CURRENT_KEYWORDS_IDX):
        try:
            endeca_props, _ = se.find_endeca_props(keyword)
            solr_props = se.find_solr_props(keyword)
            result_tuple = (keyword, len(endeca_props), len(solr_props))
            report_results.append(result_tuple)
            print("Keyword: {}, Endeca qty: {}, Solr qty: {}".format(result_tuple[0], result_tuple[1], result_tuple[2]))
        except Exception as e:
            print("Error processing keyword: {}".format(keyword))
            print(e)
            logging.exception(e)
    write_to_file(CURRENT_KEYWORDS_IDX, report_results, ('Endeca Qty', 'Solr Qty'))


if __name__ == "__main__":
    main()