import numpy as np
import matplotlib.pyplot as plt
import time

from transformations.s_vf import SVF
from visualizer.fields_at_the_window import see_field
from visualizer.fields_comparisons import see_2_fields_separate_and_overlay, \
    see_overlay_of_n_fields, see_n_fields_special

"""
Module for the computation of 2d SVF generated with matrix of se2_a.
The exponential of the SVFs is then computed and compared with the stationary
displacement field SDISP generated by the closed for of the exponential of the
se2_a matrix in se2_g.
Here for only 1 sfv, step by step.
In main_matrix_generated_multiple the same for an arbitrary number of svf
generated by matrix, with random input parameters.
"""

### parameters
spline_interpolation_order = 3
passepartout = 2

random_seed = 42

if random_seed > 0:
    np.random.seed(random_seed)

### elaborate transformations:

shape = (14, 14, 1, 1, 2)
svf_0   = SVF.generate_random_smooth(shape=shape, sigma=2, sigma_gaussian_filter=2)

### compute exponential with different available methods:

sdisp_ss      = svf_0.exponential(algorithm='ss',        s_i_o=spline_interpolation_order)
sdisp_ss_pa   = svf_0.exponential(algorithm='gss_rk4',   s_i_o=spline_interpolation_order)
sdisp_euler   = svf_0.exponential(algorithm='euler',     s_i_o=spline_interpolation_order)
sdisp_mid_p   = svf_0.exponential(algorithm='midpoint',  s_i_o=spline_interpolation_order)
#sdisp_series  = svf_0.exponential(algorithm='series',    s_i_o=spline_interpolation_order)
sdisp_heun    = svf_0.exponential(algorithm='heun',      s_i_o=spline_interpolation_order)
sdisp_heun_m  = svf_0.exponential(algorithm='heun_mod',  s_i_o=spline_interpolation_order)
sdisp_rk4     = svf_0.exponential(algorithm='rk4',       s_i_o=spline_interpolation_order)

# Dummy ground truth
sdisp_0  = svf_0.exponential(algorithm='ss',       s_i_o=spline_interpolation_order)

print '--------------------'
print "Norm of the svf:"
print svf_0.norm(passe_partout_size=4)

print '--------------------'
print "Norm of the displacement field:"
print sdisp_0.norm(passe_partout_size=4)


print '--------------------'
print "Norm of the errors:"
print '--------------------'

print '|ss - disp|           = ' + str((sdisp_ss - sdisp_0).norm(passe_partout_size=passepartout))
print '|ss_pa - disp|        = ' + str((sdisp_ss_pa - sdisp_0).norm(passe_partout_size=passepartout))
print '|euler - disp|        = ' + str((sdisp_euler - sdisp_0).norm(passe_partout_size=passepartout))
print '|midpoint - disp|     = ' + str((sdisp_mid_p - sdisp_0).norm(passe_partout_size=passepartout))
#print '|sdisp_series - disp| = ' + str((sdisp_series - sdisp_0).norm(passe_partout_size=passepartout))
print '|heun - disp|         = ' + str((sdisp_heun - sdisp_0).norm(passe_partout_size=passepartout))
print '|heun_mod - disp|     = ' + str((sdisp_heun_m - sdisp_0).norm(passe_partout_size=passepartout))
print '|rk4 - disp|          = ' + str((sdisp_rk4 - sdisp_0).norm(passe_partout_size=passepartout))

print
print


### Plot:

fields_list = [svf_0, sdisp_0, sdisp_ss,   sdisp_ss_pa,   sdisp_euler,
               sdisp_mid_p, #sdisp_series, 
               sdisp_heun, sdisp_heun_m,  sdisp_rk4]
title_input = ['svf_0', 'sdisp_0', 'sdisp_ss', 'sdisp_ss_pa', 'sdisp_euler', 'disp_mid_p', 'disp_euler_m', 'disp_rk4']
subtract_id = [False, False] + ([False, ] * (len(fields_list) - 2))
input_color = ['r', 'b', 'g', 'c', 'm', 'k', 'b', 'g', 'c']

if 0:
    # See svf and disp in separate fields.
    see_field(svf_0, fig_tag=0,title_input="svf", input_color='r')
    see_field(sdisp_0, fig_tag=1,title_input="disp", input_color='b')

if 0:
    see_overlay_of_n_fields([svf_0, sdisp_0], fig_tag=13,
                            input_color=['r', 'b'],
                            input_label=None)

if 0:
    see_overlay_of_n_fields(fields_list, fig_tag=14,
                            input_color=input_color,
                            input_label=None)

if 0:
    see_2_fields_separate_and_overlay(svf_0, sdisp_0, fig_tag=3)


if 1:
    title_input_l = ['Sfv Input',
                     'Ground Output',
                     'Scaling and Squaring',
                     'Polyaffine Scal. and Sq.',
                     'Euler method',
                     'Midpoint',
                     'Series',
                     'Heun',
                     'Heun Modif',
                     'Runge Kutta 4']

    list_fields_of_field = [[svf_0], [sdisp_0]]
    list_colors = ['r', 'b']
    for third_field in fields_list[2:]:
        list_fields_of_field += [[svf_0, sdisp_0, third_field]]
        list_colors += ['r', 'b', 'm']

    see_n_fields_special(list_fields_of_field, fig_tag=10,
                         colors_input=list_colors,
                         titles_input=title_input_l,
                         sample=(1, 1),
                         zoom_input=[0, 14, 0, 14],
                         window_title_input='matrix, random generated',
                         legend_on=False)

if 0:
    title_input_l = ['Scaling and Squaring',
                     'Polyaffine Scaling and Squaring',
                     'Euler method',
                     'Series',
                     'Midpoint Method',
                     'Euler Modif Method',
                     'Runge Kutta 4']

    for k, third_field in enumerate(fields_list[2::]):
        see_overlay_of_n_fields([svf_0, sdisp_0, third_field], fig_tag=20 + k,
                                title_input=title_input_l[k],
                                input_color=['r', 'b', 'm'],
                                window_title_input='matrix, random generated')


plt.show()