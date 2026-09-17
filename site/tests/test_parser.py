"""Guards against the one known failure mode of generating a site from a README:
a formatting change the builder silently drops."""

import importlib.util
import sys
from pathlib import Path

import pytest
from markdown_it import MarkdownIt

SITE = Path(__file__).resolve().parent.parent
FIXTURE = Path(__file__).parent / "fixtures" / "sample.md"

spec = importlib.util.spec_from_file_location("build", SITE / "build.py")
build = importlib.util.module_from_spec(spec)
# Registered before execution because @dataclass resolves annotations through
# sys.modules and fails on a module that is not there yet.
sys.modules["build"] = build
spec.loader.exec_module(build)


@pytest.fixture
def parsed():
    parser = build.Parser(MarkdownIt("commonmark"))
    parser.parse(FIXTURE.read_text(encoding="utf-8"))
    return parser


def test_title_and_tagline(parsed):
    assert parsed.title == "Awesome Sample"
    assert parsed.tagline == 'A <a href="https://example.com">sample</a> list.'


def test_meta_sections_are_excluded(parsed):
    titles = [s.title for s in parsed.sections]
    assert titles == ["Official", "Agent examples"]


def test_anchors_match_github_slugs(parsed):
    assert [s.anchor for s in parsed.sections] == ["official", "agent-examples"]


def test_entries_split_name_url_and_description(parsed):
    entry = parsed.sections[0].groups[0].entries[0]
    assert entry.name == "engine"
    assert entry.url == "https://github.com/humanbound/humanbound"
    assert entry.description == "The testing engine."


def test_subheadings_become_groups(parsed):
    examples = parsed.sections[1]
    assert [g.title for g in examples.groups] == ["", "LangChain"]
    assert examples.count == 1


def test_group_intro_is_kept(parsed):
    assert "Vulnerable agents" in parsed.sections[1].groups[0].intro


def test_inline_markup_survives_in_descriptions(parsed):
    entry = parsed.sections[1].groups[1].entries[0]
    assert "<code>create_agent</code>" in entry.description
    assert "<em>Verified: F 27.38/100, 2026-09-10.</em>" in entry.description


def test_lede_excludes_the_blockquote(parsed):
    assert len(parsed.lede) == 1
    assert "sample list" not in " ".join(parsed.lede)


def test_nested_lists_do_not_leak_entries(parsed):
    # The Contents list is nested navigation and must not become entries.
    assert sum(s.count for s in parsed.sections) == 3


def test_llms_txt_is_plain_text(parsed):
    text = build.render_llms_txt(parsed)
    assert "<" not in text and "&quot;" not in text
    assert "> A sample list." in text
    assert "- [example](https://github.com/owner/example): Uses create_agent." in text


def test_real_readme_parses(tmp_path):
    out = build.build()
    html = (out / "index.html").read_text(encoding="utf-8")
    assert "Awesome Humanbound" in html
    assert 'id="agent-examples"' in html
    assert (out / "llms.txt").exists()
    assert (out / "CNAME").read_text(
        encoding="utf-8"
    ).strip() == "awesome.humanbound.ai"
