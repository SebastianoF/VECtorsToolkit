import numpy as np
from numpy.testing import assert_array_equal, assert_raises, assert_equal, assert_almost_equal

from VECtorsToolkit.tools.fields.queries import check_omega, check_is_vf, get_omega_from_vf, \
    vf_shape_from_omega_and_timepoints, get_omega_from_vf, vf_norm


''' test check_omega '''


def test_check_omega_type():
    with assert_raises(IOError):
        check_omega((10, 10, 10.2))


def test_check_omega_wrong_dimension4():
    with assert_raises(IOError):
        check_omega((10, 10, 10, 1))


def test_check_omega_wrong_dimension1():
    with assert_raises(IOError):
        check_omega((10, ))


def test_check_omega_ok():
    assert check_omega((10, 11, 12)) == 3
    assert check_omega((10, 11)) == 2


''' test check_is_vf '''


def test_check_is_vf_wrong_input():
    with assert_raises(IOError):
        check_is_vf([1, 2, 3])


def test_check_is_vf_wrong_input_len():
    with assert_raises(IOError):
        check_is_vf(np.array([1, 2, 3]))


def test_check_is_vf_mismatch_omega_last_dimension():
    with assert_raises(IOError):
        check_is_vf(np.zeros([10, 10, 10, 1, 7]))


def test_check_is_vf_ok():
    assert check_is_vf(np.zeros([10, 10, 10, 1, 3])) == 3
    assert check_is_vf(np.zeros([10, 10, 10, 1, 9])) == 3
    assert check_is_vf(np.zeros([10, 10, 1, 1, 2])) == 2
    assert check_is_vf(np.zeros([10, 10, 1, 1, 4])) == 2


''' test get_omega '''


def test_get_omega_from_vf_wrong_input():
    with assert_raises(IOError):
        get_omega_from_vf(np.zeros([10, 10, 10, 1, 2]))


def test_get_omega_from_vf_3d():
    assert_array_equal(get_omega_from_vf(np.zeros([10, 10, 10, 1, 3])), [10, 10, 10])


def test_get_omega_from_vf_2d():
    assert_array_equal(get_omega_from_vf(np.zeros([10, 10, 1, 1, 2])), [10, 10])

''' test vf_shape_from_omega_and_timepoints '''

def test_vf_shape_from_omega_and_timepoints():
    assert_array_equal(vf_shape_from_omega_and_timepoints([10, 10], 3), (10, 10, 1, 3, 2))


''' test vf_norm '''


def test_vf_norm_zeros():
    vf = np.zeros([10, 10, 10, 1, 3])
    assert_equal(vf_norm(vf), 0)


def test_vf_norm_ones():
    vf = np.ones([10, 10, 10, 1, 3])
    assert_almost_equal(vf_norm(vf, passe_partout_size=0, normalized=False), 10**3 * np.sqrt(3))


def test_vf_norm_ones_normalised():
    vf = np.ones([10, 10, 10, 1, 3])
    assert_almost_equal(vf_norm(vf, passe_partout_size=0, normalized=True), np.sqrt(3))


if __name__ == '__main__':
    test_check_omega_type()
    test_check_omega_wrong_dimension4()
    test_check_omega_wrong_dimension1()
    test_check_omega_ok()

    test_check_is_vf_wrong_input()
    test_check_is_vf_wrong_input_len()
    test_check_is_vf_mismatch_omega_last_dimension()
    test_check_is_vf_ok()

    test_get_omega_from_vf_wrong_input()
    test_get_omega_from_vf_3d()
    test_get_omega_from_vf_2d()

    test_get_omega_2d()
    test_get_omega_3d()

    test_vf_shape_from_omega_and_timepoints()

    test_vf_norm_zeros()
    test_vf_norm_ones()
    test_vf_norm_ones_normalised()
