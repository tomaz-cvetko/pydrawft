from time import time
import numpy as np
from matplotlib import pyplot as plt

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        # print('click', event)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Input a curve')
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1, 1])
line, = ax.plot([], [], marker="o", color="r")
linebuilder = LineBuilder(line)

plt.show()

points = np.zeros(len(linebuilder.xs)+1, np.complex64)
points[:-1] = np.array(linebuilder.xs) + 1j*np.array(linebuilder.ys)
points[-1] = points[0]

points -= np.average(points)

plt.plot(points.real, points.imag)
plt.show()

np.savetxt("input.dat", points)