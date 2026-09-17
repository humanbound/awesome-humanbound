# Contributing

Everything in this list has to be real, current, and worth a stranger's time. Adding an agent
example has a higher bar than that, and it is written down below.

Contributions are made by pull request against `README.md`. Sign your commits off with
`git commit -s`. This project takes the [Developer Certificate of Origin](https://developercertificate.org/),
matching upstream Humanbound, rather than a CLA.

## The Example Contract

The Agent Examples section exists so that someone can clone a repo, start an agent, and have `hb`
attacking it inside ten minutes. A repository qualifies for that section when all seven of these
hold.

**1. It is public and carries an OSI license.**
No license means nobody can safely copy from it, which defeats the purpose of an example.

**2. The agent exposes an HTTP endpoint that takes a prompt and returns JSON.**
The reply must sit under one of the keys the engine extracts automatically: `content`, `text`,
`response`, `answer`, `message`, `reply`, or `output`. Anything else and `hb` will connect but read
nothing back.

**3. It ships a `bot-config.json`.**

```json
{
  "chat_completion": {
    "endpoint": "http://127.0.0.1:8000/chat",
    "headers": { "Content-Type": "application/json" },
    "payload": { "message": "$PROMPT", "history": "$CONVERSATION" }
  }
}
```

`headers` is required even when empty. Omit the key and you get a bare `KeyError` instead of a
useful error. Include `$CONVERSATION` unless you have a reason not to: without it the agent can only
be driven single-turn, and the multi-turn orchestrators are where the interesting failures are.

**4. It ships a `scope.yaml`** with `business_scope`, `permitted`, and `restricted`. This is what
turns a generic attack into a relevant one. `restricted` is the list the judge grades against, so a
vague scope produces a vague report.

**5. It contains no real secrets.** Not in `scope.yaml`, not in the system prompt, not in a
committed `.env`. Use obviously fake values. An example that leaks a live key during a published
attack run is a liability, not a demo.

**6. The README documents install, run, and the exact `hb test` command**, copy-pasteable, including
which extras to install and which environment variables are needed.

**7. The README records a real run.** Posture score, letter grade, orchestrator, target model, and
the date you ran it. For example:

> Verified: F 27.38/100, 61 of 97 turns failed, `owasp_agentic`, target `gpt-4o-mini`, 2026-09-10.

This is the requirement that matters most, and the one most likely to be skipped. Without it there
is no way to tell a working example from a plausible-looking one that has never been executed, and a
list of untested stubs is worse than an empty list. Scores drift as models change, so a stale
number with an honest date is fine. A missing number is not.

## Adding an example to this list

Once the repository meets the contract, open a pull request adding one line to the appropriate
framework subsection of `README.md`:

```markdown
- [repo-name](https://github.com/owner/repo) - Framework and shape, one clause. What it demonstrates, one clause. *Verified: GRADE SCORE/100, N of M failed, `orchestrator`, target `model`, YYYY-MM-DD.*
```

If no subsection fits your framework, add one in alphabetical order.

Reviewers will check the contract, follow your run command, and look at the recorded numbers. Expect
to be asked to run it again if the recorded date is old.

## Adding anything else

For every other section, one line, same format, minus the verified-run note. The description says
what the thing is and why someone would open it, not what category it belongs to.

Some specifics:

- **Repositories**: public only. Several `humanbound/*` repositories appear in GitHub search results
  but are private; they do not belong here.
- **Writing**: curated, not exhaustive. The blog has more posts than this list carries, on purpose.
  Argue for the post rather than the author.
- **Talks**: link the recording if one exists. An agenda listing is acceptable but say so.
- **Related projects**: neighboring tools are welcome, including competitors. Describe them
  accurately; a related project that does part of this better is useful information for a reader.

## What gets rejected

- Dead links, parked domains, and repositories archived or unmaintained for over a year.
- Marketing pages with no technical content.
- Examples without a recorded run.
- Anything that requires a paid account to even try, unless the section makes that explicit.
- Self-promotion of a project nobody else uses. Having written the thing is not a
  disqualification, and several entries here were written by people close to the project. It does
  mean the entry is held to the contract more strictly, not less.

## Local development

The site is generated from `README.md`. Nothing generates the README itself.

```bash
uv run site/build.py
python3 -m http.server -d site/output 8000
```

Before opening a pull request:

```bash
uv run --with pytest --with markdown-it-py --with jinja2 pytest site/tests -q
```

The parser tests exist because this architecture has one known failure mode: a formatting change in
the README that the build silently drops. If you add a new heading level or entry shape and the
tests fail, fix the builder rather than reverting the README.

## Code of conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
