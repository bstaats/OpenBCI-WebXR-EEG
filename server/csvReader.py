import csv


freqFile = 'data/fftcenter.csv'
intensityFile = 'data/intensitydata.csv'

def read_playback_files(dataFile):
    data = []
    with open(dataFile) as dataCSV:
        _data = csv.DictReader(dataCSV, delimiter=',')
        for row in _data:
            data.append(row)

    return data



# loop through Ordered Dicts, need to merge the freq data with the intensity data
def merge_fdata_and_idata(fdata, idata):
    '''
    merge the two dicts from these two files...
    '''
    i = 0
    f_len = len(fdata)
    #print(f_len)
    new_list = []
    while i < f_len:
        new_dict = {}
        f_dict = fdata[i]
        i_dict = idata[i]
        for key in f_dict.keys():
            if key is not '':
                new_dict[key] = {'freq': f_dict.get(key), 'int': i_dict.get(key)}
                # in the old dataStreamer.js code, not sure why
                new_dict['field1'] = {'freq': i, 'int': i}
        new_list.append(new_dict)
        i += 1

    return new_list


def run():
     # create two ordered Dicts from CSV data
    fdata = read_playback_files(freqFile)
    idata = read_playback_files(intensityFile)
    merge_data = merge_fdata_and_idata(fdata, idata)
    for row in merge_data:
        yield row

