# Carta Mayor Prototype
An attempt on a prototype of a simple terminal-based version of the great card game Carta Mayor.

---
## Local
For a local version of the application, follow:

### Repo and Dependencies
```bash
# create dir
# eclone repo
# go to dev branch
# start virtualenv
# install dependencies
# set env vars
```

### Execution
```bash
# run the thing
```

If you'd like to see the logs during the execution, use the following in a new terminal:
```bash
tail -f logs/info.log       # -f provides live feed of the file
tail -fn 20 logs/debug.log  # -n sets the amount of lines to show
```

### Unit Tests
The application is tested using `pytest` and the tests are all grouped under the [tests](/tests/) directory.

In order to execute the available tests, use the following (from the root directory of the project):
```bash
python -m pytest tests/                                         # executes all available tests
python -m pytest tests/test_card.py                             # executes the tests in 'test_card.py'
python -m pytest tests/test_card.py::test_card_playability      # executes only 'test_card_playability' from 'test_card.py'
```

---
# Commits
When committing to this repository, following convention is advised:

* chore: regular maintenance unrelated to source code (dependencies, config, etc)
* docs: updates to any documentation
* feat: new features
* fix: bug fixes
* ref: refactored code (no new feature or bug fix)
* revert: reverts on previous commits
* test: updates to tests

For further reference on writing good commit messages, see [Conventional Commits](www.conventionalcommits.org).
