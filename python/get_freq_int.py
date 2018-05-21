import numpy as np
import pandas as pd

def apply_hanning(x, M):
    return x * np.atleast_2d(np.hanning(M)).T

def trim_fft(x):
    return x[:int(len(x) / 2)] * 2

def compute_fft(x, sr, axis=0, use_window=False):
    l = x.shape[axis]
    if use_window: x = apply_hanning(x, M=sr)
    x2 = abs(np.fft.fft(x / l, axis=axis))
    x2 = np.apply_along_axis(trim_fft, axis=axis, arr=x2)
    f = float(sr) * np.arange(l / 2.) / l
    return x2, f

def get_max_per_band(s, f):
    n = s.shape[-1]
    bands = {}
    bands['theta'] = [3,8]
    bands['alpha'] = [8,12]
    bands['beta'] = [12,35]
    out = {}

    for b, v in bands.items():
        out[b] = {e: {} for e in range(n)}
        inds = (f>=v[0]) & (f<v[1])
        for e in range(n):
            out[b][e]['int'] = np.max(s[inds,e])
            out[b][e]['freq'] = f[inds][np.argmax(s[inds,e])]
    return out

def process_data(signal, sr=250):
    x, f = compute_fft(signal, sr)
    return get_max_per_band(x, f)

# signal = np.loadtxt('./data/testfile_4.csv', delimiter=',')
# output = process_data(signal)

#
def get_preprocessed_data(filename='./data/testfile_4.csv', wlen=128, overlap=64):
    '''
    Get a list of dictionaries, each holds freq and int per channel and freq band
    Inside get fft per window (wlen) with overlap (overlap)
    :param filename: data filename, assumes space as delimiter
    :return: list of dicts
    '''

    with open(filename) as f:
        data = f.readlines()

    data = [i.split('\t') for i in data]

    for id, d in enumerate(data):
        if len(d) > 1:
            data = data[id:]
            break

    D = pd.DataFrame(data)

    data = np.abs(np.array(D[np.arange(1,9)]).astype(np.float))
    n = data.shape[0]

    dicts = []

    for w in np.arange(0, n, overlap):
        dicts.append(process_data(data[w:w+wlen,:]))

    return dicts[:-3]
