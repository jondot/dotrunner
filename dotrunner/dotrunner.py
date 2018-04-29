# -*- coding: utf-8 -*-

from docopt import docopt
from os.path import join, isdir, basename
import os.path
from toolz.curried import pipe, filter, map, get, concat, mapcat, merge, assoc, first  # noqa
import networkx as nx
import delegator
import yaml
from colorama import Style
from datetime import datetime
from .version import VERSION
from pyspin.spin import make_spin, Default


class FileSystemIO(object):
    def yaml(self, f):
        try:
            with open(f) as fp:
                return yaml.load(fp)
        except:  # noqa
            return None

    @make_spin(Default, '')
    def execute(self, cwd, cmd):
        res = delegator.run(cmd, cwd=cwd)
        if (res.return_code == 0):
            print('✅ {} {} ({})'.format(datetime.today(), cmd, cwd))
            if (res.out):
                print(Style.DIM + res.out.strip() + Style.RESET_ALL)
        else:
            print('❌ {} {} ({})'.format(datetime.today(), cmd, cwd))
            if (res.err):
                print(Style.DIM + res.err.strip() + Style.RESET_ALL)

        return (res.return_code, res.out)

    def ls(self, dir):
        return os.listdir(dir)


class DryRunIO(FileSystemIO):
    def execute(self, cwd, cmd):
        print('(dry) {} {} ({})'.format(datetime.today(), cmd, cwd))


def dirs(dir, io):
    return pipe(io.ls(dir), filter(lambda d: not d.startswith('-')),
                            map(lambda d: join(dir, d)),
                            filter(isdir),
                            list) # noqa yapf: disable


RUNNER_YAML = 'install.yml'


def modulemap(root, io):
    modules = dirs(root, io)
    return pipe(modules, map(lambda m: assoc({}, basename(m), io.yaml(join(m, RUNNER_YAML)))), # noqa
                         filter(lambda m: m[first(m)] is not None),
                         merge) # noqa yapf: disable


PHONY_DEP = ''


def runlist(yamls):
    nodelist = list(
        mapcat(
            lambda f: map(lambda i: (f[0], i), f[1].get('deps', [PHONY_DEP])),
            yamls.items()))
    return pipe(nodelist, nx.DiGraph,
                          nx.topological_sort,
                          list,
                          reversed,
                          filter(lambda r: r != PHONY_DEP),
                          list) # noqa yapf: disable


def run(root, io):
    modules = modulemap(root, io)
    lst = runlist(modules)
    return pipe(lst, map(lambda mod: io.execute(join(root, mod),
                                     modules.get(mod).get('script', './install'))), # noqa
                     list) # noqa


def main():
    doc = """dotrunner
        Usage:
        dotrunner <root> [--dry-run]
        dotrunner --version

        Options:
        -d --dry-run     Perform dry run (don't apply changes to filesystem)
        --version        Show version.
        -h --help        Show this screen.
        """
    args = docopt(doc, version='dotrunner {}'.format(VERSION))
    (root, dry_run) = get(['<root>', '--dry-run'])(args)
    IO = DryRunIO if dry_run else FileSystemIO
    run(root, IO())


if __name__ == '__main__':
    main()
