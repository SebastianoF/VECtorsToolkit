import os
import time
from os.path import join as jph
from collections import OrderedDict

import tabulate
import pandas as pd
import numpy as np
import seaborn as sns
import nibabel as nib
import nilabels as nis
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sympy.core.cache import clear_cache

from nilabels.tools.aux_methods.utils import print_and_run
from nilabels.tools.aux_methods.utils_nib import set_new_data

from calie.fields import queries as qr
from calie.fields import coordinate as coord

from benchmarking.a_main_controller import methods, spline_interpolation_order, steps
from benchmarking.b_path_manager import pfo_output_A4_AD, pfo_adni
"""
Module for the computation of a dataset of 3d SFV generated out of ADNI data-set.
Longitudinal SVF experiment.
It compares computational time and error for the exponential computation with different methods and time steps.
"""

if __name__ == '__main__':

    clear_cache()

    # controller

    control = {'generate_dataset'   : True,
                   'generate_dataset_aff'        : True,
                   'generate_dataset_nrig'       : True,
                   'generate_dataset_get_svf'    : True,
                   'generate_dataset_get_exp_svf_group_algebra'    : True,
               'compute_exps'       : True,
               'get_statistics'     : True,
               'show_graphs'        : True}

    verbose = 1
    nifty_reg_source = ''

    # parameters:

    z_val = 130  # single slice selected for the computation of the exponential

    params = OrderedDict()

    x_1, y_1, z_1 = 50, 50, 50
    if z_1 == 1:
        omega = (x_1, y_1)
    else:
        omega = (x_1, y_1, z_1)

    centre_delta = (5, 5, 5)

    params.update({'experiment id'      : 'ex1'})
    params.update({'subjects_FirstTP'   : ['4039_01', '4172_01', '4195_01', '4379_01', '4501_01', '4526_01', '4625_01', '4657_01',
                                            '4672_01', '4676_01']})
    params.update({'subjects_SecondTP'  : ['4039_05', '4172_05', '4195_05', '4379_04', '4501_05', '4526_05', '4625_01', '4657_01',
                                            '4672_04', '4676_05']})
    params.update({'selected_ground'    : 'rk4'})
    params.update({'selected_n_steps'   : 7})
    params.update({'passepartout'       : 5})
    params.update({'sio'                : spline_interpolation_order})
    params.update({'steps'              : steps})

    # Path manager

    print("\nPath to results folder {}\n".format(pfo_output_A4_AD))

    ####################
    # Generate dataset #
    ####################

    if control['generate_dataset']:

        print('---------------------------------------------------------------------------')
        print('Generating dataset ADNI! filename: ad-<s>-<algebra/group>.npy sj in BrainWeb ')
        print('---------------------------------------------------------------------------')

        # prepare dataset to obtain 38 realistic svf
        # for each subject, skull strip and save with their masks
        # and then register all to one (target_sj) with the brain tissue mask.

        if control['generate_dataset_aff']:

            for sj_first_tp, sj_second_tp in zip(params['subjects_FirstTP'], params['subjects_SecondTP']):
                print('--------------------------------------------------')
                print('Affine registration to target, sj first tp {}, second tp {}\n'.format(sj_first_tp, sj_second_tp))

                pfi_T1W_fixed_tp1 = jph(pfo_output_A4_AD, 'FirstTP', 'MaskedT1_{}.nii.gz'.format(sj_first_tp))
                pfi_mask_fixed_tp1 = jph(pfo_output_A4_AD, 'FirstTP', '{}_GIF_B1.nii.gz'.format(sj_first_tp))

                pfi_T1W_moving_tp2  = jph(pfo_output_A4_AD, 'LastTP', 'MaskedT1_{}.nii.gz'.format(sj_second_tp))
                pfi_mask_moving_tp2 = jph(pfo_output_A4_AD, 'LastTP', '{}_GIF_B1.nii.gz'.format(sj_second_tp))

                assert os.path.exists(pfi_T1W_fixed_tp1), pfi_T1W_fixed_tp1
                assert os.path.exists(pfi_mask_fixed_tp1), pfi_mask_fixed_tp1

                assert os.path.exists(pfi_T1W_moving_tp2), pfi_T1W_moving_tp2
                assert os.path.exists(pfi_mask_moving_tp2), pfi_mask_moving_tp2

                pfi_moving_on_target_warp_aff = jph(pfo_output_A4_AD, '{}_on_{}_warp_aff.nii.gz'.format(sj_second_tp, sj_first_tp))
                pfi_moving_on_target_aff = jph(pfo_output_A4_AD, '{}_on_{}_aff.txt'.format(sj_second_tp, sj_first_tp))
                cmd = 'reg_aladin -ref {0} -rmask {1} -flo {2} -fmask {3} -res {4} -aff {5} -speeeeed '.format(
                    pfi_T1W_fixed_tp1, pfi_mask_fixed_tp1, pfi_T1W_moving_tp2, pfi_mask_moving_tp2,
                    pfi_moving_on_target_warp_aff, pfi_moving_on_target_aff
                )
                print_and_run(cmd)

                pfi_moving_on_target_mask_aff = jph(pfo_output_A4_AD, '{}_on_{}_mask_warp_aff.nii.gz'.format(sj_second_tp, sj_first_tp))

                cmd = 'reg_resample -ref {0} -flo {1} -trans {2} -res {3} -inter 0 '.format(
                    pfi_T1W_fixed_tp1, pfi_mask_moving_tp2, pfi_moving_on_target_aff, pfi_moving_on_target_mask_aff
                )
                print_and_run(cmd)

        if control['generate_dataset_nrig']:

            for sj_first_tp, sj_second_tp in zip(params['subjects_FirstTP'], params['subjects_SecondTP']):

                print('--------------------------------------------------------------------------------------------------')
                print('Non-rigid registration to target, sj first tp {}, second tp {}\n'.format(sj_first_tp, sj_second_tp))

                pfi_T1W_fixed_tp1 = jph(pfo_output_A4_AD, 'FirstTP', 'MaskedT1{}.nii.gz'.format(sj_first_tp))
                pfi_mask_fixed_tp1 = jph(pfo_output_A4_AD, 'FirstTP', '{}_GIF_B1.nii.gz'.format(sj_first_tp))

                pfi_moving_on_target_warp_aff = jph(pfo_output_A4_AD, '{}_on_{}_warp_aff.nii.gz'.format(sj_second_tp, sj_first_tp))
                pfi_moving_on_target_mask_aff = jph(pfo_output_A4_AD, '{}_on_{}_mask_warp_aff.nii.gz'.format(sj_second_tp, sj_first_tp))

                assert os.path.exists(pfi_moving_on_target_warp_aff), pfi_moving_on_target_warp_aff
                assert os.path.exists(pfi_moving_on_target_mask_aff), pfi_moving_on_target_mask_aff

                pfi_cpp = jph(pfo_output_A4_AD, '{}_on_{}_cpp.nii.gz'.format(sj_second_tp, sj_first_tp))
                pfi_moving_on_target_nrig = jph(pfo_output_A4_AD, '{}_on_{}_warp_nrig.nii.gz'.format(sj_second_tp, sj_first_tp))

                cmd = 'reg_f3d -ref {0} -rmask {1} -flo {2} -fmask {3} -cpp {4} -res {5} -vel '.format(
                    pfi_T1W_fixed_tp1, pfi_mask_fixed_tp1, pfi_moving_on_target_warp_aff, pfi_moving_on_target_mask_aff,
                    pfi_cpp, pfi_moving_on_target_nrig
                )
                print_and_run(cmd)

        if control['generate_dataset_get_svf']:

            for sj_first_tp, sj_second_tp in zip(params['subjects_FirstTP'], params['subjects_SecondTP']):

                print('--------------------------------------------------------------------------------------')
                print('Get the svf from cpp, sj first tp {}, second tp {}\n'.format(sj_first_tp, sj_second_tp))

                pfi_T1W_fixed_tp1 = jph(pfo_output_A4_AD, 'FirstTP', 'MaskedT1{}.nii.gz'.format(sj_first_tp))
                assert os.path.exists(pfi_T1W_fixed_tp1), pfi_T1W_fixed_tp1

                pfi_cpp = jph(pfo_output_A4_AD, '{}_on_{}_cpp.nii.gz'.format(sj_second_tp, sj_first_tp))
                assert os.path.exists(pfi_cpp), pfi_cpp

                sj = sj_first_tp.split('-')[0]

                pfi_svf1_eul = jph(pfo_output_A4_AD, 'pre_svf-{}.nii.gz'.format(sj))
                pfi_svf1 = jph(pfo_output_A4_AD, 'svf-{}.nii.gz'.format(sj))

                cmd = 'reg_transform -ref {0} -flow {1} {2}'.format(
                    pfi_T1W_fixed_tp1, pfi_cpp, pfi_svf1_eul
                )
                print_and_run(cmd)

                # go in Lagrangian coordinates.
                im_sfv1_eul = nib.load(pfi_svf1_eul)

                data_svf1_lag = coord.eulerian_to_lagrangian(im_sfv1_eul.get_data())

                im_svf_lag = set_new_data(im_sfv1_eul, data_svf1_lag)

                nib.save(im_svf_lag, pfi_svf1)

        if control['generate_dataset_get_exp_svf_group_algebra']:

            for sj_first_tp, sj_second_tp in zip(params['subjects_FirstTP'], params['subjects_SecondTP']):

                sj = sj_first_tp.split('-')[0]

                print('--------------------------------------------------')
                print('Exponentiate the obtained SVF, sj {}'.format(sj))

                pfi_svf1 = jph(pfo_output_A4_AD, 'svf-{}.nii.gz'.format(sj))
                assert os.path.exists(pfi_svf1)
                im_svf1 = nib.load(pfi_svf1)

                # take only one slice:
                svf1_3d = im_svf1.get_data()
                shape = list(svf1_3d.shape)
                shape[2] = 1
                shape[-1] = 2

                svf1 = np.zeros(shape)
                svf1[..., 0, 0, 0] = svf1_3d[:, :, z_val, 0, 0]
                svf1[..., 0, 0, 1] = svf1_3d[:, :, z_val, 0, 1]

                flow1_ground = methods[params['selected_ground']][0](svf1, input_num_steps=params['selected_n_steps'])

                pfi_svf1 = jph(pfo_output_A4_AD, 'ad-{}-algebra.npy'.format(sj))
                pfi_flow = jph(pfo_output_A4_AD, 'ad-{}-group.npy'.format(sj))

                np.save(pfi_svf1, svf1)
                np.save(pfi_flow, flow1_ground)

                print('svf saved in {}'.format(pfi_svf1))
                print('flow (dummy ground truth) saved in {}'.format(pfi_flow))

        print('\n------------------------------------------')
        print('Data computed and saved in external files!')
        print('------------------------------------------')

    else:

        for sj in set(params['subjects']) - {params['target_sj']}:
            pfi_svf1 = jph(pfo_output_A4_AD, 'ad-{}-algebra.npy'.format(sj))
            pfi_flow = jph(pfo_output_A4_AD, 'ad-{}-group.npy'.format(sj))
            assert os.path.exists(pfi_svf1), pfi_svf1
            assert os.path.exists(pfi_flow), pfi_flow

    ###########################
    #   Compute exponentials  #
    ###########################

    print('--------------------------------------------------------------------------')
    print('Compute exponentials ADNI! filename: ad-<method>-STEPS_<steps>.csv        ')
    print('--------------------------------------------------------------------------')

    if control['compute_exps']:

        for method_name in [k for k in methods.keys() if methods[k][1]]:

            # matrices for tabulation:
            tab_errors = np.zeros([params['num_samples'], len(params['steps'])])
            tab_comp_time = np.zeros([params['num_samples'], len(params['steps'])])

            for st in params['steps']:

                print('\n Computing method {} for steps {}'.format(method_name, st))

                exp_method = methods[method_name][0]
                sub_method = methods[method_name][6]

                # initialise pandas df
                df_time_error = pd.DataFrame(columns=['subject', 'time (sec)', 'error (mm)'],
                                             index=range(params['num_samples']))

                for s in range(params['num_samples']):

                    pfi_svf0 = jph(pfo_output_A4_AD, 'ad-{}-algebra.npy'.format(s + 1))
                    pfi_flow = jph(pfo_output_A4_AD, 'ad-{}-group.npy'.format(s + 1))

                    svf1         = np.load(pfi_svf0)
                    flow1_ground = np.load(pfi_flow)

                    if methods[method_name][6]:
                        raise IOError('TODO for point-wise methods differentiate vode, lsoda')

                    # compute exponetial with time:
                    start = time.time()
                    disp_computed = exp_method(svf1, input_num_steps=st)
                    stop = (time.time() - start)

                    # compute error:
                    error = qr.norm(disp_computed - flow1_ground, passe_partout_size=params['passepartout'], normalized=True)

                    df_time_error['subject'][s] = 'sj{}'.format(s+1)
                    df_time_error['time (sec)'][s] = stop
                    df_time_error['error (mm)'][s] = error

                # save pandas df in csv
                pfi_df_time_error = jph(pfo_output_A4_AD, 'ad-{}-steps-{}.csv'.format(method_name, st))
                df_time_error.to_csv(pfi_df_time_error)

                # print something if you fancy:
                if verbose == 2:
                    print(df_time_error)
                if verbose == 1:
                    tab_errors[:, params['steps'].index(st)] = df_time_error['error (mm)'].values
                    tab_comp_time[:, params['steps'].index(st)] = df_time_error['time (sec)'].values

                    print('\n')
                    print('Errors:')
                    print(tabulate.tabulate(tab_errors, headers=['steps {}'.format(s) for s in params['steps']]))
                    print('Computational time:')
                    print(tabulate.tabulate(tab_comp_time, headers=['steps {}'.format(s) for s in params['steps']]))
                    print('\n')

    else:

        # assert pandas dataframes exists
        for method_name in [k for k in methods.keys() if methods[k][1]]:
            for st in params['steps']:
                pfi_df_time_error = jph(pfo_output_A4_AD, 'ad-{}-steps-{}.csv'.format(method_name, st))
                assert os.path.exists(pfi_df_time_error), pfi_df_time_error

    ##################
    # get statistics #
    ##################

    if control['get_statistics']:

        # for each method get mean and std indexed by num-steps.
        # | steps | mu_error | sigma_error | mu_time | sigma_error |
        # in a file called ad-stats-<method>.csv

        for method_name in [k for k in methods.keys() if methods[k][1]]:

            print('------------------------------------------------')
            print('\n Statistics for method {} '.format(method_name))

            df_mean_std = pd.DataFrame(columns=['steps', 'mu_time', 'std_time', 'mu_error', 'std_error'],
                                       index=range(len(params['steps'])))

            for st_index, st in enumerate(params['steps']):

                print('\n Steps {}'.format(st))

                pfi_df_time_error = jph(pfo_output_A4_AD, 'ad-{}-steps-{}.csv'.format(method_name, st))
                df_time_error = pd.read_csv(pfi_df_time_error)

                df_mean_std['steps'][st_index] = st

                df_mean_std['mu_time'][st_index]  = df_time_error['time (sec)'].mean()
                df_mean_std['std_time'][st_index] = df_time_error['time (sec)'].std()

                df_mean_std['mu_error'][st_index]  = df_time_error['error (mm)'].mean()
                df_mean_std['std_error'][st_index] = df_time_error['error (mm)'].std()

            pfi_df_mean_std = jph(pfo_output_A4_AD, 'ad-stats-{}.csv'.format(method_name))
            df_mean_std.to_csv(pfi_df_mean_std)

    else:

        for method_name in [k for k in methods.keys() if methods[k][1]][:1]:
            pfi_df_mean_std = jph(pfo_output_A4_AD, 'ad-stats-{}.csv'.format(method_name))
            assert os.path.exists(pfi_df_mean_std), pfi_df_mean_std

    ###############
    # show graphs #
    ###############

    if control['show_graphs']:

        font_top = {'family': 'serif', 'color': 'darkblue', 'weight': 'normal', 'size': 14}
        font_bl = {'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 12}
        legend_prop = {'size': 12}

        sns.set_style()

        fig, ax = plt.subplots(figsize=(7, 7))

        fig.canvas.set_window_title('ad_times_vs_errors.pdf')

        for method_name in [k for k in methods.keys() if methods[k][1]]:

            pfi_df_mean_std = jph(pfo_output_A4_AD, 'ad-stats-{}.csv'.format(method_name))
            df_mean_std = pd.read_csv(pfi_df_mean_std)

            ax.plot(df_mean_std['mu_time'].values,
                    df_mean_std['mu_error'].values,
                    label=method_name,
                    color=methods[method_name][3],
                    linestyle=methods[method_name][4],
                    marker=methods[method_name][5])

            for i in df_mean_std.index:
                el = mpatches.Ellipse((df_mean_std['mu_time'][i], df_mean_std['mu_error'][i]),
                                      df_mean_std['std_time'][i], df_mean_std['std_error'][i],
                                      angle=0,
                                      alpha=0.2,
                                      color=methods[method_name][3],
                                      linewidth=None)
                ax.add_artist(el)

        ax.set_title('Time error for SE(2)', fontdict=font_top)
        ax.legend(loc='upper right', shadow=True, prop=legend_prop)

        ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        ax.set_axisbelow(True)

        ax.set_xlabel('Time (sec)', fontdict=font_bl, labelpad=5)
        ax.set_ylabel('Error (mm)', fontdict=font_bl, labelpad=5)
        ax.set_xscale('log', nonposx="mask")
        ax.set_yscale('log', nonposy="mask")

        pfi_figure_time_vs_error = jph(pfo_output_A4_AD, 'graph_time_vs_error.pdf')
        plt.savefig(pfi_figure_time_vs_error, dpi=150)

        plt.show(block=True)