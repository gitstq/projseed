"""Built-in, original meta-file templates for projseed.

Every template string in this module is written from scratch for projseed.
gitignore patterns are short, curated lists covering the most common ignored
paths per ecosystem. License texts are the canonical short-form legal texts
(MIT / ISC / BSD-2-Clause / Apache-2.0) reproduced verbatim, as they are
intended to be copied verbatim into every project.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# .gitignore patterns per ecosystem
# ---------------------------------------------------------------------------
# Each entry is a list of raw gitignore lines. Order matters; negation
# patterns (leading "!") are supported and preserved on merge.

GITIGNORE_GENERAL = [
    "# OS / editor noise",
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    "*.swp",
    "*.swo",
    "*~",
    ".vscode/",
    ".idea/",
]

GITIGNORE_PYTHON = [
    "# Python",
    "__pycache__/",
    "*.py[cod]",
    "*$py.class",
    "*.egg-info/",
    "*.egg",
    ".eggs/",
    "build/",
    "dist/",
    ".venv/",
    "venv/",
    "env/",
    ".pytest_cache/",
    ".coverage",
    ".coverage.*",
    "htmlcov/",
    ".tox/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".hypothesis/",
]

GITIGNORE_NODE = [
    "# Node.js",
    "node_modules/",
    "dist/",
    "build/",
    ".next/",
    ".nuxt/",
    ".cache/",
    ".parcel-cache/",
    ".turbo/",
    "coverage/",
    "npm-debug.log*",
    "yarn-debug.log*",
    "yarn-error.log*",
    "pnpm-debug.log*",
    ".env",
    ".env.local",
    ".env.*.local",
]

GITIGNORE_GO = [
    "# Go",
    "/bin/",
    "/dist/",
    "*.exe",
    "*.exe~",
    "*.test",
    "*.out",
    "vendor/",
    "go.work.sum",
]

GITIGNORE_RUST = [
    "# Rust",
    "/target/",
    "**/*.rs.bk",
    ".cargo/",
]

GITIGNORE_JAVA = [
    "# Java / JVM",
    "target/",
    "build/",
    "out/",
    "*.class",
    "*.jar",
    "*.war",
    "*.ear",
    ".gradle/",
    ".idea/",
    "*.iml",
    ".classpath",
    ".project",
    ".settings/",
]

GITIGNORE_DOCKER = [
    "# Docker / compose local state",
    ".docker-env/",
    "docker-compose.override.yml",
]

# Registry: name -> patterns
GITIGNORE_PRESETS = {
    "general": GITIGNORE_GENERAL,
    "python": GITIGNORE_PYTHON,
    "node": GITIGNORE_NODE,
    "go": GITIGNORE_GO,
    "rust": GITIGNORE_RUST,
    "java": GITIGNORE_JAVA,
    "docker": GITIGNORE_DOCKER,
}

# ---------------------------------------------------------------------------
# LICENSE templates (canonical short texts)
# ---------------------------------------------------------------------------

def _mit_text(holder: str, year: int) -> str:
    return (
        "MIT License\n\n"
        f"Copyright (c) {year} {holder}\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE.\n"
    )


def _isc_text(holder: str, year: int) -> str:
    return (
        "ISC License\n\n"
        f"Copyright (c) {year} {holder}\n\n"
        "Permission to use, copy, modify, and/or distribute this software for any\n"
        "purpose with or without fee is hereby granted, provided that the above\n"
        "copyright notice and this permission notice appear in all copies.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\" AND THE AUTHOR DISCLAIMS ALL WARRANTIES\n"
        "WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF\n"
        "MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR\n"
        "ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES\n"
        "WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN\n"
        "ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF\n"
        "OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.\n"
    )


def _bsd2_text(holder: str, year: int) -> str:
    return (
        "BSD 2-Clause License\n\n"
        f"Copyright (c) {year} {holder}\n\n"
        "Redistribution and use in source and binary forms, with or without\n"
        "modification, are permitted provided that the following conditions are met:\n\n"
        "1. Redistributions of source code must retain the above copyright notice, this\n"
        "   list of conditions and the following disclaimer.\n\n"
        "2. Redistributions in binary form must reproduce the above copyright notice,\n"
        "   this list of conditions and the following disclaimer in the documentation\n"
        "   and/or other materials provided with the distribution.\n\n"
        "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\"\n"
        "AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\n"
        "IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"
        "DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE\n"
        "FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\n"
        "DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR\n"
        "SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER\n"
        "CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,\n"
        "OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\n"
        "OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n"
    )


def _apache_text(holder: str, year: int) -> str:
    # Apache License 2.0, canonical text with the appendix copyright notice filled in.
    apache_body = (
"                                 Apache License\n"
"                           Version 2.0, January 2004\n"
"                        http://www.apache.org/licenses/\n\n"
"   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION\n\n"
"   1. Definitions.\n\n"
"      \"License\" shall mean the terms and conditions for use, reproduction,\n"
"      and distribution as defined by Sections 1 through 9 of this document.\n\n"
"      \"Licensor\" shall mean the copyright owner or entity authorized by\n"
"      the copyright owner that is granting the License.\n\n"
"      \"Legal Entity\" shall mean the union of the acting entity and all\n"
"      other entities that control, are controlled by, or are under common\n"
"      control with that entity. For the purposes of this definition,\n"
"      \"control\" means (i) the power, direct or indirect, to cause the\n"
"      direction or management of such entity, whether by contract or\n"
"      otherwise, or (ii) ownership of fifty percent (50%) or more of the\n"
"      outstanding shares, or (iii) beneficial ownership of such entity.\n\n"
"      \"You\" (or \"Your\") shall mean an individual or Legal Entity\n"
"      exercising permissions granted by this License.\n\n"
"      \"Source\" form shall mean the preferred form for making modifications,\n"
"      including but not limited to software source code, documentation source,\n"
"      and configuration files.\n\n"
"      \"Object\" form shall mean any form resulting from mechanical\n"
"      transformation or translation of a Source form, including but\n"
"      not limited to compiled object code, generated documentation,\n"
"      and conversions to other media types.\n\n"
"      \"Work\" shall mean the work of authorship, whether in Source or\n"
"      Object form, made available under the License, as indicated by a\n"
"      copyright notice that is included in or attached to the work.\n\n"
"      \"Derivative Works\" shall mean any work, whether in Source or Object\n"
"      form, that is based on (or derived from) the Work and for which the\n"
"      editorial revisions, annotations, elaborations, or other modifications\n"
"      represent, as a whole, an original work of authorship. For the purposes\n"
"      of this License, Derivative Works shall not include works that remain\n"
"      separable from, or merely link (or bind by name) to the interfaces of,\n"
"      the Work and Derivative Works thereof.\n\n"
"      \"Contribution\" shall mean any work of authorship, including\n"
"      the original version of the Work and any modifications or additions\n"
"      to that Work or Derivative Works thereof, that is intentionally\n"
"      submitted to Licensor for inclusion in the Work by the copyright owner\n"
"      or by an individual or Legal Entity authorized to submit on behalf of\n"
"      the copyright owner. For the purposes of this definition, \"submitted\"\n"
"      means any form of electronic, verbal, or written communication sent\n"
"      to the Licensor or its representatives, including but not limited to\n"
"      communication on electronic mailing lists, source code control systems,\n"
"      and issue tracking systems that are managed by, or on behalf of, the\n"
"      Licensor for the purpose of discussing and improving the Work, but\n"
"      excluding communication that is conspicuously marked or otherwise\n"
"      designated in writing by the copyright owner as \"Not a Contribution.\"\n\n"
"      \"Contributor\" shall mean Licensor and any individual or Legal Entity\n"
"      on behalf of whom a Contribution has been received by Licensor and\n"
"      subsequently incorporated within the Work.\n\n"
"   2. Grant of Copyright License. Subject to the terms and conditions of\n"
"      this License, each Contributor hereby grants to You a perpetual,\n"
"      worldwide, non-exclusive, no-charge, royalty-free, irrevocable\n"
"      copyright license to reproduce, prepare Derivative Works of,\n"
"      publicly display, publicly perform, sublicense, and distribute the\n"
"      Work and such Derivative Works in Source or Object form.\n\n"
"   3. Grant of Patent License. Subject to the terms and conditions of\n"
"      this License, each Contributor hereby grants to You a perpetual,\n"
"      worldwide, non-exclusive, no-charge, royalty-free, irrevocable\n"
"      (except as stated in this section) patent license to make, have made,\n"
"      use, offer to sell, sell, import, and otherwise transfer the Work,\n"
"      where such license applies only to those patent claims licensable\n"
"      by such Contributor that are necessarily infringed by their\n"
"      Contribution(s) alone or by combination of their Contribution(s)\n"
"      with the Work to which such Contribution(s) was submitted. If You\n"
"      institute patent litigation against any entity (including a\n"
"      cross-claim or counterclaim in a lawsuit) alleging that the Work\n"
"      or a Contribution incorporated within the Work constitutes direct\n"
"      or contributory patent infringement, then any patent licenses\n"
"      granted to You under this License for that Work shall terminate\n"
"      as of the date such litigation is filed.\n\n"
"   4. Redistribution. You may reproduce and distribute copies of the\n"
"      Work or Derivative Works thereof in any medium, with or without\n"
"      modifications, and in Source or Object form, provided that You\n"
"      meet the following conditions:\n\n"
"      (a) You must give any other recipients of the Work or Derivative\n"
"          Works a copy of this License; and\n\n"
"      (b) You must cause any modified files to carry prominent notices\n"
"          stating that You changed the files; and\n\n"
"      (c) You must retain, in the Source form of any Derivative Works\n"
"          that You distribute, all copyright, patent, trademark, and\n"
"          attribution notices from the Source form of the Work, excluding\n"
"          those notices that do not pertain to any part of the Derivative\n"
"          Works; and\n\n"
"      (d) If the Work includes a \"NOTICE\" text file as part of its\n"
"          distribution, then any Derivative Works that You distribute must\n"
"          include a readable copy of the attribution notices contained\n"
"          within such NOTICE file, excluding those notices that do not\n"
"          pertain to any part of the Derivative Works, in at least one\n"
"          of the following places: within a NOTICE text file distributed\n"
"          as part of the Derivative Works; within the Source form or\n"
"          documentation, if provided along with the Derivative Works; or,\n"
"          within a display generated by the Derivative Works, if and\n"
"          wherever such third-party notices normally appear. The contents\n"
"          of the NOTICE file are for informational purposes only and\n"
"          do not modify the License. You may add Your own attribution\n"
"          notices within Derivative Works that You distribute, alongside\n"
"          or as an addendum to the NOTICE text from the Work, provided\n"
"          that such additional attribution notices cannot be construed\n"
"          as modifying the License.\n\n"
"      You may add Your own copyright statement to Your modifications and\n"
"      may provide additional or different license terms and conditions\n"
"      for use, reproduction, or distribution of Your modifications, or\n"
"      for any such Derivative Works as a whole, provided Your use,\n"
"      reproduction, and distribution of the Work otherwise complies with\n"
"      the conditions stated in this License.\n\n"
"   5. Submission of Contributions. Unless You explicitly state otherwise,\n"
"      any Contribution intentionally submitted for inclusion in the Work\n"
"      by You to the Licensor shall be under the terms and conditions of\n"
"      this License, without any additional terms or conditions.\n"
"      Notwithstanding the above, nothing herein shall supersede or modify\n"
"      the terms of any separate license agreement you may have executed\n"
"      with Licensor regarding such Contributions.\n\n"
"   6. Trademarks. This License does not grant permission to use the trade\n"
"      names, trademarks, service marks, or product names of the Licensor,\n"
"      except as required for reasonable and customary use in describing the\n"
"      origin of the Work and reproducing the content of the NOTICE file.\n\n"
"   7. Disclaimer of Warranty. Unless required by applicable law or agreed to\n"
"      in writing, Licensor provides the Work (and each Contributor provides\n"
"      its Contributions) on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS\n"
"      OF ANY KIND, either express or implied, including, without limitation,\n"
"      any warranties or conditions of TITLE, NON-INFRINGEMENT,\n"
"      MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely\n"
"      responsible for determining the appropriateness of using or\n"
"      redistributing the Work and assume any risks associated with Your\n"
"      exercise of permissions under this License.\n\n"
"   8. Limitation of Liability. In no event and under no legal theory,\n"
"      whether in tort (including negligence), contract, or otherwise,\n"
"      unless required by applicable law (such as deliberate and grossly\n"
"      negligent acts) or agreed to in writing, shall any Contributor be\n"
"      liable to You for damages, including any direct, indirect, special,\n"
"      incidental, or consequential damages of any character arising as a\n"
"      result of this License or out of the use or inability to use the\n"
"      Work (including but not limited to damages for loss of goodwill,\n"
"      work stoppage, computer failure or malfunction, or any and all\n"
"      other commercial damages or losses), even if such Contributor\n"
"      has been advised of the possibility of such damages.\n\n"
"   9. Accepting Warranty or Additional Liability. While redistributing\n"
"      the Work or Derivative Works thereof, You may choose to offer,\n"
"      and charge a fee for, acceptance of support, warranty, indemnity,\n"
"      or other liability obligations and/or rights consistent with this\n"
"      License. However, in accepting such obligations, You may act only\n"
"      on Your own behalf and on Your sole responsibility, not on behalf\n"
"      of any other Contributor, and only if You agree to indemnify,\n"
"      defend, and hold each Contributor harmless for any liability\n"
"      incurred by, or claims asserted against, such Contributor by reason\n"
"      of your accepting any such warranty or additional liability.\n\n"
"   END OF TERMS AND CONDITIONS\n\n"
"   APPENDIX: How to apply the Apache License to your work.\n\n"
"      To apply the Apache License to your work, attach the following\n"
"      boilerplate notice, with the fields enclosed by brackets \"[]\"\n"
"      replaced with your own identifying information. (Don't include\n"
"      the brackets!)  The text should be enclosed in the appropriate\n"
"      comment syntax for the file format. We also recommend that a\n"
"      file or class name and description of purpose be included on the\n"
"      same \"printed page\" as the copyright notice for easier\n"
"      identification within third-party archives.\n\n"
)
    appendix = (
        f"   Copyright {year} {holder}\n\n"
        "   Licensed under the Apache License, Version 2.0 (the \"License\");\n"
        "   you may not use this file except in compliance with the License.\n"
        "   You may obtain a copy of the License at\n\n"
        "       http://www.apache.org/licenses/LICENSE-2.0\n\n"
        "   Unless required by applicable law or agreed to in writing, software\n"
        "   distributed under the License is distributed on an \"AS IS\" BASIS,\n"
        "   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
        "   See the License for the specific language governing permissions and\n"
        "   limitations under the License.\n"
    )
    return apache_body + appendix


LICENSE_BUILDERS = {
    "mit": _mit_text,
    "isc": _isc_text,
    "bsd-2": _bsd2_text,
    "apache-2.0": _apache_text,
}

# ---------------------------------------------------------------------------
# Other meta-file templates
# ---------------------------------------------------------------------------

def readme_skeleton(project_name: str, holder: str, year: int) -> str:
    return f"""# {project_name}

