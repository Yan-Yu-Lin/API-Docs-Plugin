#!/usr/bin/env python3
"""
Convert MDX files to clean Markdown files for the MCP skill.

Usage:
    uv run convert_mdx_to_md.py <source_dir> <output_dir>
"""

import re
import sys
from pathlib import Path
from typing import Optional


class MDXToMDConverter:
    """Convert MDX files to clean Markdown."""

    def __init__(self):
        # Patterns for JSX components to remove/convert
        self.component_patterns = [
            # Self-closing components
            (r'<Frame[^>]*>\s*<img[^>]*\/>\s*<\/Frame>', ''),
            (r'<img[^>]*\/>', ''),

            # Block components with content - extract content
            (r'<Note>\s*(.*?)\s*<\/Note>', r'> **Note:** \1'),
            (r'<Warning>\s*(.*?)\s*<\/Warning>', r'> **Warning:** \1'),
            (r'<Tip>\s*(.*?)\s*<\/Tip>', r'> **Tip:** \1'),

            # Card components - convert to text
            (r'<Card\s+title="([^"]*)"[^>]*>\s*(.*?)\s*<\/Card>', r'**\1**: \2'),
            (r'<CardGroup[^>]*>(.*?)<\/CardGroup>', r'\1'),

            # Accordion components
            (r'<AccordionGroup>(.*?)<\/AccordionGroup>', r'\1'),
            (r'<Accordion\s+title="([^"]*)"[^>]*>\s*(.*?)\s*<\/Accordion>', r'### \1\n\n\2'),

            # Code groups - keep inner content
            (r'<CodeGroup>(.*?)<\/CodeGroup>', r'\1'),

            # Steps - convert to numbered list
            (r'<Steps>(.*?)<\/Steps>', r'\1'),
            (r'<Step\s+title="([^"]*)"[^>]*>(.*?)<\/Step>', r'**\1**\n\n\2'),

            # Tooltips - keep text only
            (r'<Tooltip\s+tip="[^"]*">([^<]*)<\/Tooltip>', r'\1'),

            # Generic self-closing tags
            (r'<[A-Z][a-zA-Z]*\s*\/>', ''),
        ]

        self.in_code_block = False
        self.in_jsx_block = False

    def is_code_block_delimiter(self, line: str) -> bool:
        """Check if line is a code block delimiter."""
        stripped = line.strip()
        return stripped.startswith('```')

    def remove_frontmatter(self, content: str) -> tuple[Optional[str], str]:
        """Remove YAML frontmatter and extract title."""
        lines = content.split('\n')
        if not lines or lines[0].strip() != '---':
            return None, content

        # Find the closing ---
        title = None
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break
            # Extract title if found
            if lines[i].strip().startswith('title:'):
                title = lines[i].split(':', 1)[1].strip().strip('"\'')

        if end_idx == -1:
            return None, content

        # Return content without frontmatter
        remaining = '\n'.join(lines[end_idx + 1:])
        return title, remaining

    def clean_jsx_components(self, content: str) -> str:
        """Remove or convert JSX components to markdown."""
        # Apply patterns (for multi-line, use DOTALL flag)
        for pattern, replacement in self.component_patterns:
            content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)

        return content

    def process_line(self, line: str) -> Optional[str]:
        """Process a single line of MDX."""
        # Track code blocks
        if self.is_code_block_delimiter(line):
            self.in_code_block = not self.in_code_block
            return line

        # Don't modify lines inside code blocks
        if self.in_code_block:
            return line

        # Remove import statements
        if line.strip().startswith('import '):
            return None

        # Remove export statements
        if line.strip().startswith('export '):
            return None

        # Simple inline JSX tag removal (for non-block components)
        # Remove self-closing tags like <Frame />, <Hero />
        line = re.sub(r'<[A-Z][a-zA-Z0-9]*\s*\/>', '', line)

        # Remove opening/closing tags for simple components
        line = re.sub(r'</?[A-Z][a-zA-Z0-9]*[^>]*>', '', line)

        return line

    def convert_content(self, content: str) -> str:
        """Convert MDX content to clean Markdown."""
        # First pass: Remove frontmatter and get title
        title, content = self.remove_frontmatter(content)

        # Second pass: Clean block-level JSX components
        content = self.clean_jsx_components(content)

        # Third pass: Process line by line for inline JSX
        lines = content.split('\n')
        processed_lines = []

        self.in_code_block = False
        for line in lines:
            processed = self.process_line(line)
            if processed is not None:
                processed_lines.append(processed)

        result = '\n'.join(processed_lines)

        # Add title as markdown header if found
        if title:
            result = f"# {title}\n\n{result}"

        # Clean up excessive blank lines
        result = re.sub(r'\n{3,}', '\n\n', result)

        return result.strip() + '\n'

    def convert_file(self, input_path: Path, output_path: Path):
        """Convert a single MDX file to MD."""
        print(f"Converting: {input_path.relative_to(input_path.parent.parent)}")

        # Read MDX content
        content = input_path.read_text(encoding='utf-8')

        # Convert to MD
        md_content = self.convert_content(content)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write MD file
        output_path.write_text(md_content, encoding='utf-8')
        print(f"  → {output_path.relative_to(output_path.parent.parent.parent)}")

    def convert_directory(self, source_dir: Path, output_dir: Path):
        """Convert all MDX files in a directory, preserving structure."""
        mdx_files = list(source_dir.rglob('*.mdx'))

        print(f"\nFound {len(mdx_files)} MDX files to convert\n")

        for mdx_file in mdx_files:
            # Calculate relative path from source
            rel_path = mdx_file.relative_to(source_dir)

            # Change extension to .md
            md_filename = rel_path.stem + '.md'
            output_path = output_dir / rel_path.parent / md_filename

            try:
                self.convert_file(mdx_file, output_path)
            except Exception as e:
                print(f"  ✗ Error converting {mdx_file}: {e}")

        print(f"\n✓ Conversion complete! {len(mdx_files)} files processed.")


def main():
    if len(sys.argv) != 3:
        print("Usage: uv run convert_mdx_to_md.py <source_dir> <output_dir>")
        print("\nExample:")
        print("  uv run convert_mdx_to_md.py /tmp/modelcontextprotocol/docs ./anthropic/skills/model-context-protocol/references")
        sys.exit(1)

    source_dir = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve()

    if not source_dir.exists():
        print(f"Error: Source directory does not exist: {source_dir}")
        sys.exit(1)

    if not source_dir.is_dir():
        print(f"Error: Source path is not a directory: {source_dir}")
        sys.exit(1)

    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")

    converter = MDXToMDConverter()
    converter.convert_directory(source_dir, output_dir)


if __name__ == '__main__':
    main()
