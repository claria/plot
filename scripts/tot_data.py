#!/usr/bin/env python2
import os
import sys
import numpy as np
import collections

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.root_tools import get_np_object, get_root_object
from util.root2np import R2npObject1D
import ROOT

nongaussian_unc = {
'yb0ys0': np.array([ 0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.11,  0.08,  0.07,  0.22,  0.06,  0.0 ,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.0 ,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.0 ,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.  ]),
'yb0ys1': np.array([  0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.37,   0.32,   0.1 ,   0.0 ,   0.00,   0.00,   0.00,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,  00.00,   0.  ,
         0.  ,   0.  ,   0.  ]),
'yb0ys2' : np.array([  0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   1.46,   1.19,   1.62,   1.38,   1.68,   0.31,   0.00,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,
         0.00,  00.00,  00.00,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ]),
'yb1ys0' :np.array([  0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.43,   0.4 ,   0.33,   0.34,   0.29,   0.13,   0.0 ,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.0 ,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,
         0.00,   0.00,   0.00,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ]),
'yb1ys1' : np.array([ 0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        1.19,  1.18,  1.01,  1.42,  1.11,  0.97,  0.5 ,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ]),
'yb2ys0' : np.array([  0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   1.8 ,   1.69,   1.17,   1.81,   1.78,   2.38,   1.08,
         0.64,   0.  ,   0.  ,   0.  ,   0.  ,   0.00,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ])
}


