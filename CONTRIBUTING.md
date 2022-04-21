# Contributing Guide

- Contributing to this framework is straight forward. This document shows you how to get started

## Submitting changes

- Fork the repo
  - <https://github.com/Base4Security/T3SF/fork>
- Check out a new branch based and name it to what you intend to do:
  - Example:
    ````
    $ git checkout -b BRANCH_NAME
    ````
    If you get an error, you may need to fetch main first by using
    ````
    $ git remote update && git fetch
    ````
  - Use one branch per fix / feature
- Commit your changes
  - Please provide a git message that explains what you've done
  - Commit to the forked repository
  - Example:
    ````
    $ git commit -am 'Adding Signal support'
    ````
- Push to the branch
  - Example:
    ````
    $ git push origin BRANCH_NAME
    ````
- Make a pull request
  - Make sure you send the PR to the <code>main</code> branch

If you follow these instructions, your PR will land pretty safely in the main repo!
