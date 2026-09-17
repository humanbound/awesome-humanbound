<p align="center">
  <img src="site/static/logo.png" alt="Humanbound" width="420">
</p>

# Awesome Humanbound

<p align="center">
  <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
</p>

> Agents, examples, and reading for [Humanbound](https://www.humanbound.ai), the open-source adversarial testing engine for AI agents.

Humanbound throws model-generated attacks at an agent over HTTP, then grades the transcripts against the OWASP Top 10 for LLM and Agentic Applications.

Most of a list like this is links. The examples come first here because they are the part you can actually run: clone one, start it, and watch it fail. If you have an agent of your own, [add it](CONTRIBUTING.md).

## Contents

- [Agent examples](#agent-examples)
- [Getting started](#getting-started)
- [Official](#official)
- [Writing](#writing)
- [Talks](#talks)
- [Community](#community)
- [Related projects](#related-projects)
- [Standards and regulation](#standards-and-regulation)

## Agent examples

Agents built to lose. Clone one, start it, point `hb` at it, and read the report.

Every entry ships a `bot-config.json` and a `scope.yaml`, and records what happened the last time someone ran it. The [Example Contract](CONTRIBUTING.md#the-example-contract) sets the bar. The [open requests](https://github.com/humanbound/awesome-humanbound/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) cover frameworks nobody has written one for yet.

### Plain HTTP and FastAPI

- [humanbound-quickstart](https://github.com/iayanpahwa/humanbound-quickstart) - FastAPI support bot that calls an OpenAI-compatible endpoint directly, with no agent framework in between. One file, `uv run agent.py`. *Verified: D 43.14/100, 43 of 97 conversations failed, `owasp_agentic`, target `gpt-4o-mini`, 2026-09-04.*

### LangChain

- [humanbound-langchain-example](https://github.com/iayanpahwa/humanbound-langchain-example) - LangChain 1.x `create_agent` with order-lookup and refund tools behind a 15-line FastAPI wrapper. Talks itself into refunding orders that were never placed. *Verified: F 27.38/100, 61 of 97 turns failed, `restriction_bypass` and `human_manipulation` dominant, `owasp_agentic`, 2026-09-10.*

### Wanted

Nobody has written one for LangGraph, CrewAI, the OpenAI Agents SDK, an MCP-backed agent, or a RAG agent that can be poisoned through retrieval. Each is an open issue, and each is a reasonable first contribution.

## Getting started

- [Installation](https://docs.humanbound.ai/getting-started/installation/) - The extras decide what you get: `engine` for local testing, `firewall` for runtime defense.
- [Quick start](https://docs.humanbound.ai/getting-started/quick-start/) - First run, end to end.
- [Agent configuration](https://docs.humanbound.ai/getting-started/agent-config/) - The `bot-config.json` contract: `chat_completion.{endpoint,headers,payload}`, with `$PROMPT` and `$CONVERSATION` as the substitution tokens.
- [Local engine](https://docs.humanbound.ai/local-engine/) - Running without a Platform account, including against Ollama.
- [Orchestrators](https://docs.humanbound.ai/local-engine/orchestrators/) - What `--quick`, `--deep`, and `--full` actually select.
- [LLM as judge](https://docs.humanbound.ai/concepts/llm-as-judge/) - How a conversation gets graded, and why one bad turn sinks the whole thing.
- [Command reference](https://docs.humanbound.ai/reference/commands/) - Every `hb` subcommand.

## Official

### Repositories

- [humanbound](https://github.com/humanbound/humanbound) - The adversarial testing engine, SDK, and `hb` CLI. Runs fully local or against the hosted Platform.
- [humanbound-firewall](https://github.com/humanbound/humanbound-firewall) - Runtime firewall for agents. Cheap local tiers run first, and an LLM judge only gets called when they are uncertain.
- [plugins](https://github.com/humanbound/plugins) - Plugin marketplace for Claude Code and Cursor. It ships four agent skills, of which `running-adversarial-tests` is the one users trigger.
- [actions](https://github.com/humanbound/actions) - Official GitHub Actions. Runs OWASP-aligned tests in CI and writes SARIF.

### Packages and marketplace

- [humanbound on PyPI](https://pypi.org/project/humanbound/) - `pip install "humanbound[engine,firewall]"`. The CLI entry point is `hb`.
- [humanbound-firewall on PyPI](https://pypi.org/project/humanbound-firewall/) - The firewall on its own, for runtime use without the test engine.
- [Humanbound AI Agent Security Testing](https://github.com/marketplace/actions/humanbound-ai-agent-security-testing) - The Action on GitHub Marketplace. It writes a SARIF file but does not upload it, so pair it with a `github/codeql-action/upload-sarif` step.

### Sites and services

- [humanbound.ai](https://www.humanbound.ai) - Product site.
- [docs.humanbound.ai](https://docs.humanbound.ai) - Documentation, 44 pages covering the local engine, testing, defense, and integrations.
- [Platform API reference](https://api.humanbound.ai/api/docs) - Interactive OpenAPI docs for the hosted Platform.
- [status.humanbound.ai](https://status.humanbound.ai/) - Platform status page.
- [llms.txt](https://humanbound.ai/llms.txt) - Machine-readable site index for agents and coding tools.

### Self-assessment tools

- [AI Security Readiness Checklist](https://www.humanbound.ai/ai-readiness) - 23 questions, written for the person who has to sign off rather than the person who built the agent.
- [Firewall Cost Calculator](https://www.humanbound.ai/firewall-calculator) - Estimates what the firewall tiers cost against your own traffic shape.

## Writing

### Tutorials

- [Attack your own AI agent in under 10 minutes](https://www.humanbound.ai/blog/attack-your-own-ai-agent-in-under-10-minutes-then-secure-it-before-deploying) - Ayan Pahwa, 2026-09-07. Builds a weak support agent, breaks it, patches it, and shows why the score barely moves afterwards.
- [How to test a LangChain agent for security](https://www.humanbound.ai/blog/how-to-test-a-langchain-agent-for-security) - Ayan Pahwa, 2026-09-11. Wrapping an agent you already have in FastAPI so `hb` can reach it.

### Essays

- [Agent Security Debt: nobody is trying to break your AI agent until it ships](https://www.humanbound.ai/blog/agent-security-debt-nobody-is-trying-to-break-your-ai-agent) - Ayan Pahwa, 2026-08-31. Guardrails and governance and evals all exist. Adversarial testing before launch mostly does not, which is how IoT went wrong too.
- [The enforcement illusion: why AI agent security starts with testing, not walls](https://www.humanbound.ai/blog/the-enforcement-illusion-ai-agent-security-starts-with-testing) - Kostas Siabanis, 2026-03-11. The argument behind testing before firewalling.
- [Your agent passed its security test. That was three weeks ago.](https://www.humanbound.ai/blog/your-agent-passed-its-security-test-that-was-three-weeks-ago) - Kostas Siabanis, 2026-03-17. Why a point-in-time assessment goes stale faster for agents than for ordinary software.
- [AI security means two different things](https://www.humanbound.ai/blog/ai-security-ai4sec-vs-sec4ai) - Kostas Siabanis, 2026-04-27. Separates using AI for security from securing AI itself, which most vendor copy smears together.
- [Why we open-sourced humanbound-firewall](https://www.humanbound.ai/blog/why-we-open-sourced-humanbound-firewall) - Demetris Gerogiannis, 2026-05-11. The reasoning, from the co-founder who made the call.
- [Beyond moderation: why LLM systems need a policy layer](https://www.humanbound.ai/blog/beyond-moderation-llm-policy-layer) - Spyros Briakos, 2026-04-07. Where content moderation stops being enough for an agent that can act on its own.
- [The agent attack scenario library](https://www.humanbound.ai/blog/ai-agent-attack-scenario-library) - Sofia Aliferi, 2026-08-20. The case for a shared, OWASP-mapped corpus of agent attacks.

### Elsewhere

Humanbound also posts on [dev.to](https://dev.to/humanbound_ai), and a lot of it never reaches the blog. Worth reading on their own:

- [The Taiwan attack: when an AI agent swarm ran a government hack with no one watching](https://dev.to/humanbound_ai/the-taiwan-attack-when-an-ai-agent-swarm-ran-a-government-hack-with-no-one-watching-5e3m) - Sofia Aliferi, 2026-08-19.
- [A new paper argues that your prompt injection defence can't win](https://dev.to/humanbound_ai/a-new-paper-argues-that-your-prompt-injection-defence-cant-win-26oc) - Sofia Aliferi, 2026-07-24.
- [We put adversarial agent testing directly in Claude Code and Cursor](https://dev.to/humanbound_ai/we-put-adversarial-agent-testing-directly-in-claude-code-and-cursor-1903) - Sofia Aliferi, 2026-07-23. The announcement behind the `plugins` repo.
- [Trust Boundary Report, issue 02](https://dev.to/humanbound_ai/trust-boundary-report-issue-02-the-month-agentic-ai-stopped-being-a-thought-experiment-38b6) - Sofia Aliferi, 2026-08-04. A monthly roundup of agentic security incidents.

## Talks

- [Break first. Fix fast. Ship safe. Repeat.](https://productledhub.com/gen-ai-unfold-summit/agenda/) - Demetris Gerogiannis at the Gen AI Unfold Summit, 2026-05-14. Continuous security testing inside the development cycle. Agenda listing only, no recording published.
- [Securing agentic AI: before your agent betrays you](https://www.meetup.com/ai-and-beers/events/314414720/) - Panel at AI and Beers Athens #6, 2026-05-28, with John Sotiropoulos, who leads the OWASP Agentic AI Top 10. No recording published.
- [Ship agents that survive the real web](https://www.zyte.com/blog/the-page-your-agent-scrapes-is-now-an-attack-surface-is-it-ready-for-the-hostile-web/) - Demetris Gerogiannis with Zyte, 2026-09-24. Upcoming at the time of writing. Zyte published slides and a recording for their previous meetup, so expect the same here.

## Community

- [Discord](https://discord.gg/QFTD6tr9zu) - The project's community server.
- [GitHub Discussions](https://github.com/humanbound/humanbound/discussions) - Questions and proposals against the engine.
- [Contributing to Humanbound](https://github.com/humanbound/humanbound/blob/main/CONTRIBUTING.md) - Upstream takes DCO sign-off (`git commit -s`) rather than a CLA.

Humanbound also turns up in these third-party lists:

- [awesome-llm-security](https://github.com/beyefendi/awesome-llm-security)
- [awesome-ai-security](https://github.com/gmh5225/awesome-ai-security)
- [AI Red Teaming Guide](https://github.com/requie/AI-Red-Teaming-Guide)

## Related projects

Tools that solve a neighboring problem. Humanbound ships adapters for promptfoo and PyRIT, so those two sit alongside it rather than against it.

- [promptfoo](https://github.com/promptfoo/promptfoo) - LLM evaluation and red-teaming toolkit, with its own `redteam_run`.
- [PyRIT](https://github.com/Azure/PyRIT) - Microsoft's Python Risk Identification Toolkit for generative AI.
- [garak](https://github.com/NVIDIA/garak) - NVIDIA's LLM vulnerability scanner, organized around probes.
- [agentic_security](https://github.com/msoedov/agentic_security) - Agentic LLM vulnerability scanner and fuzzer.
- [Scenario](https://github.com/langwatch/scenario) - Simulation-based multi-turn agent testing from LangWatch.
- [LLM Guard](https://github.com/protectai/llm-guard) - Runtime input and output guardrails, which puts it next door to humanbound-firewall.

## Standards and regulation

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) - The taxonomy `hb` reports against.
- [OWASP Agentic AI: threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) - The agentic extension, which is what the `owasp_agentic` orchestrator targets.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) - Referenced by Humanbound's compliance mapping.
- [EU AI Act explorer](https://artificialintelligenceact.eu/) - Searchable text of the regulation.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Examples have to meet the Example Contract. Everything else has to be real, current, and worth a stranger's time.

## License

[CC0 1.0](LICENSE). To the extent possible under law, contributors have waived all copyright and related rights to this work.
