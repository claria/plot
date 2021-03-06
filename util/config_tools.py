import collections
import copy
import json
import os
import sys
import logging

log = logging.getLogger(__name__)

class ConfigDict(dict):
    """ It is a normal dict, just a few convenience methods added.
    """
    def __init__(self, *args, **kwargs):
        super(ConfigDict, self).__init__(*args, **kwargs)
        self.setdefault('objects', {})

    def add_object(self, name):
        if '_default' in self['objects']:
            self['objects'][name] = copy.deepcopy(self['objects']['_default'])
        else:
            self['objects'][name] = {}


def parse_optionstring(s):
    """Splits the string at last occurence of '?' and tries to parse everything
       after it into a dict.
    """
    try:
        label, kwargs = s.rsplit('?', 1)
    except ValueError as e:
        log.debug('Could not split {0}'.format(s))
        log.debug(e)
        return s, {}
    if kwargs:
        try:
            kwargs = json.loads(kwargs, object_pairs_hook=collections.OrderedDict)
        except ValueError as e:
            log.debug('Failed parsing {0}.'.format(kwargs))
            log.debug(e)
            return s, {}
    return label, kwargs


def merge(a, b, precedence_keys=None, merge_keys=None):
    """Merges b into a, but only if key of b is not in a. If key of b in list precedence_keys,
       then the value of b overrides the value of a. If key of b in list merge_keys, arguments of
       a and b are merged by adding list arguments. This only works for lists."""
    if precedence_keys is None:
        precedence_keys = []
    if merge_keys is None:
        merge_keys = []
    for key in b:
        if key in a:
            if isinstance(a[key], collections.Mapping) and isinstance(b[key], collections.Mapping):
                merge(a[key], b[key], precedence_keys=precedence_keys)
            elif a[key] == b[key]:
                pass  # same leaf value
            elif key in merge_keys:
                try:
                    a[key] = a[key] + b[key]
                except TypeError:
                    log.error('Both arguments have to be of list type to be able to merge them.')
                    sys.exit(1)
            elif key in precedence_keys:
                a[key] = b[key]
            else:
                pass
        else:
            a[key] = b[key]
    return a


def read_config(path):
    """Read json config from file into an OrderedDict structure. This is not valid JSON standard
       but comes in very handy."""
    with open(path) as json_file:
        try:
            config = json.load(json_file, object_pairs_hook=collections.OrderedDict)
        except ValueError as e:
            log.critical('Failed to parse json file {0}. Error message is \n{1}'.format(path, e))
            sys.exit(1)
    return config


class SimpleJsonEncoder(json.JSONEncoder):
    """JSON Encoder which replaces not serializiable objects like root objects with null."""

    def default(self, obj):
        if not isinstance(obj, (dict, list, tuple, str, unicode, int, long, float, bool)):
            return 'null'
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def write_config(config, path, indent=4):
    """Save json config to file."""

    # Create output directory if not existing
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    # Write config.
    with open(path, "w") as f:
        json.dump(config, f, skipkeys=True, indent=indent, separators=(',', ': '), cls=SimpleJsonEncoder)

    # log.debug("Config written to \"{0}\"".format(path))
    log.info('Config written to \"{0}\"'.format(path))


def print_config(config):
    """ Print the config to the screen."""
    print json.dumps(config, cls=SimpleJsonEncoder, separators=(',', ': '), indent=4)


def walk_dic(node, func):
    """Walks a dic containing dicts, lists or str and calls func(key, val) on each str leaf."""
    seq_iter = node.keys() if isinstance(node, dict) else xrange(len(node))
    for k in seq_iter:
        if isinstance(node[k], basestring):
            node[k] = func(node[k])
        elif isinstance(node[k], dict) or isinstance(node[k], list):
            walk_dic(node[k], func)

def relpath_replace(s):
    """Checks if s is a path to an existing file and replaces relative paths or symlinks by the real path."""
    def replace_path(path):
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        if os.path.isfile(path.encode('utf8')):
            return os.path.realpath(path.encode('utf8'))
        else:
            return path
    s = s.split('?')
    s = [replace_path(s) for s in s]
    return '?'.join(s)

