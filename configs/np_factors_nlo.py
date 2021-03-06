
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
        config['ana_modules'] = ["Divide", "FitObj", "BuildTGraph", "RootOutputModule"]

        config["build_tgraph"] = [
                            ("res_np_factor", ("_fit_graph_origbin_hw7_mpihad", "_fit_graph_origbin_pwgp8_m1_mpihad"))
                                ]
        config["fit_obj"] = [
                        ("hw7_mpihad", {
                                "fcn": "[0]/x**[1] + 1.0", 
                                "fcn_0": [118, 1.58, 1.0], 
                                "options": "I"
                            }
                        ),
                        ("pwgp8_s1_mpihad", {
                                "fcn": "[0]/x**[1] + [2]", 
                                "fcn_0": [1.0, 1.0, 1.0], 
                                "options": "I"
                            }
                        ),
                        ("pwgp8_m1_mpihad", {
                                "fcn": "[0]/x**[1] + [2]", 
                                "fcn_0": [1.0, 1.0, 1.0], 
                                "options": "I"
                            }
                        ),
                    ]

        config["divide"] = [
                           ["hw7_mpihad", "hw7_nompinohad"], 
                           ["pwgp8_s1_mpihad", "pwgp8_nompinohad"], 
                           ["pwgp8_m1_mpihad", "pwgp8_nompinohad"], 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config['plot_order'] = []
        config['plot_id'] = ['fit_hw7_mpihad', 'hw7_mpihad','fit_pwgp8_s1_mpihad', 'pwgp8_s1_mpihad','fit_pwgp8_m1_mpihad', 'pwgp8_m1_mpihad', 'res_np_factor']

        config['objects']["res_np_factor"] = {
            "label": "NPcorr.",
            "color": "black",
            "zorder": 2.5
        } 
        config['objects']["hw7_mpihad"] = {
            "input": "~/dust/HW7/RIVET_11.root?{0}_xs".format(rap_bin), 
            "label": "Herwig 7",
            "color": "_color0_",
        } 

        config['objects']["hw7_nompinohad"] = {
            "input": "~/dust/HW7/RIVET_11_NOMPINOHAD.root?{0}_xs".format(rap_bin)
        }
        config['objects']["pwgp8_s1_mpihad"] = {
            "input": "/nfs/dust/cms/user/gsieber/POWHEG/RIVET3/POWHEG_MPIHAD.root?{0}_xs".format(rap_bin), 
            "color": "_color2_"
        } 
        config['objects']["pwgp8_m1_mpihad"] = {
            "input": "/nfs/dust/cms/user/gsieber/POWHEG/RIVET_8CUEP8M1/POWHEG_MPIHAD_8CUEP8M1.root?{0}_xs".format(rap_bin), 
            "color": "_color3_"
        } 
        config['objects']["pwgp8_nompinohad"] = {
            "input": "/nfs/dust/cms/user/gsieber/POWHEG/RIVET3/POWHEG_NOMPINOHAD.root?{0}_xs".format(rap_bin)
        }
        config['objects']["fit_hw7_mpihad"] = {
            "label": "Herwig 7",
            "style": "line",
            "color": "_color0_"
        } 
        config['objects']["fit_pwgp8_s1_mpihad"] = {
            "label": "Powheg+P8 8CUEP8S1",
            "style": "line",
            "color": "_color2_"
        } 
        config['objects']["fit_pwgp8_m1_mpihad"] = {
            "label": "Powheg+P8 8CUEP8M1",
            "style": "line",
            "color": "_color3_"
        } 

        config["y_lims"] = ["0.88", "1.4"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "NP Correction"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin),
                             ] 

        config["output_path"] = 'np_factors_nlo_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

