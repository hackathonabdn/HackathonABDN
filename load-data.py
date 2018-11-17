from welly import Well
import matplotlib.pyplot as plt
import geocomp_utils as gu
from sklearn.neighbors import NearestNeighbors
import numpy as np

p = Well.from_las('las-files/6307_d.las')

gr = p.data['GR']

gr[np.isnan(gr)] = 0

windows = gu.split_windows(gr, 10)

X = gu.extract_time_features(windows, None)
pattern = X[0, :]
pattern = pattern.reshape(-1, 20)
X_train = X[1: , :]

nn = NearestNeighbors(metric='cosine')
nn.fit(X_train)
sims, indices = nn.kneighbors(pattern)

for sim, indx in zip(sims[0], indices[0]):
    print(str(indx)+' : '+str(sim))



