---
name: charmkeeperration-tests
description: Use this skill when you need to write, update, migrate or fix integration tests.
---

Plan:

- Find the integration tests in the repository (their could be multiple "tests/integration" folders).
- Ensure each set of integration tests is following the implementation standards.
- Run the tests to ensure the code work as expected.

# Implementation standards

- Expected versions:

  - `jubilant`: ~> 1.7

- Lint produced code with `tox -e lint`.

# Testing

## Writing integrations tests

- Integration test must be implemented with `jubilant`:

  - See [How to migrate from pytest-operator to Jubilant](https://documentation.ubuntu.com/jubilant/how-to/migrate-from-pytest-operator/) if the charm is currently using pytest-operator.


- For each charm in the repository, there should be a `tests/` folder like: https://github.com/canonical/platform-engineering-charm-template/tree/main/tests

  - There is a `tests/conftest.py` file to add options to pytest. See an example here: https://github.com/canonical/haproxy-operator/blob/main/haproxy-spoe-auth-operator/tests/conftest.py
  - Integration tests goes in `tests/integration`
  - There is a `tests/integration/conftest.py` file with the same fixtures as: https://raw.githubusercontent.com/canonical/platform-engineering-charm-template/refs/heads/main/tests/integration/conftest.py
  - Fixtures should look like the ones in https://raw.githubusercontent.com/canonical/netbox-k8s-operator/refs/heads/main/tests/integration/conftest.py
  - Helper functions should go in `tests/integration/helpers.py`. See an example here: https://raw.githubusercontent.com/canonical/netbox-k8s-operator/refs/heads/main/tests/integration/helpers.py
  - There is a `tests/integration/test_charm.py` to test the basic behaviors of the charm.
  - There should be additional `tests/integration/test_xxx.py` files to test specific integrations of the charm.

- If the repository contains multiple charms, there should be a `tests/integration` at the root of the repository. You can find an example here: https://github.com/canonical/haproxy-operator/tree/main/tests


- Dependencies

  - The charms used in the integration tests should be deployed using the `latest/edge` channel (or "*track*/edge").
  - An explicit revision should be set to deploy the charm.
  - Revisions are defined through constants defined at the beginning of the file.
  - Each constant is preceded with a '# renovate: depName="xxx"' directive to let renovate detect and update the revision.
  
## Local testing

The integration tests should be run in a virtual machine named "charmkeeper".

If the machine doesn't exist, create it with: `scripts/create-charmkeeper-vm.sh`.

If not already done, mount the working directory folder in the machine with

```bash
multipass mount --type native $PWD charmkeeper:/workdir
```

Look at CONTRIBUTING.md to see if there are specific instructions to build and test the charm.

Don't forget to rebuild the charm (and the rock) if you change the code.

Unless there is something specific mentioned, you should be able to run the unit tests with: `multipass exec charmkeeper -d /workdir/ -- tox`

Then run the integration tests with `multipass exec charmkeeper -d /workdir/ -- tox -e integration -- --charm-file=path-to-charm`.

# Maintain

## Configuring renovate

Configure renovate with a charmhub customDatasource like in https://raw.githubusercontent.com/canonical/platform-engineering-charm-template/refs/heads/main/renovate.json to

- Add a regex customManager to update the revisions
- Set ignorePath to an empty array to not exclude the `tests` folders
