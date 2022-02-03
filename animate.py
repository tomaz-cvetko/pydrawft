import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from visualize import smooth



def circle_draw(Fdrawing):
    M = 100
    timeFactor = 1
    times = np.linspace(0, 1, timeFactor*Fdrawing.size)

    complexCircles = np.zeros((2*M+1, times.size), dtype=np.complex64)
    for nu in range(-M, M+1):
        # value of a single exponent on all time points
        complexCircles[nu, :] = Fdrawing[nu] * np.exp(1j*2*np.pi*nu*times)
    complexCircles /= Fdrawing.size
    # smoothDrawing = np.sum(complexCircles, axis=0)/Fdrawing.size

    # setup the plotting
    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    img = plt.imread("hbd.jpg")
    ax.imshow(img, extent=[-1.5, 1.5, -1, 1])


    scenario = [5, 10, 10]

    m_smoothDrawings = []
    for i in range(len(scenario)):
        m = scenario[i]
        m_smoothDrawings.append((np.sum(complexCircles[-m:, :], axis=0) + np.sum(complexCircles[:m+1, :], axis=0)))
    
    m_partialCircPoss = []
    m_partialCircDirs = []
    for i in range(len(scenario)):
        m = scenario[i]
        m_partialCircTemp = np.zeros((2*m+1, times.size), dtype=np.complex64)
        m_partialCircTemp[0, :] = complexCircles[0, :]
        for j in range(1, m+1):
            m_partialCircTemp[2*(j-1), :] = complexCircles[j, :]
            m_partialCircTemp[2*(j-1)+1, :] = complexCircles[-j, :]
        m_partialCircDirs.append(m_partialCircTemp)

        m_partialCircPositions = np.zeros(m_partialCircTemp.shape, dtype=np.complex64)
        m_partialCircPositions[1:, :] = np.cumsum(m_partialCircTemp, axis=0)[:-1, :] # first position must remain zero
        m_partialCircPoss.append(m_partialCircPositions)

    
    
    drawingLine, = ax.plot(m_smoothDrawings[0][0].real, m_smoothDrawings[0][0].imag, 'r')
    currentPoint, = ax.plot(m_smoothDrawings[0][0].real, m_smoothDrawings[0][0].imag, 'o', color='black')
    # drawingLine, = ax.plot([], [], 'r')
    # currentPoint, = ax.plot([], [], 'o', color='black')
    
    xs = m_partialCircPoss[-1][:, 0].real
    ys = m_partialCircPoss[-1][:, 0].imag
    us = m_partialCircDirs[-1][:, 0].real
    vs = m_partialCircDirs[-1][:, 0].imag

    quiver = ax.quiver([], [])
    fresh = True

    # ax.plot(0, 0, 'rx')
    # 
    def animation_frame(i):
        nonlocal fresh
        nonlocal quiver

        j = timeFactor*i % times.size
        m_idx = (timeFactor*i//times.size) % len(scenario)
        m = scenario[m_idx]
        print(i, j, m)

        m_smoothDrawing = m_smoothDrawings[m_idx]
        # m_smoothDrawing = np.sum(complexCircles, axis=0)
        drawingLine.set_data(m_smoothDrawing[:j].real, m_smoothDrawing[:j].imag)
        currentPoint.set_data(m_smoothDrawing[j].real, m_smoothDrawing[j].imag)

        if m_idx == len(scenario)-1:
            xs = m_partialCircPoss[m_idx][:, j].real
            ys = m_partialCircPoss[m_idx][:, j].imag
            us = m_partialCircDirs[m_idx][:, j].real
            vs = m_partialCircDirs[m_idx][:, j].imag
            
            if fresh:
                quiver = ax.quiver(xs, ys, us, vs, angles='xy', pivot='tail', units='xy', scale=1, scale_units='xy', width=0.01, minlength=0)
                fresh = False
            else:
                quiver.set_UVC(us, vs)

                offsets = np.zeros((xs.size, 2), dtype=np.float64)
                offsets[:, 0] = xs
                offsets[:, 1] = ys
                quiver.set_offsets(offsets)


        return drawingLine, currentPoint, quiver
    
    anim = animation.FuncAnimation(fig, animation_frame, len(scenario)*times.size, interval=20, blit=True)
    plt.show()


if __name__ == "__main__":
    print("Hello, animate.py")
    circle_draw(np.loadtxt("output.dat", dtype=np.complex64))