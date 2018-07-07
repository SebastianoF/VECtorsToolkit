"""
Test to perform the composition between vector fields.

Here can be found some hints to compare the error of the composition provided by the resampling.
This is actually very high, as soon as the field gets complicated.
"""
import numpy as np
from numpy.testing import assert_array_almost_equal
import matplotlib.pyplot as plt

from VECtorsToolkit.tools.fields.generate_identities import vf_identity_eulerian
from VECtorsToolkit.tools.fields.composition import eulerian_dot_eulerian
from VECtorsToolkit.tools.visualisations.fields_at_the_window import see_field


def test_2_easy_vector_fields(get_figures=False):

    dec = 15  # decimal for the error
    passe_partout = 0

    omega = (20, 20)

    svf_zeros = vf_identity_eulerian(omega)
    svf_f     = vf_identity_eulerian(omega)
    svf_f_inv = vf_identity_eulerian(omega)

    def function_f(t, x):
        t = float(t); x = [float(y) for y in x]
        return np.array([0, 0.3])

    for x in range(20):
        for y in range(20):
            svf_f[x, y, 0, 0, :] = function_f(1, [x, y])
            svf_f_inv[x, y, 0, 0, :] = -1 * function_f(1, [x, y])

    f_o_f_inv = eulerian_dot_eulerian(svf_f, svf_f_inv)
    f_inv_o_f = eulerian_dot_eulerian(svf_f_inv, svf_f)

    assert_array_almost_equal(f_o_f_inv[10, 10, 0, 0, :], [.0, .0], decimal=dec)
    assert_array_almost_equal(f_inv_o_f[10, 10, 0, 0, :], [.0, .0], decimal=dec)

    # results of a composition of 2
    assert_array_almost_equal(f_o_f_inv[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)
    assert_array_almost_equal(f_inv_o_f[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)

    if get_figures:
        see_field(svf_f)
        see_field(svf_f_inv, input_color='r', title_input='2 vector fields: f blue, g red')

        see_field(svf_f, fig_tag=2)
        see_field(svf_f_inv, fig_tag=2, input_color='r')
        see_field(f_o_f_inv, fig_tag=2, input_color='g', title_input='composition (f o f^(-1)) in green')

        see_field(svf_f, fig_tag=3)
        see_field(svf_f_inv, fig_tag=3, input_color='r')
        see_field(f_inv_o_f, fig_tag=3, input_color='g', title_input='composition (f^(-1) o f) in green')

    plt.show()

# test_2_easy_vector_fields(True)


def test_2_less_easy_vector_fields(get_figures=False):

    dec = 1  # decimal for the error
    passe_partout = 3

    omega = (20, 20)

    svf_zeros = vf_identity_eulerian(omega)
    svf_f     = vf_identity_eulerian(omega)
    svf_f_inv = vf_identity_eulerian(omega)

    def function_f(t, x):
        t = float(t); x = [float(y) for y in x]
        return np.array([np.sin(0.01*x[1]), (3*np.cos(x[0]) )/ (x[0] + 2)])

    for x in range(20):
        for y in range(20):
            svf_f[x, y, 0, 0, :] = function_f(1, [x, y])
            svf_f_inv[x, y, 0, 0, :] = -1 * function_f(1, [x, y])

    f_o_f_inv = eulerian_dot_eulerian(svf_f, svf_f_inv)
    f_inv_o_f = eulerian_dot_eulerian(svf_f_inv, svf_f)

    assert_array_almost_equal(f_o_f_inv[10, 10, 0, 0, :], [.0, .0], decimal=dec)
    assert_array_almost_equal(f_inv_o_f[10, 10, 0, 0, :], [.0, .0], decimal=dec)

    # results of a composition
    assert_array_almost_equal(f_o_f_inv[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)
    assert_array_almost_equal(f_inv_o_f[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)

    if get_figures:
        see_field(svf_f)
        see_field(svf_f_inv, input_color='r', title_input='2 vector fields: f blue, g red')

        see_field(svf_f, fig_tag=2)
        see_field(svf_f_inv, fig_tag=2)
        see_field(f_o_f_inv, fig_tag=2, input_color='g', title_input='composition (f o f^(-1)) in green')

        see_field(svf_f, fig_tag=3)
        see_field(svf_f_inv, fig_tag=3, input_color='r')
        see_field(f_inv_o_f, fig_tag=3, input_color='g', title_input='composition (f^(-1) o f) in green')

    plt.show()


def test_easy_composition_with_identity(get_figures=False):

    dec = 6
    passe_partout = 0

    omega = (10, 10)

    svf_zeros = vf_identity_eulerian(omega)
    svf_f     = vf_identity_eulerian(omega)
    svf_id    = vf_identity_eulerian(omega)  # id in lagrangian coordinates is the zero field

    def function_f(t, x):
        t = float(t); x = [float(y) for y in x]
        return np.array([0, 0.3])

    for x in range(10):
        for y in range(10):
            svf_f[x, y, 0, 0, :] = function_f(1, [x, y])

    f_o_id = eulerian_dot_eulerian(svf_f, svf_id)
    id_o_f = eulerian_dot_eulerian(svf_id, svf_f)

    # sfv_0 is provided in Lagrangian coordinates!
    if get_figures:
        see_field(svf_f, fig_tag=21)
        see_field(svf_id, fig_tag=21, input_color='r', title_input='2 vector fields: f blue, g red')

        see_field(svf_f, fig_tag=22)
        see_field(svf_id, fig_tag=22, input_color='r')
        see_field(f_o_id, fig_tag=22, input_color='g', title_input='composition (f o id) in green')

        see_field(svf_f, fig_tag=23)
        see_field(svf_id, fig_tag=23, input_color='r')
        see_field(id_o_f, fig_tag=23, input_color='g', title_input='composition (id o f) in green')

    plt.show()

    # test if the compositions are still in lagrangian coordinates, as attributes and as shape
    assert_array_almost_equal(f_o_id[5, 5, 0, 0, :], function_f(1, [5, 5]), decimal=dec)
    assert_array_almost_equal(id_o_f[5, 5, 0, 0, :], function_f(1, [5, 5]), decimal=dec)

    # results of a composition of 2 lagrangian must be a lagrangian zero field
    assert_array_almost_equal(f_o_id[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)
    assert_array_almost_equal(id_o_f[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)


# test_easy_composition_with_identity(get_figures=True)


def test_less_easy_composition_with_identity(get_figures=False):

    dec = 0  # decimal for the error
    passe_partout = 4

    omega = (20, 25)

    svf_zeros = vf_identity_eulerian(omega=omega)
    svf_f     = vf_identity_eulerian(omega=omega)
    svf_id    = vf_identity_eulerian(omega=omega)

    def function_f(t, x):
        t = float(t); x = [float(y) for y in x]
        return np.array([np.sin(0.01*x[1]), (3*np.cos(x[0]) )/ (x[0] + 2)])

    for x in range(20):
        for y in range(20):
            svf_f[x, y, 0, 0, :] = function_f(1, [x, y])

    f_o_id = eulerian_dot_eulerian(svf_f, svf_id)
    id_o_f = eulerian_dot_eulerian(svf_id, svf_f)

    # test if the compositions are still in lagrangian coordinates, as attributes and as shape
    assert_array_almost_equal(f_o_id[5, 5, 0, 0, :], function_f(1, [5, 5]), decimal=dec)
    assert_array_almost_equal(id_o_f[5, 5, 0, 0, :], function_f(1, [5, 5]), decimal=dec)

    # results of a composition of 2 lagrangian must be a lagrangian zero field

    assert_array_almost_equal(f_o_id[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)
    assert_array_almost_equal(id_o_f[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)

    # sfv_0 is provided in Lagrangian coordinates!
    if get_figures:
        see_field(svf_f, fig_tag=41)
        see_field(svf_id, fig_tag=41, input_color='r', title_input='2 vector fields: f blue, g red')

        see_field(svf_f, fig_tag=42)
        see_field(svf_id, fig_tag=42, input_color='r')
        see_field(f_o_id, fig_tag=42, input_color='g', title_input='composition (f o id) in green')

        see_field(svf_f, fig_tag=43)
        see_field(svf_id, fig_tag=43, input_color='r')
        see_field(id_o_f, fig_tag=43, input_color='g', title_input='composition (id o f) in green')

    plt.show()


test_less_easy_composition_with_identity(get_figures=True)

'''
def test_2_random_vector_fields_svf(get_figures=False):
    """
    Of course the composition is not the identity since we are working in the tangent space.
    """
    dec = 3
    passe_partout = 5

    shape = (10, 10, 1, 1, 2)

    svf_f     = SVF.generate_random_smooth(shape=shape)
    svf_f_inv = SVF.from_array(-1 * svf_f.field)  # this does not provides the inverse!

    f_o_f_inv = SVF.composition(svf_f, svf_f_inv)
    f_inv_o_f = SVF.composition(svf_f_inv, svf_f)

    # # results of a composition of 2 lagrangian must be a lagrangian zero field
    # assert_array_almost_equal(f_o_f_inv.field[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
    #                           svf_zeros.field[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
    #                           decimal=dec)
    # assert_array_almost_equal(f_inv_o_f.field[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
    #                           svf_zeros.field[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
    #                           decimal=dec)

    assert True
    # sfv_0 is provided in Lagrangian coordinates!
    if get_figures:
        see_field(svf_f, fig_tag=51, input_color='b')
        see_field(svf_f_inv, fig_tag=51, input_color='r', title_input='2 vector fields: f blue, g red')

        see_field(svf_f, fig_tag=52, input_color='b')
        see_field(svf_f_inv, fig_tag=52, input_color='r')
        see_field(f_o_f_inv, fig_tag=52, input_color='g', title_input='composition (f o f^(-1)) in green')

        see_field(svf_f, fig_tag=53, input_color='b')
        see_field(svf_f_inv, fig_tag=53, input_color='r')
        see_field(f_inv_o_f, fig_tag=53, input_color='g', title_input='composition (f^(-1) o f) in green')

    plt.show()


def visual_assessment_comparison_old_with_new_code_for_svf(get_figures=False):
    """
    Of course the composition is not the identity since we are working in the tangent space.
    """

    # generate two vector fields
    shape = (10, 10, 1, 1, 2)

    svf_f     = SVF.generate_random_smooth(shape=shape)
    svf_f_inv = SVF.from_array(-1 * svf_f.field)

    dfc = DisplacementFieldComposer()

    f_o_f_inv_dfc = dfc.compose(svf_f, svf_f_inv)
    f_inv_o_f_dfc = dfc.compose(svf_f_inv, svf_f)

    f_o_f_inv = SVF.composition(svf_f, svf_f_inv)
    f_inv_o_f = SVF.composition(svf_f_inv, svf_f)
    if get_figures:
        # see svf map the svfs
        see_field(svf_f, fig_tag=77, input_color='b')
        see_field(svf_f_inv, fig_tag=77, input_color='r', title_input='2 vector fields: f blue, g red P-code')

        see_2_fields(svf_f, svf_f, fig_tag=78, input_color='b')
        see_2_fields(svf_f_inv, svf_f_inv, fig_tag=78, input_color='r')
        see_2_fields(f_o_f_inv, f_o_f_inv_dfc, fig_tag=78, input_color='g',
                     title_input_0='(f o f^(-1)) new code', title_input_1='(f o f^(-1)) old code')

        see_2_fields(svf_f, svf_f, fig_tag=79, input_color='b')
        see_2_fields(svf_f_inv, svf_f_inv, fig_tag=79, input_color='r')
        see_2_fields(f_inv_o_f, f_inv_o_f_dfc, fig_tag=79, input_color='g',
                     title_input_0='(f^(-1) o f) new code', title_input_1='(f^(-1) o f) old code')

        plt.show()


def test_2_random_vector_fields_as_deformations(get_figures=False):

    dec = 1
    passe_partout = 3

    shape = (15, 15, 1, 1, 2)

    sigma_init = 4
    sigma_gaussian_filter = 2
    svf_zeros = SVF.generate_zero(shape=shape)
    svf_0     = SVF.generate_random_smooth(shape=shape,
                                             sigma=sigma_init,
                                             sigma_gaussian_filter=sigma_gaussian_filter)

    sdisp_0 = svf_0.exponential(algorithm='ss')
    sdisp_0_inv = (-1 * svf_0).exponential(algorithm='ss')

    f_o_f_inv = SVF.composition(sdisp_0, sdisp_0_inv)
    f_inv_o_f = SVF.composition(sdisp_0_inv, sdisp_0)

    # results of a composition of 2 lagrangian must be a lagrangian zero field
    assert_array_almost_equal(f_o_f_inv.field[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros.field[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)
    assert_array_almost_equal(f_inv_o_f.field[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              svf_zeros.field[passe_partout:-passe_partout, passe_partout:-passe_partout, 0, 0, :],
                              decimal=dec)

    # sfv_0 is provided in Lagrangian coordinates!
    if get_figures:
        see_field(sdisp_0, fig_tag=61, input_color='b')
        see_field(sdisp_0_inv, fig_tag=61, input_color='r', title_input='2 displacement fields: f blue, g red')

        see_field(sdisp_0, fig_tag=62, input_color='b')
        see_field(sdisp_0_inv, fig_tag=62, input_color='r')
        see_field(f_o_f_inv, fig_tag=62, input_color='g', title_input='composition (f o f^(-1)) in green')

        see_field(sdisp_0, fig_tag=63, input_color='b')
        see_field(sdisp_0_inv, fig_tag=63, input_color='r')
        see_field(f_inv_o_f, fig_tag=63, input_color='g', title_input='composition (f^(-1) o f) in green')

    plt.show()

'''
'''
test_2_easy_vector_fields(get_figures=True)
test_2_less_easy_vector_fields(get_figures=True)
test_easy_composition_with_identity(get_figures=True)
test_less_easy_composition_with_identity(get_figures=True)
test_2_random_vector_fields_svf(get_figures=True)
visual_assessment_comparison_old_with_new_code_for_svf(get_figures=True)

test_2_random_vector_fields_as_deformations(get_figures=True)
'''
