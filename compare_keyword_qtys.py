import solr_endeca_queries as se


CURRENT_KEYWORDS_IDX = 1
CURRENT_RESULT_IDX = 3


def read_keywords(file_idx):
    result = []
    with open ('data/keywords_{}.txt'.format(file_idx), 'r') as f:
        for line in f:
            result.append(line.strip())
    return result


def test_read_keywords():
    keywords = read_keywords(0)
    assert len(keywords) == 100
    assert keywords[0] == 'HARRY POTTER'
    assert keywords[99] == 'ANGEL'


def write_to_file(file_idx, data):
    with open('output/qty_compare_{}.txt'.format(file_idx), 'w') as f:
        f.write('Keyword,Endeca Qty, Solr Qty\n')
        for entry in data:
            f.write("{},{},{}\n".format(entry['keyword'], entry['endeca_qty'], entry['solr_qty']))



def main():
    report_results = []
    for keyword in read_keywords(CURRENT_KEYWORDS_IDX):
        try:
            endeca_props, _ = se.find_endeca_props(keyword)
            solr_props = se.find_solr_props(keyword)
            result_dict = {'keyword': keyword, 'endeca_qty': len(endeca_props), 'solr_qty': len(solr_props)}
            report_results.append(result_dict)
            print("Keyword: {}, Endeca qty: {}, Solr qty: {}".format(result_dict['keyword'], result_dict['endeca_qty'], result_dict['solr_qty']))
        except Exception as e :
            print("Error processing keyword: {}".format(keyword))
            print(e)
    write_to_file(CURRENT_RESULT_IDX, report_results)





if __name__ == "__main__":
    main()