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
ax.set_xlim([0, 1])
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

# do something so that the points will have length 2^n
t = np.linspace(0, 1, points.size)
sp = np.fft.fft(points)

timestep = 1/points.size
freq = np.fft.fftfreq(t.shape[-1], d=timestep)

plt.plot(freq, sp.real, freq, sp.imag)
plt.show()

recpoints = np.fft.ifft(sp)

plt.plot(recpoints.real, recpoints.imag)
plt.show()