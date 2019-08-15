from datetime import datetime


def read_keywords(file_idx):
    result = []
    with open('data/keywords_{}.txt'.format(file_idx), 'r') as f:
        for line in f:
            result.append(line.strip())
    return result


def test_read_keywords():
    keywords = read_keywords(0)
    assert len(keywords) == 100
    assert keywords[0] == 'HARRY POTTER'
    assert keywords[99] == 'ANGEL'


def write_to_file(file_idx, data, headers):
    with open('output/qty_compare_{}_{}.txt'.format(file_idx, datetime.now().isoformat()), 'w') as f:
        f.write('Keyword,{}, {}\n'.format(headers[0], headers[1]))
        for entry in data:
            keyword, first_qty, second_qty = entry
            f.write("{},{},{}\n".format(keyword, first_qty, second_qty))

