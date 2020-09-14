import os
import numpy as np
from pyhdx.support import np_from_txt, fmt_export
from pyhdx import PeptideMasterTable, KineticsFitting, read_dynamx
import pickle

directory = os.path.dirname(__file__)
np.random.seed(43)


fpath = os.path.join(directory, 'test_data', 'simulated_data_uptake.csv')
data = read_dynamx(fpath)
sequence = 'XXXXTPPRILALSAPLTTMMFSASALAPKIXXXXLVIPWINGDKG'

timepoints = [0.167, 0.5, 1, 5, 10, 30, 100]
start, end = 5, 45  # total span of protein (inc, inc)
nc_start, nc_end = 31, 34  # span of no coverage area (inc, inc)

pmt = PeptideMasterTable(data, drop_first=1, ignore_prolines=True, remove_nan=False)
pmt.set_backexchange(0.)
states = pmt.groupby_state()
series = states['state1']
series.make_uniform()

temperature, pH = 300, 8
kf = KineticsFitting(series, bounds=(1e-2, 800), temperature=temperature, pH=pH)

fr1 = kf.weighted_avg_fit()
out1 = fr1.output
fmt, hdr = fmt_export(out1)
np.savetxt(os.path.join(directory, 'test_data', 'fit_simulated_wt_avg.txt'), out1, fmt=fmt, header=hdr)
with open(os.path.join(directory, 'test_data', 'fit_simulated_wt_avg.pick'), 'wb') as f:
    pickle.dump(fr1, f)


fr_pfact = kf.global_fit_new(out1, use_kint=True)
out_pfact = fr_pfact.output

fmt, hdr = fmt_export(out_pfact)
np.savetxt(os.path.join(directory, 'test_data', 'fit_simulated_pfact.txt'), out_pfact, fmt=fmt, header=hdr)
with open(os.path.join(directory, 'test_data', 'fit_simulated_pfact.pick'), 'wb') as f:
    pickle.dump(fr_pfact, f)
