import numpy as np

def log_sum_exp(x, axis=-1):
    a = x.max(axis=axis, keepdims=True)
    out = a + np.log(np.sum(np.exp(x - a), axis=axis, keepdims=True))
    return np.squeeze(out, axis=axis)

def kl_normal(qm, qv, pm, pv):
    return 0.5 * np.sum(np.log(pv) - np.log(qv) + qv/pv +
                        np.square(qm - pm) / pv - 1, axis=-1)

def convert_to_ssl(x, y, n_labels, n_classes, complement=False):
    if y.shape[-1] == n_classes:
        y_sparse = y.argmax(1)
    else:
        y_sparse = y
    x_label, y_label = [], []
    if complement:
        x_comp, y_comp = [], []
    for i in xrange(n_classes):
        idx = y_sparse == i
        x_cand, y_cand = x[idx], y[idx]
        idx = np.random.choice(len(x_cand), n_labels/n_classes, replace=False)
        x_select, y_select = x_cand[idx], y_cand[idx]
        x_label += [x_select]
        y_label += [y_select]
        if complement:
            x_select, y_select = np.delete(x_cand, idx, 0), np.delete(y_cand, idx, 0)
            x_comp += [x_select]
            y_comp += [y_select]
    x_label = np.concatenate(x_label, axis=0)
    y_label = np.concatenate(y_label, axis=0)
    if complement:
        x_comp = np.concatenate(x_comp, axis=0)
        y_comp = np.concatenate(y_comp, axis=0)
        return x_label, y_label, x_comp, y_comp
    else:
        return x_label, y_label, x, y

def conv_shape(x, k, s, p):
    if p == 'SAME':
        return np.ceil(float(x) / float(s))
    elif p == 'VALID':
        return np.ceil(float(x - k + 1) / float(s))
    else:
        raise Exception('Unknown padding type')

def split(arr, size):
    for i in range(0, len(arr), size):
        yield arr[i:i + size]
