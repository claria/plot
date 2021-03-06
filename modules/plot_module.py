import itertools
import re
import collections
from collections import OrderedDict

import matplotlib

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from util.plot_tools import BasePlot
import util.callbacks as callbacks

BasePlot.init_matplotlib()

from util import plot_tools
from util.plot_tools import plot_errorbar, plot_band, plot_line, plot_errorlines, plot_histo, plot_heatmap
from util.plot_tools import log_locator_filter
from modules.base_module import BaseModule

import logging

from src.lookup_dict import get_lookup_val
from util.config_tools import parse_optionstring
from util.setting_parser import parse_query

log = logging.getLogger(__name__)


class PlotModule(BaseModule):
    """Plotting output module for 1d and 2d plots using the matplotlib library. 

       All objects plotted are read from the 'objects' dict in the configs. You can
       use all the id based settings to manipulate the appearance of the objects and the
       standard arguments to adapt the axis and figure.
    """

    def __init__(self):
        super(PlotModule, self).__init__()
        # Plot object options
        # TODO: Split into arg groups for setting based arguments and standard arguments.
        self.arg_group.add_argument('--label', type='str2kvstr', nargs='+', default='__nolegend__', action='setting',
                                    help='Legend labels for each plot')
        self.arg_group.add_argument('--color', type='str2kvstr', nargs='+',
                                    default='auto', action='setting',
                                    help='Colors for each plot.')
        self.arg_group.add_argument('--edgecolor', type='str2kvstr', nargs='+',
                                    default='auto', action='setting',
                                    help='Edgecolor for each plot.')
        self.arg_group.add_argument('--cmap', type='str2kvstr', nargs='+',
                                    default='viridis', action='setting',
                                    help='Colormap used for heatmaps.')
        self.arg_group.add_argument('--hatch', type='str2kvstr', nargs='+',
                                    default=None, action='setting',
                                    help='Hatch for each plot')
        self.arg_group.add_argument('--fill', type='str2kvbool', nargs='+',
                                    default=True, action='setting',
                                    help='Hatch for each plot')
        self.arg_group.add_argument('--rasterized', type='str2kvbool', nargs='+',
                                    default=True, action='setting',
                                    help='Hatch for each plot')
        self.arg_group.add_argument('--linestyle', type='str2kvstr', nargs='+',
                                    default='', action='setting',
                                    help='Linestyle for each plot')
        self.arg_group.add_argument('--linewidth', type='str2kvfloat', nargs='+',
                                    default=None, action='setting',
                                    help='Linewidth for each plot')
        self.arg_group.add_argument('--dashes', type='str2kvfloat', nargs='+',
                                    default=None, action='setting',
                                    help='Dashes for each plot')
        self.arg_group.add_argument('--marker', type='str2kvstr', nargs='+',
                                    default='.', action='setting',
                                    help='Marker for errorbars for each plot.')
        self.arg_group.add_argument('--plot-datavals', type='str2kvbool', nargs='+',
                                    default=False, action='setting',
                                    help='Marker for errorbars for each plot.')
        self.arg_group.add_argument('--x-err', type='str2kvbool', nargs='+', default=True, action='setting',
                                    help='Show x-errors.')
        self.arg_group.add_argument('--y-err', type='str2kvbool', nargs='+', default=True, action='setting',
                                    help='Show y-errors.')
        self.arg_group.add_argument('--alpha', type='str2kvfloat', nargs='+', default=1.0, action='setting',
                                    help='Alpha value in plot.')
        self.arg_group.add_argument('--edgealpha', type='str2kvfloat', nargs='+', default=1.0, action='setting',
                                    help='Alpha value of Edgecolor in plot.')
        self.arg_group.add_argument('--capsize', type='str2kvint', nargs='+', default=0, action='setting',
                                    help='Capsize of errorbars in plot.')
        self.arg_group.add_argument('--zorder', type='str2kvfloat', nargs='+', default=1.0, action='setting',
                                    help='Alpha value in plot.')
        self.arg_group.add_argument('--mask-value', type='str2kvfloat', nargs='+', default=None, action='setting',
                                    help='Mask value equal to setting.')
        self.arg_group.add_argument('--style', default='errorbar', type='str2kvstr', nargs='+', action='setting',
                                    help='Style of the plotted object.')
        self.arg_group.add_argument('--step', type='str2kvbool', nargs='+', default=False, action='setting',
                                    help='Plot the data stepped at the xerr edges.')
        self.arg_group.add_argument('--axis', type='str2kvstr', nargs='+', default='ax', action='setting',
                                    help='Plot the object in the following axis.')

        # Figure options
        self.arg_group.add_argument('--fig-size', type=float, nargs=2, default=None, help='Size of figure.')

        # Axis options
        self.arg_group.add_argument('--add-subplot', default=False, type='bool', help='Add subplot with name ax1.')
        self.arg_group.add_argument('--x-lims', nargs=2, default=[None, None],
                                    help='X limits of plot. \'none\' can be passed as xmin or xmax '
                                         'resulting in auto scaling.')
        self.arg_group.add_argument('--y-lims', nargs=2, default=[None, None],
                                    help='Y limits of plot. \'none\' can be passed as ymin or ymax '
                                         'resulting in auto scaling.')
        self.arg_group.add_argument('--y-subplot-lims', nargs=2, default=[None, None],
                                    help='Y limits of plot. \'none\' can be passed as ymin or ymax '
                                         'resulting in auto scaling.')
        self.arg_group.add_argument('--z-lims', nargs=2, default=[None, None],
                                    help='Z limits of plot (only used in 2d plots).')

        self.arg_group.add_argument('--x-log', default=False, type='bool', help='Use log scale for x-axis.')
        self.arg_group.add_argument('--y-log', default=False, type='bool', help='Use log scale for y-axis.')
        self.arg_group.add_argument('--z-log', default=False, type='bool', help='Use log scale for z-axis.')

        self.arg_group.add_argument('--x-axis-formatter', default='scalar2', help='Formatter for x-axis.')
        self.arg_group.add_argument('--y-axis-formatter', default='scientific', help='Formatter for y-axis.')
        self.arg_group.add_argument('--z-axis-formatter', default='scientific', help='Formatter for z-axis.')

        self.arg_group.add_argument('--x-label', default='', help='Label of the x axis.')
        self.arg_group.add_argument('--y-label', default='', help='Label of the y axis.')
        self.arg_group.add_argument('--y-subplot-label', default='', help='Label of the y subplot axis.')
        self.arg_group.add_argument('--z-label', default='', help='Label of the z axis.')

        self.arg_group.add_argument('--margin', type=float, default=0.0, help='Relative margin between datalims and axis lims.')

        self.arg_group.add_argument('--show-legend', type='bool', default=True, help='Plot a legend on axis ax.')
        self.arg_group.add_argument('--legend-ncol', type=int, default=1, help='Number of columns in legend.')
        self.arg_group.add_argument('--combine-legend-entries', type='str2kvstr', nargs='+', default=[],
                                    help='Combines multiple legend entries into one if possible.')
        self.arg_group.add_argument('--legend-loc', default='best', help='Location of legend on axis ax.')

        self.arg_group.add_argument('--plot-id', default=[r'^(?!_).*'], nargs='+',
                                    help='All ids matching are passed to plot-module.'
                                         ' Default matches everything not starting with a underscore.')
        self.arg_group.add_argument('--plot-order', default=[], nargs='+',
                                    help='Processes ids in the given order, i.e. to order the legend.')

        self.arg_group.add_argument('--ax-texts', nargs='+', default=[],
                                    help='Add text to plot. Syntax is \'Text?json_dict. The options have to be '
                                         'something like \'text?{"x": 0.95, "y":0.05, "va": "bottom", "ha" : "right"}\'')
        self.arg_group.add_argument('--ax-vlines', nargs='+', default=[],
                                    help='Add vertical lines to plot. Syntax is y=1.0?lw=2.0?color=green. All matplotlib '
                                         'Line2D kwargs are valid.')
        self.arg_group.add_argument('--ax-hlines', nargs='+', default=[], type='str2dict',
                                    help='Add horizontal lines to plot. Syntax is y=1.0?lw=2.0?color=green. All matplotlib '
                                         'Line2D kwargs are valid.')


    def __call__(self, config):
        plot = Plot(**config)

        callbacks.trigger('before_plot', plt=plt, mpl=matplotlib)

        # plot each object
        id_regex = config.get('plot_id', '')
        if isinstance(id_regex, basestring) or not isinstance(id_regex, collections.Iterable):
            id_regex = [id_regex]
        items = ([(x, config['objects'][x]) for x in config.get('plot_order', []) if x in config['objects'].keys()] + 
                [(x, config['objects'][x]) for x in config['objects'].keys() if x not in config.get('plot_order', [])])
        for id, item in items:
            item['id'] = id
            if item.get('no_plot', False):
                log.debug('Omitting id {0} since no_plot setting was set.'.format(id))
                continue
            if not any([re.match(regex, id) for regex in id_regex]):
                log.debug('Omitting id {0} since it does not match the regex.'.format(id))
                continue
            if not item.get('obj', None):
                log.warning('Not obj found for id {0}. Skipping this id.'.format(id))
                continue
            log.info('Drawing id {0}'.format(id))
            artist = plot.plot(**item)

        # Save plot
        plot.finish()


