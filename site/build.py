#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py>=3.0", "jinja2>=3.1"]
# ///
"""Render README.md into a static site.

The README is the source of truth. This walks its token stream rather than
matching text, so a formatting change surfaces as a parse failure or a missing
section in the tests instead of silently mangled output.
"""

from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass, field
from html import unescape
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUTPUT = SITE / "output"

SITE_URL = "https://awesome.humanbound.ai"

# Repo-meta headings. They belong in the README but the site carries them in the
# footer instead of as list sections.
SKIP_SECTIONS = {"contents", "contributing", "license"}
DESCRIPTION = (
    "Agents, examples, and reading for Humanbound, the open-source "
    "adversarial testing engine for AI agents."
)


@dataclass
class Entry:
    name: str
    url: str
    description: str


@dataclass
class Group:
    title: str
    intro: str = ""
    entries: list[Entry] = field(default_factory=list)


@dataclass
class Section:
    title: str
    anchor: str
    groups: list[Group] = field(default_factory=list)

    @property
    def count(self) -> int:
        return sum(len(g.entries) for g in self.groups)


def slugify(text: str) -> str:
    """GitHub's heading anchor rules, which the README's Contents list assumes."""
    slug = text.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    return re.sub(r"[\s_]+", "-", slug)


class Parser:
    """Walks a flat markdown-it token stream into sections, groups and entries."""

    def __init__(self, md: MarkdownIt) -> None:
        self.md = md
        self.title = ""
        self.tagline = ""
        self.lede: list[str] = []
        self.sections: list[Section] = []

    def parse(self, source: str) -> None:
        tokens = self.md.parse(source)
        section: Section | None = None
        group: Group | None = None
        skipping = False
        in_quote = False
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == "heading_open":
                text = tokens[i + 1].content
                if token.tag == "h1":
                    self.title = text
                elif token.tag == "h2":
                    skipping = text.strip().lower() in SKIP_SECTIONS
                    if skipping:
                        section = group = None
                    else:
                        section = Section(title=text, anchor=slugify(text))
                        group = Group(title="")
                        section.groups.append(group)
                        self.sections.append(section)
                elif token.tag == "h3" and section is not None:
                    group = Group(title=text)
                    section.groups.append(group)
                i += 3
                continue

            if skipping:
                i += 1
                continue

            if token.type == "blockquote_open":
                in_quote = True
                if not self.tagline:
                    self.tagline = self._collect_blockquote(tokens, i)

            elif token.type == "blockquote_close":
                in_quote = False

            elif token.type == "paragraph_open" and not in_quote:
                html = self._render_inline(tokens[i + 1].children or [])
                if section is None:
                    if html and "img" not in html and "awesome.re" not in html:
                        self.lede.append(html)
                elif group is not None:
                    group.intro = (
                        f"{group.intro}<p>{html}</p>"
                        if group.intro
                        else f"<p>{html}</p>"
                    )

            elif token.type == "bullet_list_open" and group is not None:
                i = self._collect_entries(tokens, i, group)
                continue

            i += 1

    def _collect_entries(self, tokens: list, start: int, group: Group) -> int:
        """Consume one bullet list, appending an Entry per item. Returns next index."""
        depth = 0
        i = start
        while i < len(tokens):
            token = tokens[i]
            if token.type == "bullet_list_open":
                depth += 1
            elif token.type == "bullet_list_close":
                depth -= 1
                if depth == 0:
                    return i + 1
            elif token.type == "inline" and tokens[i - 1].type == "paragraph_open":
                entry = self._to_entry(token.children or [])
                if entry is not None:
                    group.entries.append(entry)
            i += 1
        return i

    def _to_entry(self, children: list) -> Entry | None:
        if not children or children[0].type != "link_open":
            return None
        url = children[0].attrGet("href") or ""
        close = next(
            (n for n, t in enumerate(children) if t.type == "link_close"),
            None,
        )
        if close is None:
            return None
        name = "".join(t.content for t in children[1:close])
        description = self._render_inline(children[close + 1 :]).lstrip(" —-–")
        return Entry(name=name, url=url, description=description.strip())

    def _render_inline(self, children: list) -> str:
        return self.md.renderer.render(children, self.md.options, {}).strip()

    def _collect_blockquote(self, tokens: list, start: int) -> str:
        parts = []
        for token in tokens[start:]:
            if token.type == "blockquote_close":
                break
            if token.type == "inline":
                parts.append(self._render_inline(token.children or []))
        return " ".join(parts)


def build(base_path: str = "") -> Path:
    md = MarkdownIt("commonmark").enable("strikethrough")
    parser = Parser(md)
    parser.parse((ROOT / "README.md").read_text(encoding="utf-8"))

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    shutil.copytree(SITE / "static", OUTPUT / "static")
    shutil.move(str(OUTPUT / "static" / "CNAME"), str(OUTPUT / "CNAME"))

    env = Environment(
        loader=FileSystemLoader(SITE / "templates"),
        autoescape=select_autoescape(["html"]),
    )
    prefix = base_path.rstrip("/")
    html = env.get_template("index.html").render(
        title=parser.title,
        tagline=parser.tagline,
        lede=parser.lede,
        sections=parser.sections,
        description=DESCRIPTION,
        site_url=SITE_URL,
        base=prefix,
        total=sum(s.count for s in parser.sections),
    )
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")
    (OUTPUT / "llms.txt").write_text(render_llms_txt(parser), encoding="utf-8")
    return OUTPUT


def plain_text(html_fragment: str) -> str:
    """Strip markup for the agent-facing llms.txt, which is plain text."""
    text = re.sub(r"<[^>]+>", "", html_fragment)
    return unescape(text).replace("\n", " ").strip()


def render_llms_txt(parser: Parser) -> str:
    lines = [f"# {parser.title}", "", f"> {plain_text(parser.tagline)}", ""]
    for section in parser.sections:
        lines.append(f"## {section.title}")
        lines.append("")
        for group in section.groups:
            for entry in group.entries:
                plain = plain_text(entry.description)
                lines.append(f"- [{entry.name}]({entry.url}): {plain}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    out = build(os.environ.get("BASE_PATH", ""))
    print(f"built {out}")
