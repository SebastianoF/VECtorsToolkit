"""
Module for the computation of 2d SVF generated with matrix of se2_a.
The exponential of the SVFs is then computed and compared with the stationary
displacement field SDISP generated by the closed for of the exponential of the
se2_a matrix in se2_g.
Here for only 1 sfv, step by step.
In main_matrix_generated_multiple the same for an arbitrary number of svf
generated by matrix, with random input parameters.
"""

import matplotlib.pyplot as plt
import numpy as np

from calie.operations import lie_exp
from calie.transformations import se2
from calie.visualisations.fields import fields_comparisons

from calie.fields import generate as gen
from calie.fields import queries as qr

if __name__ == '__main__':

    # -> compute matrix of transformations:

    omega = (14, 14)

    x_c = 7
    y_c = 7
    theta = np.pi/8

    tx   = (1 - np.cos(theta)) * x_c + np.sin(theta) * y_c
    ty   = -np.sin(theta) * x_c + (1 - np.cos(theta)) * y_c

    passepartout = 2

    m_0 = se2.Se2G(theta, tx, ty)
    dm_0 = se2.se2g_log(m_0)

    print(dm_0.get_matrix)
    print(m_0.get_matrix)

    # -> generate subsequent vector fields
    svf_0   = gen.generate_from_matrix(omega, dm_0.get_matrix, structure='algebra')
    sdisp_0 = gen.generate_from_matrix(omega, m_0.get_matrix, structure='group')

    # -> compute exponential with different available methods:

    spline_interpolation_order = 3

    l_exp = lie_exp.LieExp()
    l_exp.s_i_o = spline_interpolation_order

    sdisp_ss      = l_exp.scaling_and_squaring(svf_0)
    sdisp_ss_pa   = l_exp.gss_aei(svf_0)
    sdisp_euler   = l_exp.euler(svf_0)
    sdisp_mid_p   = l_exp.midpoint(svf_0)
    sdisp_euler_m = l_exp.euler_mod(svf_0)
    sdisp_rk4     = l_exp.rk4(svf_0)
    sdisp_vode    = l_exp.scipy_pointwise(svf_0, verbose=True, passepartout=passepartout)

    print(type(sdisp_ss))
    print(type(sdisp_ss_pa))
    print(type(sdisp_euler))
    print(type(sdisp_euler_m))
    print(type(sdisp_rk4))

    print('--------------------')
    print("Norm of the svf:")
    print(qr.norm(svf_0, passe_partout_size=4))

    print('--------------------')
    print("Norm of the displacement field:")
    print(qr.norm(sdisp_0, passe_partout_size=4))

    print('--------------------')
    print("Norm of the errors:")
    print('--------------------')
    print('|ss - disp|        = {} '.format(str(qr.norm(sdisp_ss - sdisp_0, passe_partout_size=passepartout))))
    print('|ss_pa - disp|     = {} '.format(str(qr.norm(sdisp_ss_pa - sdisp_0, passe_partout_size=passepartout))))
    print('|euler - disp|     = {} '.format(str(qr.norm(sdisp_euler - sdisp_0, passe_partout_size=passepartout))))
    print('|midpoint - disp|  = {} '.format(str(qr.norm(sdisp_mid_p - sdisp_0, passe_partout_size=passepartout))))
    print('|euler_mod - disp| = {} '.format(str(qr.norm(sdisp_euler_m - sdisp_0, passe_partout_size=passepartout))))
    print('|rk4 - disp|       = {} '.format(str(qr.norm(sdisp_rk4 - sdisp_0, passe_partout_size=passepartout))))
    print('|vode - disp|      = {} '.format(str(qr.norm(sdisp_vode - sdisp_0, passe_partout_size=passepartout+1))))

    # Plot:

    fields_list = [svf_0, sdisp_0, sdisp_ss,   sdisp_ss_pa,   sdisp_euler,
                   sdisp_mid_p,   sdisp_euler_m,   sdisp_rk4, sdisp_vode]
    title_input = ['svf_0', 'sdisp_0', 'sdisp_ss', 'sdisp_ss_pa', 'sdisp_euler',
                   'disp_mid_p', 'disp_euler_m', 'disp_rk4', 'disp_vode']
    subtract_id = [False, False] + ([False, ] * (len(fields_list) - 2))
    input_color = ['r', 'b', 'g', 'c', 'm', 'k', 'b', 'g', 'c']

    title_input_l = ['Sfv Input',
                     'Ground Output',
                     'Scaling and Squaring',
                     'Polyaffine Scal. and Sq.',
                     'Euler method',
                     'Midpoint Method',
                     'Euler Modif Method',
                     'Runge Kutta 4',
                     'Vode (scipy)']

    list_fields_of_field = [[svf_0], [sdisp_0]]
    list_colors = ['r', 'b']
    for third_field in fields_list[2:]:
        list_fields_of_field += [[svf_0, sdisp_0, third_field]]
        list_colors += ['r', 'b', 'm']

    fields_comparisons.see_n_fields_special(list_fields_of_field, fig_tag=50,
                                            colors_input=list_colors,
                                            titles_input=title_input_l,
                                            sample=(1, 1),
                                            zoom_input=[0, 14, 0, 14],
                                            window_title_input='matrix, random generated',
                                            legend_on=False)

    plt.show()
