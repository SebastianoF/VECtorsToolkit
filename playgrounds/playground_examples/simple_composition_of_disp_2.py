import matplotlib.pyplot as plt
import numpy as np

from VECtorsToolkit.tools.fields.composition import lagrangian_dot_lagrangian
from VECtorsToolkit.tools.visualisations.fields.fields_at_the_window import see_field

if __name__ == '__main__':
    shape = (6, 6, 1, 1, 2)

    svf_f   = np.zeros(shape)
    svf_g   = np.zeros(shape)


    def function_f(t, x):
        t = float(t)
        x = [float(y) for y in x]
        return np.array([0, 0.3])


    def function_g(t, x):
        t = float(t)
        x = [float(y) for y in x]
        return np.array([0, -0.3])


    for x in range(0, 6):
        for y in range(0, 6):
            svf_f[x, y, 0, 0, :] = function_f(1, [x, y])
            svf_g[x, y, 0, 0, :] = function_g(1, [x, y])

    f_o_g = lagrangian_dot_lagrangian(svf_f, svf_g)
    g_o_f = lagrangian_dot_lagrangian(svf_g, svf_f)

    see_field(svf_f, fig_tag=2, input_color='b')
    see_field(svf_g, fig_tag=2, input_color='r')
    see_field(f_o_g, fig_tag=2, input_color='g', title_input='composition (f o g) in green')

    see_field(svf_f, fig_tag=3, input_color='b')
    see_field(svf_g, fig_tag=3, input_color='r')
    see_field(g_o_f, fig_tag=3, input_color='g', title_input='composition (g o f) in green')

    plt.show()
