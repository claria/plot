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
        config['ana_modules'] = ["Ratio", "MinusOne"]
        config["ratio"] = [
                           ["dataunf_lumi", "dataunf_stat"], 
                           ["dataunf_total", "dataunf_total"], 
                           ["dataunf_uncor", "dataunf_stat"], 
                           ["dataunf_jec", "dataunf_stat"], 
                           ["dataunf_jer", "dataunf_stat"], 
                           ["dataunf_nongaussian", "dataunf_stat"], 
                           ["dataunf_stat", "dataunf_stat"], 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]

        config['plot_order'] = ['dataunf_stat', 'dataunf_jec', 'dataunf_uncor', 'dataunf_jer', 'dataunf_lumi', 'dataunf_nongaussian']
        config['minusone'] = ['dataunf_stat', 'dataunf_jec', 'dataunf_uncor', 'dataunf_jer', 'dataunf_nongaussian', 'dataunf_lumi', 'dataunf_total']

        config['objects']["dataunf_stat"] = {
            "color": "black", 
            "edgecolor": "black", 
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_stat".format(rap_bin), 
            "label": "Stat. uncertainty", 
            "marker": ".", 
            "step": False, 
            "zorder": 2.0,
        }
        config['objects']["dataunf_lumi"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_lumi".format(rap_bin), 
            "label": "Lumi uncertainty", 
            "style": "errorlines",
            "color": "_color2_",
            "dashes": [4,4,10,4],
            "step": True,
        }
        config['objects']["dataunf_jec"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_jec".format(rap_bin), 
            "label": "JEC uncertainty", 
            "style": "errorlines",
            "color": "_color0_",
            "dashes": [20,4],
            "step": True,
        }
        config['objects']["dataunf_jer"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_jer".format(rap_bin), 
            "label": "JER uncertainty", 
            "style": "errorlines",
            "color": "_color3_",
            "linestyle": "--",
            "step": True,
        }

        config['objects']["dataunf_nongaussian"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_nongaussian".format(rap_bin), 
            "label": "Non-Gaussian tails unc.", 
            "style": "errorlines",
            "color": "_color5_",
            "linestyle": "-",
            "step": True,
        }


        config['objects']["dataunf_uncor"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_unc".format(rap_bin), 
            "label": "Uncorrelated unc.", 
            "style": "errorlines",
            "color": "_color1_",
            "step": True,
        }
        config['objects']["dataunf_total"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_tot".format(rap_bin), 
            "label": "Total uncertainty", 
            "style": "errorlines",
            "color": "black",
            "step": True,
        }

        config["y_lims"] = ["-0.30", "0.30"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'lower left'
        config["legend_ncol"] = 2
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Relative uncertainty?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_|size=32'.format(rap_bin), 
                              {'s': ur'CMS' , 'x': 0.55, 'y': 0.95, 'ha': 'center', 'va': 'top', 'size': 40, 'weight': 'bold'}, 
                              # {'s': ur'Preliminary' , 'x': 0.555, 'y': 0.875, 'ha': 'center', 'va': 'top', 'size': 18, 'style':'italic'}, 

                              '_20fb_'] 

        config["output_path"] = 'exp_unc_overview_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 22
    kwargs['mpl'].rcParams['legend.columnspacing'] = 1
    kwargs['mpl'].rcParams['lines.linewidth'] = 4
