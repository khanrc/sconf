![](https://github.com/khanrc/sconf/workflows/build/badge.svg)

# sconf: Simple config supporting CLI modification

sconf is yaml-based simple config library.


## Features

- Supports merging multiple configs
- Supports CLI modification
- Supports coloring modified key-values


## Install

```
$ pip install git+https://github.com/khanrc/sconf
```

## Usage

### Initialize

#### Basic init

```py
from sconf import Config

cfg = Config(default="configs/defaults.yaml")
cfg.argv_update()  # apply CLI modification
```


#### Init with argparse and multiple configs

```py
import sys
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


### Dumps

sconf has two dumping methods, `dumps` and `yaml`. `dumps` return colorized contents for modified items without comments and `yaml` return contents and comments without coloring.

```py
# dump with coloring modified items
print(cfg.dumps())

# dump with comments
print(cfg.yaml())
```

### Access

sconf has same interface with dictionary:

```py
# access
print(cfg['key'])
print(cfg['key1']['key2'])

# get
print(cfg.get('non-key', 'default-value'))

# unpacking
function(**cfg['model'])
```

### CLI modification

sconf supports CLI modification like argparse. Also you can access to the child key using dot.

```
# configs/defaults.yaml
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
