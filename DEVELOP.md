# Deploy

You should deploy sconf manually, using `deploy.sh`. Steps:

1. Update version in `setup.py`
2. Push commits to github repository
3. Deploy sconf using `deploy.sh`
4. Check [pypi](https://pypi.org/project/sconf/) and github repository and make sure it is updated.

pypi version info in README will be updated automatically.


# Test with coverage

```py
python -m pytest --cov=./sconf/ ./tests/ --cov-report term-missing
```
