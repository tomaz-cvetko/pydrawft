import numpy as np
import matplotlib.pyplot as plt



def smooth(Fdrawing, M):
    # use M frequencies to reconstruct drawing
    # this means frequencies from -M to +M (=2*M + 1), in fact
    freqs = np.fft.fftfreq(Fdrawing.size, d=1/Fdrawing.size)
    print(freqs[:10])
    
    times = np.linspace(0, 1, 10*Fdrawing.size)

    complexCircles = np.zeros((2*M+1, times.size), dtype=np.complex64)
    for nu in range(-M, M+1):
        # value of a single exponent on all time points
        complexCircles[nu, :] = Fdrawing[nu] * np.exp(1j*2*np.pi*nu*times)
    
    smoothDrawing = np.sum(complexCircles, axis=0)/Fdrawing.size

    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    img = plt.imread("hbd.jpg")
    ax.imshow(img, extent=[-1.5, 1.5, -1, 1])
    ax.plot(smoothDrawing.real, smoothDrawing.imag, 'r')

    plt.show()




if __name__ == "__main__":
    print("Hello visualize.py")
    smooth(np.loadtxt("output.dat", dtype=np.complex64), 100)