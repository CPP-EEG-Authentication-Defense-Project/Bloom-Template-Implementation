# Bloom Template Implementation

This repository contains an implementation of an EEG template generation backend, using [Bloom Filters](https://w.wiki/39oG).

## Development

To set up a development environment for this package, it is recommended to create a virtual environment. See the
[Python documentation](https://docs.python.org/3/library/venv.html) for guidance on how to do that.

Once you have activated the virtual environment, you can then install development dependencies with:

```shell
pip install -r dev-requirements.txt
```

This package uses [PyInvoke](https://github.com/pyinvoke/invoke) to provide simple build/maintenance task running.

### Adding Dependencies

To add dependencies, update the `pyproject.toml` file. Additionally, update the `dev-requirements.txt` file by 
running:

```shell
invoke requirements
```

### Building

To build this package, run the following:

```shell
invoke build
```
