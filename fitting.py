# general imports
import numpy
from scipy.special import wofz


def gaussian(x, a, b, c):
    result = a*1./(c*numpy.sqrt(2*numpy.pi))*numpy.exp(-0.5/c**2.*(x-b)**2.)
    return result


def lorentzian(x, a, b, c):
    result = a/numpy.pi*c/((x-b)**2.+c**2.)
    return result


def voigt(x, a, b, c, d):
    z = (x-b+1j*d)/c/numpy.sqrt(2)
    result = a*numpy.real(wofz(z))/c/numpy.sqrt(2*numpy.pi)
    return result
