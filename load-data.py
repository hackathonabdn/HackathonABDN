from welly import Well
import matplotlib.pyplot as plt
import geocop_utils

p = Well.from_las('las-files/6307_d.las')

gr = p.data['GR']
