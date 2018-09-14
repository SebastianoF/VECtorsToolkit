import numpy as np
from scipy.linalg import expm, logm


class Pgl2A(object):
    """
    Classes for projective real Lie algebra, general and special, of dimension d.
    Default value d=2.

    https://en.wikipedia.org/wiki/Projective_linear_group

    Real projective general/special linear Lie algebra of dimension d.
    Each element is a (d+1)x(d+1) real matrix defined up to a constant.
    Its exponential is given through the numerical approximation expm.
    If special trace must be zero.
    """
    def __init__(self, d=2, m=np.zeros([3, 3]), special=False):
        """
        """
        if np.array_equal(m.shape, [d + 1] * 2):
            self.matrix = m  # - np.min(m)*np.ones([d+1, d+1])
            self.dim = d
            self.special = special
        else:
            raise IOError
        if special is True and not np.abs(np.trace(m)) < 1e-4:
            raise IOError('input matrix is not in the special projective group')

    def shape(self):
        return self.matrix.shape

    shape = property(shape)

    def ode_solution(self, init_cond=np.array([0, 0, 1]), affine_coordinates=True):
        s = expm(self.matrix).dot(init_cond)
        if affine_coordinates:
            return s[0:self.dim]/s[self.dim]  # the projective coordinate is the last one
        else:
            return s


class Pgl2G(object):
    """
    Real projective general/special linear Lie group of dimension 2.
    Each element is a (d+1)x(d+1) real matrix with non-zero determinant defined up to an element of
    the scalar transformations given by c*I for c constant and I identity matrix.
    It is meant to be generated as exponential of an element of the class pgl_2 with its method exponentiate.
    """
    def __init__(self, d=2, m=np.eye(3), special=False):
        if not isinstance(m, np.ndarray):
            raise IOError
        if np.array_equal(m.shape, [d+1]*2) and not np.linalg.det(m) == 0:
            self.matrix = m
            self.dim = d
            self.special = special
        else:
            raise IOError

    def shape(self):
        return self.matrix.shape

    shape = property(shape)

    def centered_matrix(self, c):
        """
        :param c: center = np.array([x_c, y_c])
        Returns: the matrix correspondent to self, centered in c. Non destructive over c.
        """
        h = self.matrix[:]
        h_prime = np.zeros_like(self.matrix)
        d = self.dim
        if isinstance(c, list):
            c = np.array(c)
        # den = one - Bc
        den = 1 - h[d, :-1].dot(c)

        # A prime
        h_prime[:-1, :-1] = (h[:-1, :-1] + np.kron(c.reshape(1, 2), h[d, :-1].reshape(2, 1)))/den
        # B prime
        h_prime[d, :-1] = (h[d, :-1])/den
        # T prime
        h_prime[:-1, 2] = (-(h[:-1, :-1]).dot(c) - h[d, :-1].dot(c) * c + c)/den

        h_prime[d, d] = 1

        return h_prime

    def centered(self, c):
        """
        Non destructive, provide a new homography as self, translated on c.
        :param c:
        :return:
        """
        return Pgl2G(d=self.dim, m=self.centered_matrix(c))

    def centering(self, c):
        """
        destructive, center the given homography to the given center
        :param c:
        :return:
        """
        self.matrix = self.centered_matrix(c)


def randomgen_Pgl2A(d=2, scale_factor=None, sigma=1.0, special=False):
    """
    Generate a random element in the projective linear algebra
    :param d:
    :param scale_factor:
    :param sigma:
    :param special:
    :return:
    """
    random_h = sigma*np.random.randn(d+1,  d+1)

    if scale_factor is not None:
        random_h = scale_factor * random_h

    if special:
        random_h[0, 0] = -1 * np.sum(np.diagonal(random_h)[1:])

    return Pgl2A(d=d, m=random_h, special=special)


def Pgl2A_exp(pgl2a):
    return Pgl2G(pgl2a.dim, expm(pgl2a.matrix), special=pgl2a.special)


