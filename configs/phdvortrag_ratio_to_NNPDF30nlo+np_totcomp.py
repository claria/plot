import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    configs = []
    for rap_bin in rap_bins:
        config = get_base_config()
        config['ana_modules'] = ["Normalize", "ReBinning", "Multiply", "Ratio", "ToTGraph"]
        # config["normalize"] = [("dataunf", "width")]

        config['quadratic_sum'] = [
                                ('theounc', ('nlonnpdf30_scale', 'nlonnpdf30')),
                                 ]
        config["normalize"] = []
        config["multiply"] = [
                              ("nloct14", "_np"), 
                              ("nlommht2014", "_np"), 
                              ("abm11nlo", "_np"), 
                              ("nlonnpdf30", "_np")] 
        config["ratio"] = [
                           ["dataunf_stat", "nlonnpdf30"], 
                           ["dataunf_syst", "nlonnpdf30"], 
                           ["nlommht2014", "nlonnpdf30"], 
                           ["abm11nlo", "nlonnpdf30"], 
                           ["nloct14", "nlonnpdf30"],
                           ["nlonnpdf30", "nlonnpdf30"],
                           ["nlonnpdf30_scale", "nlonnpdf30_scale"] 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config["to_tgraph"] = ["nlonnpdf30", 
                               "nlommht2014", 
                               "abm11nlo", 
                               "nloct14"] 
        config['plot_order'] = ['dataunf_stat', 'dataunf_syst', 'nlonnpdf30','nlonnpdf30_scale']
        config['plot_id'] = ['dataunf_stat', 
                             'dataunf_syst', 
                             '^nlonnpdf30$',
                             # 'nlonnpdf30_scale', 
                             # "nlommht2014", 
                             # "abm11nlo", 
                             # "nloct14"
                             ]


        config['objects']["_np"] = {
            "input": "~/dust/dijetana/plot/np_factors.root?{0}/res_np_factor".format(rap_bin)
        } 
        config['objects']["dataunf_stat"] = {
            "color": "black", 
            "edgecolor": "black", 
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_stat".format(rap_bin), 
            "label": "Data", 
            "marker": ".", 
            "step": False, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 4.0
        }
        config['objects']["dataunf_syst"] = {
            "color": "_color4_", 
            "edgecolor": "_color4_", 
            "linewidth":2.0,
            "edgealpha":1.0,
            "alpha": 0.1,
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_syst".format(rap_bin), 
            "label": "Syst. Unc.", 
            "marker": ".", 
            "step": True, 
            "style": "band", 
            "hatch": '//',
            "rasterized": False,
            "x_err": True, 
            "y_err": True, 
            "zorder": 2.0
        }

        config['objects']["nlonnpdf30"] = {
            "alpha": 0.3, 
            "color": "_color0_", 
            "edgecolor": "_color0_", 
            "input_tgraph": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_xs&~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_pdfunc_l&~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_pdfunc_u".format(rap_bin), 
            "label": "PDF Unc.", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "band", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config['objects']["nlonnpdf30_scale"] = {
            "alpha": 1.0, 
            "color": "_color3_", 
            "edgecolor": "_color3_", 
            "input_tgraph": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_xs&~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_scunc_l&~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_scunc_u".format(rap_bin), 
            "label": "Scale Unc.", 
            "linestyle": "--", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "errorlines", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        } 
        config['objects']["nlommht2014"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "#15b01a", 
            "edgecolor": "#15b01a", 
            "id": "nlommht2014", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/MMHT2014_xs".format(rap_bin), 
            "label": "MMHT 2014 - NLO$\otimes$NP", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        } 
        config['objects']["nloct14"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "#ff000d", 
            "edgecolor": "#ff000d", 
            "id": "nlonnpdf30", 
            "input_tgraph": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/CT14nlo_xs".format(rap_bin), 
            "label": "CT14 - NLO$\otimes$NP", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["abm11nlo"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "_color5_", 
            "edgecolor": "_color5_", 
            "id": "nlonnpdf30", 
            "input_tgraph": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/ABM11NLO_xs".format(rap_bin), 
            "label": "NLO$\otimes$NP (ABM11)", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }

        config["y_lims"] = ["0.4", "1.6"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config['x_axis_formatter'] = 'scalar2'
        config["x_log"] =  True
        config["legend_loc"] = 'upper left'
        config["legend_ncol"] = 1
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Ratio to Theory?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperright_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'phdvortrag_ratio_to_NNPDF30+np_totcomp_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 20
    kwargs['mpl'].rcParams['lines.linewidth'] = 4
    # kwargs['mpl'].rcParams['font.size'] = 20
