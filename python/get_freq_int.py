import numpy as np

def apply_hanning(x, M):
    return x * np.atleast_2d(np.hanning(M)).T

def trim_fft(x):
    return x[:len(x) / 2] * 2

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
    '''
    Get max fft per band
    :param signal: matrix win x channels; sr: sampling rate
    :return: dictionary: bands -> electrodes -> freq, int
    '''
    x, f = compute_fft(signal, sr)
    return get_max_per_band(x, f)

# signal = np.load('./data/sample.npy')
# output = process_data(signal)
#