def randomgen_Pgl2G(d=2, center=None, scale_factor=None, sigma=1.0, special=False):
    """
    H = [A, T; B, 1]
    :param d:
    :param center: if we want to center the given matrix.
    :param scale_factor:
    :param sigma:
    :param special:
    :return:
    """
    random_h = sigma * np.random.randn(d+1,  d+1)
    # select one equivalence class.
    random_h[-1, -1] = 1
    # Ensure its matrix logarithm will have real entries.
    random_h = expm(random_h)

    if scale_factor is not None:
        random_h = scale_factor * random_h

    if center is not None:
        random_h = Pgl2G(d=d, m=random_h).centered_matrix(center)

    if special:
        random_h[0, 0] = -1 * np.sum(np.diagonal(random_h)[1:])

    random_h[-1, -1] = 1.

    return Pgl2G(d=d, m=random_h, special=special)


def pgl2a_log(pgl2g):
    return Pgl2A(pgl2g.dim, np.copy(logm(pgl2g.matrix)), special=pgl2g.special)


def randomgen_homography(d=2, center=None, scale_factor=None, sigma=1.0, special=False, get_as_matrix=False,
                         random_kind='diag'):
    """

    :param d:
    :param center:
    :param scale_factor:
    :param sigma:
    :param special:
    :param get_as_matrix:
    :param random_kind:
    :return:
    """
    h_g = randomgen_Pgl2G(d=d, center=center, scale_factor=scale_factor, sigma=sigma, special=special)
    h_g_matrix = h_g.matrix
    if len(center) == 2:
        center = center + [1]
    x_c, y_c, z_c = center

    if random_kind == 'diag':
        h_g_matrix[0, 0] = 1 - (h_g_matrix[0, 1] * y_c + h_g_matrix[0, 2] * z_c) / float(x_c)
        h_g_matrix[1, 1] = 1 - (h_g_matrix[1, 0] * x_c + h_g_matrix[1, 2] * z_c) / float(y_c)
        h_g_matrix[2, 2] = 1 - (h_g_matrix[2, 0] * x_c + h_g_matrix[2, 1] * y_c) / float(z_c)

    elif random_kind == 'skew':
        h_g_matrix[0, 2] = ((1 - h_g_matrix[0, 0]) * x_c - h_g_matrix[0, 1] * y_c) / float(z_c)
        h_g_matrix[1, 0] = ((1 - h_g_matrix[1, 1]) * y_c - h_g_matrix[1, 2] * z_c) / float(x_c)
        h_g_matrix[2, 1] = ((1 - h_g_matrix[2, 2]) * z_c - h_g_matrix[2, 0] * x_c) / float(y_c)

    elif random_kind == 'transl':
        h_g_matrix[0, 2] = (1 - h_g_matrix[0, 0]) * x_c - h_g_matrix[0, 1] * y_c
        h_g_matrix[1, 2] = - h_g_matrix[1, 0] * x_c + (1 - h_g_matrix[1, 1]) * y_c
        h_g_matrix[2, 2] = 1  # - random_h[2, 0] * x_c - random_h[2, 1] * y_c + 1

    elif random_kind == 'shift':
        two_minus_Bc = 2 - h_g_matrix[2, :-1].dot(np.array([x_c, y_c]).T)
        T_plus_c_minus_Ac = h_g_matrix[:-1, 2] + np.array([x_c, y_c]).T - h_g_matrix[-1, :-1].dot(np.array([x_c, y_c]).T)
        # A prime
        h_g_matrix[:-1, :-1] = h_g_matrix[:-1, :-1] / float(two_minus_Bc)
        # B prime
        h_g_matrix[2, :-1] = h_g_matrix[2, :-1] / float(two_minus_Bc)
        # T prime
        h_g_matrix[:-1, 2] = T_plus_c_minus_Ac
        h_g_matrix[2, 2] = 1

    elif random_kind == 's':
        two_minus_Bc = 2 - h_g_matrix[2, :-1].dot(np.array([x_c, y_c]).T)
        T_plus_c_minus_Ac = h_g_matrix[:-1, 2] + np.array([x_c, y_c]).T - h_g_matrix[-1, :-1].dot(np.array([x_c, y_c]).T)
        # A prime
        h_g_matrix[:-1, :-1] = h_g_matrix[:-1, :-1] / float(two_minus_Bc)
        # B prime
        h_g_matrix[2, :-1] = h_g_matrix[2, :-1] / float(two_minus_Bc)
        # T prime
        h_g_matrix[:-1, 2] = T_plus_c_minus_Ac

        h_g_matrix[2, 2] = 1
    else:
        pass

    h_a = pgl2a_log(h_g)

    if get_as_matrix:
        return h_g.matrix, h_a.matrix
    else:
        return h_g, h_a
