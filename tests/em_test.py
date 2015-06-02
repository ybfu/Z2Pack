#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    13.04.2015 10:55:29 CEST
# File:    test_em.py


from common import *

import numpy as np
import warnings
#~ warnings.filterwarnings('ignore', category=DeprecationWarning)

pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
pauli_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)
pauli_vector = list([pauli_x, pauli_y, pauli_z])

class TestEmTestCase(CommonTestCase):

    def tb_hamiltonian(self, k):
        k[2] = -k[2]
        res = np.zeros((2, 2), dtype=complex)
        for kval, p_mat in zip(k, pauli_vector):
            res += kval * p_mat
        return res

    def test_res_0(self):
        system = z2pack.em.System(self.tb_hamiltonian, pos=[[0, 0, 0], [0., 0., 0.]], occ=1)
        surface = system.surface(z2pack.shapes.Sphere([0., 0., 0.], 0.04))
        surface.wcc_calc(pickle_file=None, verbose=False)

        res = {'t_par': [0.0, 0.10000000000000001, 0.20000000000000001, 0.30000000000000004, 0.40000000000000002, 0.5, 0.60000000000000009, 0.70000000000000007, 0.80000000000000004, 0.90000000000000002, 1.0], 'wcc': [[0.0], [0.97700105140316218], [0.90910824353141262], [0.80034213787699182], [0.65926687257349847], [0.5], [0.34073312742650147], [0.19965786212300812], [0.09089175646858734], [0.022998948596837845], [0.0]], 'lambda_': [array([[ 1.+0.j]]), array([[ 0.98957707+0.14400425j]]), array([[ 0.84131241+0.54054919j]]), array([[ 0.31106078+0.95039002j]]), array([[-0.53971039+0.84185076j]]), array([[-1. -5.55111512e-17j]]), array([[-0.53971039-0.84185076j]]), array([[ 0.31106078-0.95039002j]]), array([[ 0.84131241-0.54054919j]]), array([[ 0.98957707-0.14400425j]]), array([[ 1.+0.j]])], 'kpt': [[0.0, 0.0, -0.040000000000000001], [0.012360679774997897, 0.0, -0.038042260651806145], [0.023511410091698926, 0.0, -0.032360679774997896], [0.032360679774997896, 0.0, -0.023511410091698923], [0.038042260651806145, 0.0, -0.012360679774997899], [0.040000000000000001, 0.0, -2.4492935982947064e-18], [0.038042260651806145, 0.0, 0.012360679774997902], [0.032360679774997896, 0.0, 0.023511410091698923], [0.02351141009169893, 0.0, 0.032360679774997896], [0.0123606797749979, 0.0, 0.038042260651806145], [4.8985871965894128e-18, 0.0, 0.040000000000000001]], 'gap': [0.5, 0.47700105140316218, 0.40910824353141262, 0.30034213787699171, 0.15926687257349847, 0.0, 0.84073312742650153, 0.69965786212300807, 0.59089175646858738, 0.52299894859683782, 0.5]}
        self.assertFullAlmostEqual(surface.get_res(), res)

    def test_res_1(self):
        system = z2pack.em.System(self.tb_hamiltonian, pos=[[0.25, 0.25, 0.25], [0., 0., 0.]], occ=1)
        surface = system.surface(z2pack.shapes.Sphere([0., 0., 0.], 0.04))
        surface.wcc_calc(pickle_file=None, verbose=False)

        res = {'t_par': [0.0, 0.10000000000000001, 0.20000000000000001, 0.30000000000000004, 0.40000000000000002, 0.5, 0.60000000000000009, 0.70000000000000007, 0.80000000000000004, 0.90000000000000002, 1.0], 'wcc': [[0.0], [0.97739579390899423], [0.91046316400096627], [0.80258295121698775], [0.66135676934080723], [0.5], [0.33652292044623267], [0.18998205512816774], [0.075954376465955709], [0.0043379091081855977], [0.97999999999999998]], 'lambda_': [array([[ 1.+0.j]]), array([[ 0.98993119+0.14154942j]]), array([[ 0.84588368+0.53336741j]]), array([[ 0.32441047+0.94591641j]]), array([[-0.52860966+0.84886502j]]), array([[-1. -2.77555756e-16j]]), array([[-0.51725425-0.85583178j]]), array([[ 0.36822938-0.92973497j]]), array([[ 0.88826816-0.45932525j]]), array([[ 0.99962858-0.02725251j]]), array([[ 0.9921147+0.12533323j]])], 'kpt': [[0.0, 0.0, -0.040000000000000001], [0.012360679774997897, 0.0, -0.038042260651806145], [0.023511410091698926, 0.0, -0.032360679774997896], [0.032360679774997896, 0.0, -0.023511410091698923], [0.038042260651806145, 0.0, -0.012360679774997899], [0.040000000000000001, 0.0, -2.4492935982947064e-18], [0.038042260651806145, 0.0, 0.012360679774997902], [0.032360679774997896, 0.0, 0.023511410091698923], [0.02351141009169893, 0.0, 0.032360679774997896], [0.0123606797749979, 0.0, 0.038042260651806145], [4.8985871965894128e-18, 0.0, 0.040000000000000001]], 'gap': [0.5, 0.47739579390899411, 0.41046316400096616, 0.30258295121698775, 0.16135676934080712, 0.0, 0.83652292044623267, 0.68998205512816768, 0.57595437646595571, 0.50433790910818554, 0.47999999999999998]}
        self.assertFullAlmostEqual(surface.get_res(), res)
        
    def test_res_2(self):
        system = z2pack.em.System(self.tb_hamiltonian, pos=[[0.25, 0.25, 0.25], [0., 0., 0.]], occ=2)
        surface = system.surface(z2pack.shapes.Sphere([0., 0., 0.], 0.04))
        surface.wcc_calc(pickle_file=None, verbose=False)

        res = {'t_par': [0.0, 0.10000000000000001, 0.20000000000000001, 0.30000000000000004, 0.40000000000000002, 0.5, 0.60000000000000009, 0.70000000000000007, 0.80000000000000004, 0.90000000000000002, 1.0], 'wcc': [[0.0, 0.02], [0.019021130325903118, 1.0], [0.016180339887498958, 0.99999999999999989], [0.011755705045849437, 0.99999999999999989], [4.8591807633470389e-17, 0.0061803398874989398], [4.5278729840279209e-17, 1.0], [4.4174370575882209e-18, 0.993819660112501], [0.98824429495415056, 1.0], [0.98381966011250099, 0.99999999999999989], [0.98097886967409686, 1.0], [4.417437057588214e-18, 0.97999999999999998]], 'lambda_': [array([[ 0.9921147-0.12533323j,  0.0000000+0.j        ],
       [ 0.0000000+0.j        ,  1.0000000+0.j        ]]), array([[ 0.99304135-0.11631124j,  0.00110214+0.01842189j],
       [ 0.00110214+0.01842189j,  0.99982544-0.00291774j]]), array([[ 0.99532971-0.0917977j ,  0.00151747+0.02982688j],
       [ 0.00151747+0.02982688j,  0.99950694-0.00969134j]]), array([[ 0.99783533-0.0585862j ,  0.00110295+0.02985116j],
       [ 0.00110295+0.02985116j,  0.99943802-0.01520993j]]), array([[  9.99506582e-01-0.02540963j,   3.58489315e-04+0.01846118j],
       [  3.58489315e-04+0.01846118j,   9.99739542e-01-0.01341283j]]), array([[  1.00000000e+00 +1.38777878e-16j,
          2.91433544e-16 +5.55111512e-16j],
       [  1.11022302e-16 +2.77555756e-17j,
          1.00000000e+00 -2.49800181e-16j]]), array([[  9.99506582e-01+0.02540963j,  -3.58489315e-04+0.01846118j],
       [ -3.58489315e-04+0.01846118j,   9.99739542e-01+0.01341283j]]), array([[ 0.99783533+0.0585862j , -0.00110295+0.02985116j],
       [-0.00110295+0.02985116j,  0.99943802+0.01520993j]]), array([[ 0.99532971+0.0917977j , -0.00151747+0.02982688j],
       [-0.00151747+0.02982688j,  0.99950694+0.00969134j]]), array([[ 0.99304135+0.11631124j, -0.00110214+0.01842189j],
       [-0.00110214+0.01842189j,  0.99982544+0.00291774j]]), array([[  9.92114701e-01 +1.25333234e-01j,
         -1.23259516e-32 +6.77927340e-32j],
       [ -3.69778549e-32 +6.16297582e-33j,
          1.00000000e+00 -6.96033324e-32j]])], 'kpt': [[0.0, 0.0, -0.040000000000000001], [0.012360679774997897, 0.0, -0.038042260651806145], [0.023511410091698926, 0.0, -0.032360679774997896], [0.032360679774997896, 0.0, -0.023511410091698923], [0.038042260651806145, 0.0, -0.012360679774997899], [0.040000000000000001, 0.0, -2.4492935982947064e-18], [0.038042260651806145, 0.0, 0.012360679774997902], [0.032360679774997896, 0.0, 0.023511410091698923], [0.02351141009169893, 0.0, 0.032360679774997896], [0.0123606797749979, 0.0, 0.038042260651806145], [4.8985871965894128e-18, 0.0, 0.040000000000000001]], 'gap': [0.51000000000000001, 0.50951056516295157, 0.50809016994374945, 0.50587785252292461, 0.50309016994374944, 0.5, 0.4969098300562505, 0.49412214747707539, 0.49190983005625055, 0.49048943483704832, 0.48999999999999999]}
        self.assertFullAlmostEqual(surface.get_res(), res)
        
    def test_res_3(self):
        system1 = z2pack.em.System(self.tb_hamiltonian, pos=[[0.25, 0.25, 0.25], [0., 0., 0.]], occ=1)
        surface1 = system1.surface(z2pack.shapes.Sphere([0., 0., 0.], 0.04))
        surface1.wcc_calc(pickle_file=None, verbose=False)

        system2 = z2pack.em.System(self.tb_hamiltonian, pos=[[0.25, 0.25, 0.25], [0., 0., 0.]])
        surface2 = system2.surface(z2pack.shapes.Sphere([0., 0., 0.], 0.04))
        surface2.wcc_calc(pickle_file=None, verbose=False)

        self.assertFullAlmostEqual(surface1.get_res(), surface2.get_res())
        
    def test_res_4(self):
        system1 = z2pack.em.System(self.tb_hamiltonian, pos=[[0., 0., 0.], [0., 0., 0.]], occ=1)
        surface1 = system1.surface(z2pack.shapes.Sphere([0., 0., 0.], 0.04))
        surface1.wcc_calc(pickle_file=None, verbose=False)

        system2 = z2pack.em.System(self.tb_hamiltonian, occ = 1)
        surface2 = system2.surface(z2pack.shapes.Sphere([0., 0., 0.], 0.04))
        surface2.wcc_calc(pickle_file=None, verbose=False)

        self.assertFullAlmostEqual(surface1.get_res(), surface2.get_res())

    def test_error(self):
        self.assertRaises(ValueError, z2pack.em.System, lambda k: [[1]], occ=1, pos=[[0., 0., 0.], [0.5, 0.5, 0.5]])

if __name__ == "__main__":
    unittest.main()    
