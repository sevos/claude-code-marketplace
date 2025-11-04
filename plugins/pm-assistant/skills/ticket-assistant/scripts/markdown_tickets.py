#!/usr/bin/env python3
"""
Local Markdown Ticket Manager

Manages tickets stored as individual markdown files in a docs/tickets directory.
Each ticket has YAML frontmatter with metadata and relationships.

Operations:
- list_tickets: Scan and return all tickets with metadata
- get_ticket: Fetch specific ticket with full details
- create_ticket: Generate ID and create new ticket file
- update_ticket: Modify existing ticket
- search_tickets: Filter tickets by criteria
- analyze_dependencies: Build dependency graph
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import yaml

class MarkdownTicketManager:
    def __init__(self, tickets_dir: str):
        """Initialize with path to tickets directory."""
        self.tickets_dir = Path(tickets_dir)
        self.tickets_dir.mkdir(parents=True, exist_ok=True)
        self.counter_file = self.tickets_dir / ".ticket_counter"

    def _get_next_id(self) -> str:
        """Get next ticket ID by reading/updating counter file."""
        if self.counter_file.exists():
            try:
                current = int(self.counter_file.read_text().strip())
            except ValueError:
                current = 0
        else:
            # Scan existing files to find highest ID
            current = 0
            for f in self.tickets_dir.glob("TICKET-*.md"):
                match = re.search(r'TICKET-(\d+)', f.name)
                if match:
                    num = int(match.group(1))
                    current = max(current, num)

        next_id = current + 1
        self.counter_file.write_text(str(next_id))
        return f"TICKET-{next_id:03d}"

    def _parse_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """Parse YAML frontmatter and return (metadata, body)."""
        if not content.startswith("---"):
            return {}, content

        try:
            parts = content.split("---", 2)
            if len(parts) < 3:
                return {}, content

            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return frontmatter or {}, body
        except yaml.YAMLError:
            return {}, content

    def _create_frontmatter(self, metadata: Dict[str, Any]) -> str:
        """Create YAML frontmatter from metadata dict."""
        # Ensure required fields
        if 'created_at' not in metadata:
            metadata['created_at'] = datetime.now().isoformat()
        if 'status' not in metadata:
            metadata['status'] = 'Backlog'

        yaml_str = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_str}---\n"

    def list_tickets(self, status: Optional[str] = None, ticket_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all tickets, optionally filtered by status or type."""
        tickets = []

        for md_file in sorted(self.tickets_dir.glob("TICKET-*.md")):
            content = md_file.read_text()
            metadata, body = self._parse_frontmatter(content)

            # Apply filters
            if status and metadata.get('status') != status:
                continue
            if ticket_type and metadata.get('type') != ticket_type:
                continue

            metadata['id'] = md_file.stem
            metadata['_file'] = md_file.name
            tickets.append(metadata)

        return tickets

    def get_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Get full ticket details including body."""
        ticket_file = self.tickets_dir / f"{ticket_id}.md"

        if not ticket_file.exists():
            return None

        content = ticket_file.read_text()
        metadata, body = self._parse_frontmatter(content)

        metadata['id'] = ticket_id
        metadata['body'] = body
        return metadata

    def create_ticket(self, title: str, description: str, ticket_type: str = "Feature",
                     parent: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Create a new ticket and return its details."""
        ticket_id = self._get_next_id()

        metadata = {
            'title': title,
            'type': ticket_type,
            'status': kwargs.get('status', 'Backlog'),
            'created_at': datetime.now().isoformat(),
        }

        # Add optional metadata
        if parent:
            metadata['parent'] = parent

        # Add any additional metadata passed in
        for key in ['blocks', 'blocked_by', 'labels', 'estimate']:
            if key in kwargs:
                metadata[key] = kwargs[key]

        # Create file content
        frontmatter = self._create_frontmatter(metadata)
        content = frontmatter + description

        # Write file
        ticket_file = self.tickets_dir / f"{ticket_id}.md"
        ticket_file.write_text(content)

        metadata['id'] = ticket_id
        metadata['body'] = description
        return metadata

    def update_ticket(self, ticket_id: str, **updates) -> Optional[Dict[str, Any]]:
        """Update an existing ticket."""
        ticket_file = self.tickets_dir / f"{ticket_id}.md"

        if not ticket_file.exists():
            return None

        # Get current content
        content = ticket_file.read_text()
        metadata, body = self._parse_frontmatter(content)

        # Update metadata
        for key, value in updates.items():
            if key == 'body':
                body = value
            elif key == 'description':
                body = value
            else:
                metadata[key] = value

        # Write updated content
        frontmatter = self._create_frontmatter(metadata)
        new_content = frontmatter + body
        ticket_file.write_text(new_content)

        metadata['id'] = ticket_id
        metadata['body'] = body
        return metadata

    def search_tickets(self, query: str = "", status: Optional[str] = None,
                      ticket_type: Optional[str] = None, parent: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search tickets by query text and filters."""
        tickets = self.list_tickets(status=status, ticket_type=ticket_type)

        if not query:
            return tickets

        # Search in title, description (first line of body)
        query_lower = query.lower()
        results = []

        for ticket in tickets:
            if query_lower in ticket.get('title', '').lower():
                results.append(ticket)
                continue

            # Check body preview
            full_ticket = self.get_ticket(ticket['id'])
            if full_ticket and query_lower in full_ticket.get('body', '').lower():
                results.append(ticket)

        return results

    def get_subtickets(self, parent_id: str) -> List[Dict[str, Any]]:
        """Get all tickets that have this ticket as parent."""
        tickets = self.list_tickets()
        return [t for t in tickets if t.get('parent') == parent_id]

    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze ticket dependencies and return dependency graph."""
        tickets = self.list_tickets()

        # Build relationship maps
        blocks_map = {}  # ticket_id -> [list of tickets it blocks]
        blocked_by_map = {}  # ticket_id -> [list of tickets blocking it]
        parent_map = {}  # ticket_id -> parent ticket_id

        for ticket in tickets:
            ticket_id = ticket['id']

            # Parent relationships
            if ticket.get('parent'):
                parent_map[ticket_id] = ticket['parent']

            # Blocks relationships
            if ticket.get('blocks'):
                blocks = ticket['blocks'] if isinstance(ticket['blocks'], list) else [ticket['blocks']]
                blocks_map[ticket_id] = blocks
                for blocked_ticket in blocks:
                    if blocked_ticket not in blocked_by_map:
                        blocked_by_map[blocked_ticket] = []
                    blocked_by_map[blocked_ticket].append(ticket_id)

            # Blocked-by relationships (explicit)
            if ticket.get('blocked_by'):
                blocked_by = ticket['blocked_by'] if isinstance(ticket['blocked_by'], list) else [ticket['blocked_by']]
                if ticket_id not in blocked_by_map:
                    blocked_by_map[ticket_id] = []
                blocked_by_map[ticket_id].extend(blocked_by)

        return {
            'blocks': dict(blocks_map),
            'blocked_by': dict(blocked_by_map),
            'parent': parent_map,
            'total_tickets': len(tickets),
        }


def main():
    """CLI interface for ticket operations."""
    if len(sys.argv) < 2:
        print("Usage: markdown_tickets.py <operation> [args]")
        print("Operations: list, get, create, update, search, analyze-dependencies, get-subtickets")
        sys.exit(1)

    operation = sys.argv[1]
    tickets_dir = os.getenv('TICKETS_DIR', './docs/tickets')
    manager = MarkdownTicketManager(tickets_dir)

    try:
        if operation == 'list':
            status = sys.argv[2] if len(sys.argv) > 2 else None
            ticket_type = sys.argv[3] if len(sys.argv) > 3 else None
            tickets = manager.list_tickets(status=status, ticket_type=ticket_type)
            print(json.dumps(tickets, indent=2))

        elif operation == 'get':
            if len(sys.argv) < 3:
                print("Usage: markdown_tickets.py get <ticket_id>")
                sys.exit(1)
            ticket = manager.get_ticket(sys.argv[2])
            if ticket:
                print(json.dumps(ticket, indent=2))
            else:
                print(json.dumps({'error': f'Ticket {sys.argv[2]} not found'}))
                sys.exit(1)

        elif operation == 'create':
            # Read JSON from stdin for complex data
            input_data = json.loads(sys.stdin.read())
            ticket = manager.create_ticket(**input_data)
            print(json.dumps(ticket, indent=2))

        elif operation == 'update':
            if len(sys.argv) < 3:
                print("Usage: markdown_tickets.py update <ticket_id>")
                sys.exit(1)
            input_data = json.loads(sys.stdin.read())
            ticket = manager.update_ticket(sys.argv[2], **input_data)
            if ticket:
                print(json.dumps(ticket, indent=2))
            else:
                print(json.dumps({'error': f'Ticket {sys.argv[2]} not found'}))
                sys.exit(1)

        elif operation == 'search':
            query = sys.argv[2] if len(sys.argv) > 2 else ""
            status = sys.argv[3] if len(sys.argv) > 3 else None
            tickets = manager.search_tickets(query=query, status=status)
            print(json.dumps(tickets, indent=2))

        elif operation == 'analyze-dependencies':
            deps = manager.analyze_dependencies()
            print(json.dumps(deps, indent=2))

        elif operation == 'get-subtickets':
            if len(sys.argv) < 3:
                print("Usage: markdown_tickets.py get-subtickets <parent_id>")
                sys.exit(1)
            subtickets = manager.get_subtickets(sys.argv[2])
            print(json.dumps(subtickets, indent=2))

        else:
            print(f"Unknown operation: {operation}")
            sys.exit(1)

    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
