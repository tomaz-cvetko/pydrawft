import numpy as np
import matplotlib.pyplot as plt

FIVE_EIGHTS = 5/8

def interpolate(points, N, f=FIVE_EIGHTS, correct=0):
    print(f"{points.size=}, {N=}")
    directions = points[1:] - points[:-1]
    deltas = np.abs(directions)
    realLength = np.sum(deltas)
    dl = realLength/N

    unitDirections = directions/deltas
    interpolated = np.zeros(N, dtype=np.complex64)

    interpolated[0] = points[0]
    i = 1
    for j in range(0, deltas.size):
        l_j = dl
        while l_j < deltas[j]+f*dl and i < N:
            interpolated[i] = interpolated[i-1] + dl*unitDirections[j]
            l_j += dl
            i += 1
        interpolated[i] = points[j+1]
    print(i)
    
    # manually correct the last few points
    interpolated[-1-correct:] = points[-1]
    
    fig, ax = plt.subplots(1, 2)
    ax[0].plot(points.real, points.imag, 'k.-')
    ax[0].set_title("Input points")
    ax[1].plot(interpolated.real, interpolated.imag, 'r.-')
    ax[1].plot([0, dl], [0, 0], '.-')
    ax[1].set_title("Interpolated points")
    plt.show()

    return interpolated


def fourier(drawing):
    times = np.arange(drawing.size)
    
    # do something so that the points will have length 2^n

    Fdrawing = np.fft.fft(drawing)
    print(f"{drawing.size=}, {Fdrawing.size=}")

    np.savetxt("output.dat", Fdrawing)

    freq = np.fft.fftfreq(times.size, d=1/times.size)

    plt.plot(freq, Fdrawing.real, freq, Fdrawing.imag)
    plt.show()

    # recpoints = np.fft.ifft(Fdrawing)

    # plt.plot(recpoints.real, recpoints.imag, 'k.-')
    # plt.show()


if __name__ == "__main__":
    print("Hello, Fourier")
    N = 1024
    interPoints = interpolate(np.loadtxt("input.dat", dtype=np.complex64), N, f=0.5, correct=5)

    fourier(interPoints)