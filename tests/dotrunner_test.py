from dotrunner.dotrunner import dirs, \
                      FileSystemIO, runlist, modulemap, run
from os.path import realpath, dirname, join


class FakeIO(FileSystemIO):
    def execute(self, cwd, cmd):
        return join(cwd, cmd)


def fixture(p):
    return realpath(join(dirname(__file__), 'fixtures', p))


def sanitize(ps):
    return list(
        map(lambda p: str(p).replace(realpath(dirname(__file__)), ''), ps))


def test_modulemap(snapshot):
    snapshot.assert_match(modulemap(fixture('demo-system'), FileSystemIO()))


def test_runlist():
    deps_with_phony = {
        'asdf': {
            'deps': ['brew'],
        },
        'brew': {
            'deps': ['osx'],
        },
        'osx': {},
        'python': {
            'deps': ['asdf', 'brew'],
        }
    }

    assert runlist(deps_with_phony) == ['osx', 'brew', 'asdf', 'python']

    deps_all = {
        'asdf': {
            'deps': ['brew'],
        },
        'brew': {
            'deps': ['osx'],
        },
        'osx': {
            'deps': ['foo-bar']
        },
        'python': {
            'deps': ['asdf', 'brew'],
        }
    }
    assert runlist(deps_all) == ['foo-bar', 'osx', 'brew', 'asdf', 'python']

    no_deps = {'foo': {}, 'bar': {}}

    assert runlist(no_deps) == ['foo', 'bar']


def test_dirs(snapshot):
    snapshot.assert_match(
        sorted(sanitize(dirs(fixture('demo-system'), FileSystemIO()))))


def test_run(snapshot):
    snapshot.assert_match(
        sorted(sanitize(run(fixture('demo-system'), FakeIO()))))
