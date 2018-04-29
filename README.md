# dotrunner

Use [`dotrunner`](https://github.com/jondot/dotrunner) and [`dotlinker`](https://github.com/jondot/dotlinker) to build a fantastically aesthetic macOS dotfiles set up.

✅ Organize by topics (folder modules), i.e. 'nodejs', 'osx', and 'python'.  
✅ DAG (Directed Acyclic Graph) based runner for a powerful dependency system.  
✅ No shell scripts, gunk, yuck, and hairballs required

Here's an example dotfiles repo:

```
~/.dotfiles
    asdf/
    brew/
      install.yml
      Brewfile
    python/
    osx/
    nodejs/
      .npmrc.symlink
      install.yml
    fonts/
```

And here's an example `install.yml` taken from the `nodejs` module:

```yaml
script: npm i -g yarn
deps:
- asdf
```

## Quick Start

Note: check out the [example](example/) if you'd like to test this all out on a Docker container instance.

Install:

```
$ pip install dotrunner dotlinker
```

Dry run:

```
$ dotrunner ~/.dotfiles --dry-run
```

And finally, apply (this will obviously change your system!):

```
$ dotrunner ~/.dotfiles
```

## Building a Dotfiles System with dotrunner

This layout describes a system that installs apps (with `homebrew`), development tools (with `asdf`), nodejs tools (with `install.sh`) and some system defaults (with `set-defaults.sh`):

```
asdf/         <----- a 'module'
  install.yml <----- a module install file. required.
  Asdffile
brew/
  install.yml
  Brewfile
nodejs/
  .npmrc.symlink   <--- this is handled by dotlinker, see
                        https://github.com/jondot/dotlinker
  install.yml
  install.sh
osx/
  install.yml
  set-defaults.sh
```

This system follows a few simple principles:

* Every directory is a _module_ if it has an `install.yml` file and it doesn't start with a dash (-).
* Each module can describe `deps` (dependencies) and a `script` to run.
* Each module actions must be idempotent: running the same script multiple times will have the same result. In other words `dotrunner` will happily run your scripts again on reruns/failures and you're responsible to do validation/checks in your scripts.

Here are a few examples of an `install.yml` file:

No dependencies:

```yaml
script: sh ./install.sh
```

Has depdendencies but no `script`, it will use `./install` script by default.

```yaml
deps:
- brew
- osx
```

Has both dependencies and a `script` which points to an executable script:

```yaml
script: ./install.sh
deps:
- brew
- osx
```

# Contributing

Fork, implement, add tests, pull request, get my everlasting thanks and a respectable place here :).

### Thanks:

To all [Contributors](https://github.com/jondot/dotrunner/graphs/contributors) - you make this happen, thanks!

# Copyright

Copyright (c) 2018 [Dotan Nahum](http://gplus.to/dotan) [@jondot](http://twitter.com/jondot). See [LICENSE](LICENSE.txt) for further details.
