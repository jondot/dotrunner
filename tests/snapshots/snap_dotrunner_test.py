# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_modulemap 1'] = {
    'asdf': {
        'deps': [
            'brew'
        ],
        'script': 'echo asdf'
    },
    'brew': {
        'script': 'echo brew'
    },
    'osx': {
        'script': 'install.sh'
    },
    'python': {
        'deps': [
            'asdf'
        ],
        'script': 'echo hello'
    }
}

snapshots['test_dirs 1'] = [
    '/fixtures/demo-system/asdf',
    '/fixtures/demo-system/osx',
    '/fixtures/demo-system/python',
    '/fixtures/demo-system/brew'
]
