import logging
import numpy as np

from src.modules.base_module import BaseModule
from helpers import divide_tgraph, isfloat
import ROOT

log = logging.getLogger(__name__)


class Ratio(BaseModule):
    """Calculates ratios of objects. without taking into account any error propagation. If you need an
       proper error propagation use the Divide module.
    """

    def __init__(self):
        super(Ratio, self).__init__()
        self.parser.add_argument('--ratio', nargs='+', default=[], type='str2kvstr',
                                 help='List of id:to_id objects for which the ratio is calculated.')

    def __call__(self, config):
        for id, to in config['ratio']:
            log.debug('Calculating ratio of {0} to {1}'.format(id, to))
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if to not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(to))

            # ratio_to_obj(config['objects'][id]['obj'], config['objects'][to]['obj'])
            obj = config['objects'][id]['obj']
            to_obj = config['objects'][to]['obj']
            if isinstance(obj, ROOT.TH1) and isinstance(to_obj, ROOT.TH1):
                if not (obj.GetNbinsX() == to_obj.GetNbinsX()):
                    raise ValueError('The two histograms have different numbers of bins.')
                for i in xrange(1, obj.GetNbinsX() + 1):
                    obj.SetBinContent(i, obj.GetBinContent(i) / obj.GetBinContent(i))
                    obj.SetBinError(i, obj.GetBinError(i) / obj.GetBinContent(i))
            elif isinstance(obj, ROOT.TGraph) and isinstance(to_obj, ROOT.TGraph):
                divide_tgraph(obj, to_obj, error_prop=False)
            elif isinstance(obj, ROOT.TH1) and isinstance(to_obj, ROOT.TGraph):
                obj = ROOT.TGraphAsymmErrors(obj)
                divide_tgraph(obj, to_obj, error_prop=False)
                config['objects'][id]['obj'] = obj
            else:
                raise TypeError('Invalid types passed: {0} and {1}'.format(type(obj), type(to_obj)))


class Normalize(BaseModule):
    """Normalize an obj by binwidth, to unity, to integral of another id or by a float."""

    def __init__(self):
        super(Normalize, self).__init__()
        self.parser.add_argument('--normalize', nargs='+', default=[], type='str2kvstr',
                                 help='Normalize an id to bin widths, unity, to the integral of another object or by a float using width/unity/obj_id or a float.')

    def __call__(self, config):
        for id, val in config['normalize']:
            log.debug('Normalizing id {0} using {1}.'.format(id, val))
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if val == 'width':
                # Normalize to bin width
                config['objects'][id]['obj'].Scale(1.0, 'width')
            elif val == 'unity':
                # Normalize to Unity
                config['objects'][id]['obj'].Scale(1.0 / config['objects'][id]['obj'].Integral())
            elif val in config['objects']:
                # Normalize to another object
                config['objects'][id]['obj'].Scale(1.0 / config['objects'][val]['obj'].Integral())
            elif isfloat(val):
                # Normalize/Scale by an factor
                config['objects'][id]['obj'].Scale(float(val))
            else:
                raise ValueError('There intended normalization could not be identified for {0}'.format(val))


class NormalizeToGen(BaseModule):
    """Normalizes a given TH2 to the sum in a row (y axis), e.g. to the number of true events."""

    def __init__(self):
        super(NormalizeToGen, self).__init__()
        self.parser.add_argument('--normalize-to-gen', nargs='+', default=[], type=str,
                                 help='Id of 2d histograms which will be row-normalized.')

    def __call__(self, config):
        for id in config['normalize_to_gen']:
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            obj = config['objects'][id]['obj']

            for y in xrange(1, obj.GetNbinsY() + 1):
                y_sow = np.sum([obj.GetBinContent(x, y) for x in xrange(1, obj.GetNbinsX() + 1)])
                for x in xrange(1, obj.GetNbinsX() + 1):
                    obj.SetBinContent(x, y, obj.GetBinContent(x, y) / y_sow)
                    obj.SetBinError(x, y, obj.GetBinError(x, y) / y_sow)

