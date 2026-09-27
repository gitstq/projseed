# Contributing to projseed

Thanks for taking the time to contribute! projseed is a small,
zero-dependency Python CLI, so contributing is meant to be quick.

## Getting started

1. Fork and clone the repository.
2. Make sure you are on Python 3.9 or newer (`python3 --version`).
3. There is no install step for local development — the package is pure
   standard library. You can run it directly:

   ```sh
   python3 -m projseed --help
   ```

4. Run the test suite before opening a PR:

   ```sh
   python3 -m unittest -v
   ```

## Commit messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):
`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.

## Pull requests

- Keep PRs focused and small.
- Add or update tests for any behavioural change.
- Make sure `python3 -m unittest -v` passes.
- Do not add third-party runtime dependencies — projseed deliberately stays
  on the standard library. If you think you need one, open an issue first.

## Reporting bugs

Open an issue and include: what you expected, what happened, the exact
command you ran, your OS and Python version.