> One-line description of what {project_name} does.

## Features

- Feature one
- Feature two
- Feature three

## Install

```sh
# TODO: install instructions
```

## Usage

```sh
# TODO: minimal usage
```

## Development

```sh
# TODO: setup / test commands
```

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.
Copyright (c) {year} {holder}.
"""


EDITORCONFIG = """# https://editorconfig.org
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{md,markdown}]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
"""


def contributing_skeleton(project_name: str) -> str:
    return f"""# Contributing to {project_name}

Thanks for taking the time to contribute! This is a quick guide to get you
set up.

## Getting started

1. Fork the repository and clone your fork.
2. Create a topic branch: `git checkout -b my-change`.
3. Make your change and add or update tests.
4. Run the local test suite before opening a PR.
5. Open a pull request against `main`.

## Commit messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/)
style: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.

## Pull requests

- Keep PRs focused and small.
- Describe what changed and why.
- Make sure CI (if configured) passes.

## Reporting bugs

Open an issue and include: what you expected, what happened, steps to
reproduce, and your OS / runtime version.
"""


def changelog_skeleton(holder: str, year: int) -> str:
    return f"""# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Project scaffold created by projseed.

### Changed
-

### Fixed
-

[Unreleased]: https://example.com/commits/Unreleased

<!--
Copyright (c) {year} {holder}.
Edit the compare links above to point at your own repository once it exists.
-->
"""


BUG_REPORT_YML = """---
name: Bug report
about: Report something that is not working as expected
title: "[Bug]: "
labels: ["bug"]
---

## What happened

A clear and concise description of the bug.

## Expected behavior

What you expected to happen.

## To reproduce

Steps to reproduce the behavior:
1.
2.
3.

## Environment

- OS:
- Runtime / language version:
- Project version:

## Additional context

Logs, screenshots, or anything else that helps.
"""


FEATURE_REQUEST_YML = """---
name: Feature request
about: Suggest an idea or improvement
title: "[Feature]: "
labels: ["enhancement"]
---

## Problem

What problem are you trying to solve?

## Proposed solution

A clear and concise description of what you want to happen.

## Alternatives considered

Any alternative solutions or features you've considered.

## Additional context

Anything else that helps.
"""


PR_TEMPLATE = """## What does this PR do?

A clear and concise description of what this PR changes.

## Why?

Why is this change needed? Link to an issue if there is one.

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Refactor
- [ ] Documentation
- [ ] Other (describe below)

## How has this been tested?

Describe how you tested this change.

## Checklist

- [ ] I have read the contributing guide.
- [ ] I have added or updated tests where appropriate.
- [ ] The docs reflect the change.
"""
