![](https://github.com/khanrc/sconf/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/khanrc/sconf/branch/master/graph/badge.svg)](https://codecov.io/gh/khanrc/sconf)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sconf)
![PyPI](https://img.shields.io/pypi/v/sconf?color=blue)

# sconf: Simple config system supporting CLI modification

sconf is yaml-based simple config library.


## Features

- Supports merging multiple configs
- Supports CLI modification by argparse-like interface
- Supports coloring modified key-values
- Supports global access to config objects


## Install

```
$ pip install sconf
```

## Usage

### Quickstart

#### A Minimal Example

```py
from sconf import Config

cfg = Config(default="configs/defaults.yaml")
cfg.argv_update()  # apply CLI modification
```

You can modify `cfg` by CLI in the runtime, by argparse-like interface.

#### Init with argparse and multiple configs

```py
import argparse
from sconf import Config

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("config_paths", nargs="*")
parser.add_argument("--show", action="store_true", default=False)
args, left_argv = parser.parse_known_args()

# merging multiple configs if given
cfg = Config(*args.config_paths, default="configs/defaults.yaml")
cfg.argv_update(left_argv)
```

Run:

```
python train.py example configs/exp.yaml --lr 0.1
```

The resulting `cfg` is based on `configs/defaults.yaml`, merged with `configs/exp.yaml`, and updated by `--lr 0.1`.

### Dumps

sconf dumps contents with coloring modified items.

```py
print(cfg.dumps())

# If you do not want to colorize:
print(cfg.dumps(modified_color=None))
```

### Access

- Item access with dictionary-like interfaces:

```py
# access
print(cfg['key'])
print(cfg['key1']['key2'])

# get
print(cfg.get('non-key', 'default-value'))

# unpacking
function(**cfg['model'])
```

- Attribute access:

```py
print(cfg.key)
print(cfg.key1.key2)
```

- **Note** that the attribute access returns method object for the duplicated key, unlike the item access.

```py
cfg = Config({'get': 2})

print(cfg['get'])  # 2
print(cfg.get)  # method object
```


### CLI modification

sconf supports CLI modification like argparse. Also you can access to the child key using dot.

```
# yaml example
batch_size: 64
model:
    encoder:
        n_channels: 64
    decoder:
        n_channels: 64
```

- CLI modification:

```
> python train.py --batch_size 128 --model.encoder.n_channels 32
```

- Accessing via partial key is also available:

```
> python train.py --encoder.n_channels 32
```

- Use triple dashs `---` if you want to modify multiple keys:

```
# modifying encoder.n_channels and decoder.n_channels both.
> python train.py ---n_channels 32
```


### Global access to config object

Global access is useful in ML project, even though it can be anti-pattern in SW engineering.

```py
# main.py
cfg = Config({'weight_decay': 0.001})  # first config is automatically registered to 'default' key

# train.py
cfg = Config.get_default()  # get 'default' config
print(cfg.weight_decay)  # 0.001
```

Note `from_registry` helps global access to multiple configs.


## Note

- sconf use utf-8 as a default encoding. If you want different encoding, use file pointer (`open` function) instead of file path as a key.
