# package_dags
Simple python script to package airflow DAGs into a zip file


# Installation

```shell
python -m pip install --upgrade pip
python -m pip install .
```

# Release

## dependencies

```shell
python -m pip install build
```

Also, the [github cli](https://github.com/cli/cli)

1. Commit the changes
2. Bump the version in pyproject.toml
3. Commit that
4. Tag the branch (`git tag -m <version> <version>`)
5. build the release `python -m pip build .`
6. Make the release on github `gh release create --generate-notes <version> dist/package_dags-<version>*`