def main():
    pass
    ybys_bins = ['yb0ys0', 'yb0ys1', 'yb0ys2', 'yb1ys0', 'yb1ys1', 'yb2ys0']
    def get_coltype(s):
        if s in ['yb_low', 'yb_high', 'ys_low', 'ys_high',  'pt_low', 'pt_high', 'NPCorr', 'nbin']:
            return 'Bin'
        elif s in ['sigma']:
            return 'Sigma'
        else:
            return 'Error'

    f = ROOT.TFile('data_summary.root', 'RECREATE')

    for i, ybys_bin in enumerate(ybys_bins):
        # unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO_WITHFAKES.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root.Scale(1.0, 'width')
        unf_data = R2npObject1D(unf_data_root)
        np_factor = get_np_object('~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor'.format(ybys_bin))

        jer_data = get_np_object('~/dust/dijetana/plot/plots/jer_uncert_{0}.root?jer_uncert'.format(ybys_bin))

        data = collections.OrderedDict()
        data['nbin'] = np.array([i] * len(unf_data.xl))
        data['yb_low'] = np.array([float(ybys_bin[2])] * len(unf_data.xl))
        data['yb_high'] = np.array([float(ybys_bin[2]) + 1.0] * len(unf_data.xl))
        data['ys_low'] = np.array([float(ybys_bin[5])] * len(unf_data.xl))
        data['ys_high'] = np.array([float(ybys_bin[5]) + 1.0] * len(unf_data.xl))
        data['pt_low'] = unf_data.xl
        data['pt_high'] = unf_data.xu
        data['sigma'] = unf_data.y
        data['uncor'] = np.array([1.0] * len(unf_data.xl))
        data['stat'] = unf_data.yerr/unf_data.y * 100.
        data['jer_up'] = jer_data.yerru/jer_data.y * 100.
        data['jer_dn'] = jer_data.yerrl/jer_data.y * 100.
        # lumi
        lumi_unc = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/lumi_unc_relative.root?{0}/lumi_unc_up'.format(ybys_bin))
        data['lumi'] = (lumi_unc.y - 1.) * 100.

        # non-gaussian tails
        # unf_smeared = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/SMEARED_NEW2_QCDMGP6.root?{0}/h_ptavg'.format(ybys_bin))
        # unf_scaled = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/SMEARED_OLD_QCDMGP6.root?{0}/h_ptavg'.format(ybys_bin))
        # data['nongaussiantails'] = np.abs(unf_smeared.y - unf_scaled.y)/unf_smeared.y / 2.0 * 100.
        data['nongaussiantails'] = nongaussian_unc[ybys_bin] 
        # data['nongaussiantails'] = smooth(data['nongaussiantails'], 3)
        # np.set_printoptions(precision=2)
        # np.set_printoptions(suppress=True)
        # print ybys_bin, np.array_repr(np.nan_to_num(data['nongaussiantails']))



        jec_sources  = [
                       'AbsoluteScale','AbsoluteStat','AbsoluteMPFBias',
                       'Fragmentation',
                       'SinglePionECAL',
                       'SinglePionHCAL',
                       'FlavorQCD',
                       'RelativeJEREC1','RelativeJEREC2','RelativeJERHF',
                       'RelativePtBB','RelativePtEC1','RelativePtEC2','RelativePtHF',
                       'RelativeFSR',
                       'RelativeStatEC2', 'RelativeStatHF', 'RelativeStatFSR',
                       'PileUpDataMC',
                       'PileUpPtRef',
                       'PileUpPtBB','PileUpPtEC1','PileUpPtEC2','PileUpPtHF',
                       ]

        jec_default = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}/h_genptavg'.format(ybys_bin))
        for jec_source in jec_sources:
            jec_up = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_{1}_up/h_genptavg'.format(ybys_bin, jec_source))
            jec_dn = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_{1}_dn/h_genptavg'.format(ybys_bin, jec_source))
            # data['{0}_up'.format(jec_source)] = jec_up.y/jec_default.y -1.
            # data['{0}_dn'.format(jec_source)] = 1. - jec_dn.y/jec_default.y
            # data['{0}'.format(jec_source)] = np.abs((jec_up.y - jec_dn.y)/2.0)/jec_default.y * 100.

            data['{0}_up'.format(jec_source)] = ((np.maximum(np.maximum(jec_up.y - jec_default.y, jec_dn.y - jec_default.y), 0))/ jec_default.y) * 100.
            data['{0}_dn'.format(jec_source)] = ((np.maximum(np.maximum(jec_default.y - jec_up.y, jec_default.y - jec_dn.y), 0))/ jec_default.y) * 100.
            # data['{0}_sym'.format(jec_source)] = np.maximum(np.abs(1. - jec_up.y/jec_default.y), np.abs(1. - jec_dn.y/jec_default.y)) * 100.
            data['{0}_sym'.format(jec_source)] = 0.5 *( (jec_up.y -jec_dn.y)/jec_default.y) * 100.
            # data['{0}'.format(jec_source)] = np.abs(1 - jec_up.y/jec_default.y) * 100.

        jec_total_up = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_Total_up/h_genptavg'.format(ybys_bin))
        jec_total_dn = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_Total_dn/h_genptavg'.format(ybys_bin))
        data['Total_up'.format(jec_source)] = ((np.maximum(np.maximum(jec_total_up.y - jec_default.y, jec_total_dn.y - jec_default.y), 0))/ jec_default.y) * 100.
        data['Total_dn'.format(jec_source)] = ((np.maximum(np.maximum(jec_default.y - jec_total_up.y, jec_default.y - jec_total_dn.y), 0))/ jec_default.y) * 100.

        for k,v in data.iteritems():
            v[np.isnan(v)] = 0.
            v[np.isinf(v)] = 0.

        #sums
        stat_error_u = data['sigma'] * (data['stat']/100.)
        stat_error_l = data['sigma'] * (data['stat']/100.)
        syst_error_u = np.zeros((len(data['sigma'])))
        syst_error_l = np.zeros((len(data['sigma'])))

        jec_error_u = np.zeros((len(data['sigma'])))
        jec_error_l = np.zeros((len(data['sigma'])))

        jec_total_error_u = (data['Total_up']/100.) * data['sigma']
        jec_total_error_l = (data['Total_dn']/100.) * data['sigma']

        jer_error_u = np.zeros((len(data['sigma'])))
        jer_error_l = np.zeros((len(data['sigma'])))

        nongaussian_error_u = np.zeros((len(data['sigma'])))
        nongaussian_error_l = np.zeros((len(data['sigma'])))



        unc_error_u = np.zeros((len(data['sigma'])))
        unc_error_l = np.zeros((len(data['sigma'])))

        lumi_error_u = np.zeros((len(data['sigma'])))
        lumi_error_l = np.zeros((len(data['sigma'])))

        lumi_error_u = data['lumi']/100. * data['sigma']
        lumi_error_l = data['lumi']/100. * data['sigma']

        unc_error_u = data['uncor']/100. * data['sigma']
        unc_error_l = data['uncor']/100. * data['sigma']

        jer_error_u = data['jer_up']/100. * data['sigma']
        jer_error_l = data['jer_dn']/100. * data['sigma']

        nongaussian_error_u = data['nongaussiantails']/100. * data['sigma']
        nongaussian_error_l = data['nongaussiantails']/100. * data['sigma']

        syst_error_u += (data['nongaussiantails']/100. * data['sigma'])**2
        syst_error_l += (data['nongaussiantails']/100. * data['sigma'])**2

        syst_error_u += (data['uncor']/100. * data['sigma'])**2
        syst_error_l += (data['uncor']/100. * data['sigma'])**2

        syst_error_u += (data['lumi']/100. * data['sigma'])**2
        syst_error_l += (data['lumi']/100. * data['sigma'])**2



        for jec_source in jec_sources:
            syst_error_u += (data['{0}_up'.format(jec_source)]/100. * data['sigma'])**2
            syst_error_l += (data['{0}_dn'.format(jec_source)]/100. * data['sigma'])**2

            jec_error_u += (data['{0}_up'.format(jec_source)]/100. * data['sigma'])**2
            jec_error_l += (data['{0}_dn'.format(jec_source)]/100. * data['sigma'])**2

        jec_error_u = np.sqrt(jec_error_u)
        jec_error_l = np.sqrt(jec_error_l)
        # jec_error_u = jec_total_error_u 
        # jec_error_l = jec_total_error_l 

        syst_error_u = np.sqrt(syst_error_u)
        syst_error_l = np.sqrt(syst_error_l)


        f.cd()
        f.mkdir(ybys_bin)
        f.Cd("/" + ybys_bin)

        data_tot = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_stat = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_syst = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_lumi = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_unc = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_jec = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_jer = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_nongaussian = ROOT.TGraphAsymmErrors(len(data['sigma'])) 

        for i in range(len(data['sigma'])):
            data_tot.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_tot.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], np.sqrt(stat_error_l[i]**2+syst_error_l[i]**2), np.sqrt(stat_error_u[i]**2+syst_error_u[i]**2))

            data_stat.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_stat.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], stat_error_l[i], stat_error_u[i])

            data_syst.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_syst.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], syst_error_l[i], syst_error_u[i])

            data_lumi.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_lumi.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], lumi_error_l[i], lumi_error_u[i])

            data_unc.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_unc.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], unc_error_l[i], unc_error_u[i])

            data_jec.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_jec.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], jec_error_l[i], jec_error_u[i])

            data_jer.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_jer.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], jer_error_l[i], jer_error_u[i])

            data_nongaussian.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_nongaussian.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], nongaussian_error_l[i], nongaussian_error_u[i])



        data_tot.Write('data_tot')
        data_stat.Write('data_stat')
        data_syst.Write('data_syst')
        data_lumi.Write('data_lumi')
        data_unc.Write('data_unc')
        data_jec.Write('data_jec')
        data_jer.Write('data_jer')
        data_nongaussian.Write('data_nongaussian')

        print_hepdata_summary(data=data['sigma'], 
                              ystar_l=data['ys_low'], ystar_u=data['ys_high'],
                              yboost_l=data['yb_low'], yboost_u=data['yb_high'],
                              ptavg_l=data['pt_low'], ptavg_u=data['pt_high'],
                              stat_l=stat_error_l, stat_u=stat_error_u,
                              syst_l=syst_error_l, syst_u=syst_error_u,
                              ybys_bin=ybys_bin)