def get_plot(*args, **kwargs):
    return Plot(*args, **kwargs)


class Plot(BasePlot):
    def __init__(self, histos=None, **kwargs):

        super(Plot, self).__init__(**kwargs)
        if not kwargs['add_subplot']:
            self.ax = self.fig.add_subplot(111)
            self.ax1 = None
        else:
            self.ax = plt.subplot2grid((4, 1), (0, 0), rowspan=3)
            self.ax1 = plt.subplot2grid((4, 1), (3, 0), rowspan=1)
        self.histos = histos

        self.x_lims = [get_lookup_val('x_lims', val) for val in kwargs.pop('x_lims', [None, None])]
        self.x_lims = [any2float(v) for v in self.x_lims]
        self.y_lims = [get_lookup_val('y_lims', val) for val in kwargs.pop('y_lims', [None, None])]
        self.y_lims = [any2float(v) for v in self.y_lims]
        self.y_subplot_lims = kwargs.pop('y_subplot_lims', (None, None))
        self.y_subplot_lims = [any2float(v) for v in self.y_subplot_lims]
        self.z_lims = kwargs.pop('z_lims', (None, None))
        self.z_lims = [any2float(v) for v in self.z_lims]

        self.margin = kwargs.pop('margin', 0.1)


        self.x_log = kwargs.pop('x_log', False)
        self.y_log = kwargs.pop('y_log', False)
        self.z_log = kwargs.pop('z_log', False)

        self.x_axis_formatter = kwargs.pop('x_axis_formatter', 'scalar')
        self.y_axis_formatter = kwargs.pop('y_axis_formatter', 'scalar')
        self.z_axis_formatter = kwargs.pop('z_axis_formatter', 'scalar')

        self.x_label = get_lookup_val('x_label', kwargs.pop('x_label', ''))
        self.y_label = get_lookup_val('y_label', kwargs.pop('y_label', ''))
        self.y_subplot_label = get_lookup_val('y_label', kwargs.pop('y_subplot_label', ''))
        self.z_label = get_lookup_val('z_label', kwargs.pop('z_label', ''))

        self.show_legend = kwargs.pop('show_legend', True)
        self.combine_legend_entries = kwargs.pop('combine_legend_entries', [])
        self.legend_loc = kwargs.pop('legend_loc', 'best')
        self.legend_ncol = kwargs.pop('legend_ncol', 1)
        self.legend_bbox_anchor = kwargs.pop('legend_bbox_anchor', None)

        self.texts = kwargs.pop('ax_texts', [])
        self.vlines = kwargs.pop('ax_vlines', [])
        self.hlines = kwargs.pop('ax_hlines', [])

        self.auto_colors = itertools.cycle(matplotlib.rcParams['axes.color_cycle'])

        self.colorbar_mappable = None

        # helpers for legend labels/artists
        self._ids = []
        self._legend_handles = []
        self._legend_labels = []


    def plot(self, **kwargs):
        style = kwargs.pop('style', 'errorbar')
        kwargs['label'] = get_lookup_val('label', kwargs.get('label'))
        # Plot object on this axis
        axis_name = kwargs.pop('axis', 'ax')
        try:
            ax = getattr(self, axis_name)
        except AttributeError as e:
            log.critical('The axis name {0} does not exist.'.format(axis_name))
            log.critical(e)
            raise

        if kwargs['color'] == 'auto':
            kwargs['color'] = next(self.auto_colors)
        if kwargs['edgecolor'] == 'auto':
            kwargs['edgecolor'] = kwargs['color']

        kwargs['color'] = get_lookup_val('color', kwargs.get('color'))
        # Facecolor is always set using the color argument.
        kwargs['facecolor'] = kwargs['color']

        kwargs['edgecolor'] = get_lookup_val('color', kwargs.get('edgecolor'))
        if style == 'errorbar':
            artist = plot_errorbar(ax=ax, **kwargs)
        elif style == 'band':
            artist = plot_band(ax=ax, **kwargs)
        elif style == 'histo':
            artist = plot_histo(ax=ax, **kwargs)
        elif style == 'line':
            artist = plot_line(ax=ax, **kwargs)
        elif style == 'errorlines':
            artist = plot_errorlines(ax=ax, **kwargs)
        elif style == 'heatmap':
            # special case for z scale and lims in heatmaps since they have to be set by the object instead of the axis.
            kwargs['z_log'] = self.z_log
            kwargs['z_lims'] = self.z_lims
            artist = plot_heatmap(ax=self.ax, **kwargs)
            self.colorbar_mappable = artist
        else:
            raise ValueError('Style {0} not supported.'.format(style))

        self._ids.append(kwargs['id'])
        self._legend_handles.append(artist)
        self._legend_labels.append(kwargs['label'])

        return artist

    def finish(self):

        # Add colorbar if there is a mappable
        if self.colorbar_mappable:
            cb = self.fig.colorbar(self.colorbar_mappable, ax=self.ax)
            cb.ax.minorticks_on()
            cb.solids.set_rasterized(True)
            if self.z_label:
                cb.set_label(self.z_label)

        # Add axis texts
        for text in self.texts:
            text = get_lookup_val('ax_texts', text)
            default_text_kwargs = {'x': 0.05, 'y': 0.95, 'va': 'top', 'ha': 'left'}
            text_kwargs = parse_query(text)
            default_text_kwargs.update(text_kwargs)
            ax_name = default_text_kwargs.pop('axis', 'ax')

            s = default_text_kwargs.pop('s')
            r = re.compile(r'\$([^$]*)\$')
            s = r.sub(lambda m: m.group().replace('.', '.\!'), s)
            try:
                cax = getattr(self, ax_name)
            except AttributeError as e:
                log.critical('The axis name {0} does not exist.'.format(ax_name))
                log.critical(e)
                raise
            cax.text(s=s, transform=cax.transAxes, **default_text_kwargs)

        # Add horizontal lines to ax
        for hline_kwargs in self.hlines:
            ax_name = hline_kwargs.pop('axis', 'ax')
            try:
                cax = getattr(self, ax_name)
            except AttributeError as e:
                log.critical('The axis name {0} does not exist.'.format(ax_name))
                log.critical(e)
                raise
            cax.axhline(**hline_kwargs)

        # Add vertical lines to ax
        for vline_kwargs in self.vlines:
            ax_name = vline_kwargs.pop('axis', 'ax')
            try:
                cax = getattr(self, ax_name)
            except AttributeError as e:
                log.critical('The axis name {0} does not exist.'.format(ax_name))
                log.critical(e)
                raise
            cax.axvline(**vline_kwargs)

        # a specified position of the label can be set via label?json_dict
        x_label_kwargs = {'position': (1.0, 0.0), 'ha': 'right', 'va': 'top'}
        x_label, user_x_label_kwargs = parse_optionstring(self.x_label)
        x_label_kwargs.update(user_x_label_kwargs)
        if self.ax1:
            self.ax1.set_xlabel(x_label, **x_label_kwargs)
        else:
            self.ax.set_xlabel(x_label, **x_label_kwargs)

        y_label_kwargs = {'position': (0.0, 1.0), 'ha': 'right', 'va': 'bottom'}
        y_label, user_y_label_kwargs = parse_optionstring(self.y_label)
        y_label_kwargs.update(user_y_label_kwargs)
        self.ax.set_ylabel(y_label, **y_label_kwargs)

        if self.ax1:
            y_subplot_label, y_subplot_label_kwargs = parse_optionstring(self.y_subplot_label)
            self.ax1.set_ylabel(y_subplot_label, **y_subplot_label_kwargs)

        if self.x_log:
            self.ax.set_xscale('log')

            if self.x_axis_formatter == 'scalar':
                xfmt = ScalarFormatter()
                self.ax.xaxis.set_major_formatter(xfmt)
            elif self.x_axis_formatter == 'scalar2':
                xfmt = ScalarFormatter()
                self.ax.xaxis.set_minor_formatter(plt.FuncFormatter(log_locator_filter))
                self.ax.xaxis.set_major_formatter(xfmt)
            if self.ax1:
                self.ax1.set_xscale('log')
                if self.x_axis_formatter == 'scalar':
                    xfmt = ScalarFormatter()
                    self.ax1.xaxis.set_major_formatter(xfmt)
                elif self.x_axis_formatter == 'scalar2':
                    xfmt = ScalarFormatter()
                    self.ax1.xaxis.set_minor_formatter(plt.FuncFormatter(log_locator_filter))
                    self.ax1.xaxis.set_major_formatter(xfmt)

        else:
            self.ax.set_xscale('linear')


        if self.y_log:
            self.ax.set_yscale('log', nonposy='clip')
            if self.y_axis_formatter == 'scalar':
                xfmt = ScalarFormatter()
                self.ax.yaxis.set_major_formatter(xfmt)
            elif self.y_axis_formatter == 'scalar2':
                xfmt = ScalarFormatter()
                self.ax.yaxis.set_major_formatter(xfmt)
                self.ax.yaxis.set_minor_formatter(plt.FuncFormatter(log_locator_filter))
        else:
            self.ax.set_yscale('linear')
       
        # By default set a 10% margin
        plot_tools.set_margin(margin=self.margin)

        self.ax.set_ylim(ymin=self.y_lims[0], ymax=self.y_lims[1])
        self.ax.set_xlim(xmin=self.x_lims[0], xmax=self.x_lims[1])

        if self.show_legend:
            # handles, labels = self.ax.get_legend_handles_labels()
            no_legend_ids = ['nolegend', '_nolegend_', '__nolegend__','none', '']

            # handles = self._legend_handles
            # labels = self._legend_labels
            # TODO combine legend entries
            for id, id2 in self.combine_legend_entries:
                log.debug('Combining legend entries {0} and {1}'.format(id, id2))
                if id in self._ids and id2 in self._ids:
                    self._legend_handles[self._ids.index(id)] = (self._legend_handles[self._ids.index(id2)],self._legend_handles[self._ids.index(id)]) 
            leg_entry_dict = OrderedDict(zip(self._legend_labels, self._legend_handles))
            for key in leg_entry_dict.keys():
                if key.lower() in no_legend_ids:
                    del leg_entry_dict[key]

            if leg_entry_dict:
                labels, handles = zip(*leg_entry_dict.items())
                if 'outside' in self.legend_loc:
                    if self.legend_bbox_anchor:
                        bbox_to_anchor = self.legend_bbox_anchor
                    else:
                        bbox_to_anchor = (1, 1)

                    self.legend_loc = self.legend_loc.replace('outside', '').strip()
                else:
                    bbox_to_anchor = None
                legend = self.ax.legend(handles, labels, loc=self.legend_loc, ncol=self.legend_ncol, bbox_to_anchor=bbox_to_anchor)
                legend.get_frame().set_alpha(0.0)

                # [obj.set_rasterized(True) for obj in legend.get_patches()]
                # for obj in legend.get_patches():
                    # obj.set_rasterized(True)

                # legend.draw()
                # self.ax.legend_ = None
                # self.ax.add_artist(legend)
            else:
                log.debug('Omit legend since all labels are empty.')

        if self.ax1:
            self.ax1.set_ylim(ymin=self.y_subplot_lims[0], ymax=self.y_subplot_lims[1])
            plt.setp(self.ax.get_xticklabels(), visible=False)
            plt.setp(self.ax.get_xticklabels(minor=True), visible=False)
            # self.ax1.set_xscale(self.ax.get_xscale())
            self.ax1.set_xlim(self.ax.get_xlim())
            plt.subplots_adjust(hspace=0.15)

        callbacks.trigger('after_plot', plt=self)

        self.save_fig()
        plt.close(self.fig)


def str2bool(v):
    """ Parse string content to bool."""
    return v.lower() in ("yes", "true", "t", "1")


def any2float(v):
    """Return float if parseable, else None."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None
