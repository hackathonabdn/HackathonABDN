from welly import Well
import matplotlib.pyplot as plt
p = Well.from_las('las-files/6307_d.las')

p.plot()
plt.show()