def infinalrange(pt_low, ybys_bin):
    cuts = {
            'yb0ys0' : (74.,1784.),
            'yb0ys1' : (74.,1248.),
            'yb0ys2' : (74.,548.),
            'yb1ys0' : (74.,1032.),
            'yb1ys1' : (74.,686),
            'yb2ys0' : (74.,430.),
            }
    if pt_low >= cuts[ybys_bin][0] and pt_low < cuts[ybys_bin][1]:
        return True
    return False

def print_data(data, labels, ybys_bin):
    # labels = data.keys()
    # labels.sort()
    nbins = len(data[labels[0]])
    for i in xrange(nbins):
        if infinalrange(data['pt_low'][i], ybys_bin):
            vals = ['{0:<15.4g}'.format(data[label][i]) for label in labels]
            print ' '.join(vals)


def print_hepdata_summary(**kwargs):
    # print kwargs.keys()

    header="""
*author: CMS Collaboration
*experiment: CERN-LHC-CMS
*detector: CMS
*title: Measurement of Triple-Differential Dijet Cross Sections at sqrt(s) = 8 TeV with the CMS Detector and Constraints on Parton Distribution Functions
"""
    if kwargs['ybys_bin'] == 'yb0ys0':
        print header

    dataset="""
*dataset:
*dscomment: Triple differential dijet cross section for {ystar_l} <= YSTAR < {ystar_u} and {yboost_l} <= YBOOST < {yboost_u} as function of the average transverse momentum of the leading two jets. 
            The (sys) error is the total relative systematic error, including the luminosity uncertainty of 2.6%.
*reackey: P P --> JET JET
*obskey: D3SIG/DPTAVG/DYSTAR/DYBOOST
*qual: {ystar_l} <= YSTAR < {ystar_u}; {yboost_l} <= YBOOST < {yboost_u}
*qual: RE : P P --> JET JET
*qual: SQRT(S) IN GEV : 8000.0
*yheader: D3(SIG)/DPTAVG/DYSTAR/DYBOOST IN PB/GEV
*xheader: PTAVG IN GEV 
*data: x : y 
""".format(ystar_l=kwargs['ystar_l'][0], ystar_u=kwargs['ystar_u'][0], yboost_l=kwargs['yboost_l'][0], yboost_u=kwargs['yboost_u'][0])
    print dataset
    data ="""
 {ptavg_l} TO {ptavg_u}; {sigma:15.4G} +- {stat:.4G} (DSYS=+{syst_u:.4G},-{syst_l:.4G});"""
    for i in xrange(len(kwargs['data'])):
        if infinalrange(kwargs['ptavg_l'][i], kwargs['ybys_bin']):
            print data.format(ptavg_l=kwargs['ptavg_l'][i], ptavg_u=kwargs['ptavg_u'][i], sigma=kwargs['data'][i],
                              stat=kwargs['stat_l'][i], syst_u=kwargs['syst_u'][i], syst_l=kwargs['syst_l'][i]), 
    footer="""
*dataend:

"""
    print footer


    if kwargs['ybys_bin'] == 'yb2ys0':
        print "*E"


if __name__ == '__main__':
    main()
