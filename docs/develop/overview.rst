.. _dev_overview:

Overview
========

Here we describe the development process overview. It's in F.A.Q. format to
make it simple.


Why is ``next`` the default branch?
-----------------------------------

The ``main`` branch is always in a production-ready state. The tip of 
``main`` contains the latest full (ie non-candidate) release. New PRs
should be made into the ``next`` branch to be first release as a *candidate*
and batched with other PRs into the next versioned release.

The ``next`` branch, can potentially break. As a user, you should NEVER use
non-main branches in production (if you're desperate
for a feature or fix not yet released, either use a SHA to install at a
specific commit, or install a release candidate tag).


How to file a ticket?
---------------------

Go to https://github.com/django-guardian/django-guardian/issues and create new
one.


How do I get involved?
----------------------

If you want to fix a bug, extend documentation or whatever you
think is appropriate for the project that involves changes, it's
typically a good idea to raise an issue first, especially if your 
change involves the actual code (eg isn't just a docstring typo or similar!).

Then, fork the project on github (https://github.com/django-guardian/django-guardian),
create a separate branch, work on it, push changes to your fork and create a pull
request.

Here is a quick how to:

1. Fork a project: https://github.com/django-guardian/django-guardian/fork
2. Checkout project to your local machine::

       $ git clone git@github.com:YOUR_NAME/django-guardian.git

3. Create a new branch with name describing change you are going to work on::

       $ git checkout -b support-for-custom-model

4. Perform changes at newly created branch. Remember to include tests (if this
   is code related change) and run test suite. See :ref:`running tests documentation
   <testing>`. Also, remember to add yourself to the bottom of the ``authors`` entry in ``pyproject.toml``.

5. (Optional) Squash commits. If you have multiple commits and it doesn't make
   much sense to have them separated (and it usually makes little sense),
   please consider merging all changes into single commit. Please see
   https://help.github.com/articles/interactive-rebase if you need help with
   that.

6. Publish changes::

        $ git push origin YOUR_BRANCH_NAME

6. Create a `Pull Request <https://help.github.com/articles/creating-a-pull-request>`_.
   Usually it's as simple as opening up https://github.com/YOUR_NAME/django-guardian
   and clicking on review button for newly created branch. There you can make
   final review of your changes and if everything seems fine, create a Pull
   Request.


Why was my issue/pull request closed?
-------------------------------------

We usually put an explanation when we close an issue or PR. Common reasons:
- no reply for over a month after our last comment or review
- no tests for the changes, or failing tests
- there are performance implications of the changes
- PRs made out of the blue without filing an issue first
- breaking changes we don't want to introduce
- out-of-scope features
- features or approaches that are difficult to support going forwards


How do you make a release candidate?
------------------------------------

This workflow may only be triggered by project maintainers.

To make a new *release candidate* you should perform the following steps:

* Be on any branch other than ``main``, typically ``devel``
* Update ``pyproject.toml`` with the new version identifier (see `Semantic Versioning 2.0 <http://semver.org/>`_ )
* Ensure the new identifier ends in ``rc<x>``, eg ``3.0.0rc1``
* Push your changes to GitHub
* Navigate to `the release-publish action <https://github.com/django-guardian/django-guardian/actions/workflows/release-publish.yml>`_ on GitHub
* Run the workflow manually:
  * Use workflow from branch ``devel``.
  * Specify the branch name or commit sha to release
  * Specify the tag to apply, which must match your version identifier (eg ``3.0.0rc1``)
* If it is a breaking release, edit release notes to include an "Upgrade Instructions" section

This will:
* build and upload the package to PyPI using a trusted publisher,
* tag the repo, and
* create a prerelease version in GitHub Releases.



How do you make a full release?
-------------------------------

This workflow may only be triggered by project maintainers.

To make a new full release you should perform the following steps:

* Start on a branch (typically ``devel``) where:
  * the tip is at your latest published release candidate and 
  * the branch is up to date with ``main``
* Update ``pyproject.toml`` to remove the ``rc<x>`` suffix from the version identifier 
* Commit this change and push to GitHub
* Merge to ``main``
* Navigate to `the release-publish action <https://github.com/django-guardian/django-guardian/actions/workflows/release-publish.yml>`_ on GitHub
* Run the workflow manually:
  * Use workflow from branch ``main``.
  * Specify the branch name ``main``
  * Specify the version identifier eg ``3.0.0``
* If it is a breaking release, edit release notes to include an "Upgrade Instructions" section (copy across from the release canditate notes)

This will:
* build and upload the package to PyPI using a trusted publisher,
* tag the repo, and
* create a full release version in GitHub Releases.
