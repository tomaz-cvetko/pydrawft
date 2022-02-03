import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from visualize import smooth



def circle_draw(Fdrawing):
    M = 256
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


    scenario = [8, 16, 32, 64, 128, 256]
    # scenario = [4]

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
        m_tempSum = np.cumsum(m_partialCircTemp, axis=0)
        m_partialCircPositions[1:, :] = m_tempSum[:-1, :] # first position must remain zero
        m_error = m_smoothDrawings[i][0] - m_tempSum[-1, 0]
        # m_partialCircPoss.append(m_error + m_partialCircPositions)
        m_partialCircPoss.append(m_partialCircPositions)
        m_smoothDrawings[i][:] -= m_error

    
    
    drawingLine, = ax.plot(m_smoothDrawings[0][0].real, m_smoothDrawings[0][0].imag, 'r')
    currentPoint, = ax.plot(m_smoothDrawings[0][0].real, m_smoothDrawings[0][0].imag, 'o', color='black')
    
    xs = m_partialCircPoss[-1][:, 0].real
    ys = m_partialCircPoss[-1][:, 0].imag
    us = m_partialCircDirs[-1][:, 0].real
    vs = m_partialCircDirs[-1][:, 0].imag

    quiver = ax.quiver([], [])
    old_m_idx = -1
    draw_quivers = True

    text = ax.text(0.0, 0.0, "")
    
    speedFactor = 3
    def animation_frame(i):
        nonlocal old_m_idx
        nonlocal draw_quivers
        nonlocal quiver

        j = speedFactor*timeFactor*i % times.size
        m_idx = (speedFactor*timeFactor*i//times.size) % len(scenario)
        m = scenario[m_idx]
        text = ax.text(1.0, 0.0, str(m))
        # print(i, j, m)

        if m_idx < old_m_idx:
            quiver = ax.quiver([], [])
            draw_quivers = False

        m_smoothDrawing = m_smoothDrawings[m_idx]
        # m_smoothDrawing = np.sum(complexCircles, axis=0)
        drawingLine.set_data(m_smoothDrawing[:j].real, m_smoothDrawing[:j].imag)
        currentPoint.set_data(m_smoothDrawing[j].real, m_smoothDrawing[j].imag)


        if draw_quivers:
            xs = m_partialCircPoss[m_idx][:, j].real
            ys = m_partialCircPoss[m_idx][:, j].imag
            us = m_partialCircDirs[m_idx][:, j].real
            vs = m_partialCircDirs[m_idx][:, j].imag
            
            quiver = ax.quiver(xs, ys, us, vs, angles='xy', pivot='tail', units='xy', scale=1, scale_units='xy', width=0.01, minlength=0)

        old_m_idx = m_idx
        return drawingLine, currentPoint, quiver, text
    
    anim = animation.FuncAnimation(fig, animation_frame, len(scenario)*times.size, interval=20, blit=True)
    plt.show()


if __name__ == "__main__":
    print("Hello, animate.py")
    circle_draw(np.loadtxt("output3.dat", dtype=np.complex64))