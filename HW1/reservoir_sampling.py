import random
from urllib2 import Request, urlopen, URLError, HTTPError


def read_data(url):
    req = Request(url=url)
    try:
        response = urlopen(req)
    except HTTPError as e:
        print 'HTTPError code: ', e.code
    except URLError as e:
        print 'URLError: ', e.reason
    else:
        return response.read()


def reservoir_sampling(stream, reservoir_size):
    reservoir = [None for _ in range(reservoir_size)]
    i = 0
    for data_line in stream.splitlines():
        if len(data_line) > 0:
            comment = data_line.startswith('%')
            if not comment:
                sample = tuple(data_line.rstrip().split(' '))
                if i < reservoir_size:
                    reservoir[i] = sample
                else:
                    j = random.randint(0, i)
                    if j < reservoir_size:
                        reservoir[j] = sample
                i += 1
    return reservoir


def store_sample(sample_data, filename):
    with open(filename, 'a') as out_file:
        header = ' '.join(['MagX', 'MagY'])
        out_file.write(header + '\n')
        for sample_line in sample_data:
            mag_x_mag_y = ' '.join(sample_line[1:3])
            out_file.write(mag_x_mag_y+'\n')


if __name__ == '__main__':
    nudge = read_data('http://www.nxp.com/files-static/global_support_files/Nudge.txt')
    sample = reservoir_sampling(nudge, 20)
    store_sample(sample, 'output.txt')