# HTML Visualization Skill - Examples

This directory contains example visualizations created with the html-visualization skill.

## Example Requests

Here are some ways to trigger this skill:

### 1. Technical Documentation from Codebase

```
Create an HTML onboarding guide for our multi-tenant Rails system
```

This will:
- Analyze your codebase for tenant-related code
- Create ER diagrams of database relationships
- Include sequence diagrams of request flow
- Provide code examples from actual implementation
- Use long-page format for comprehensive reference

### 2. Library/Framework Tutorial

```
Create a slideshow presentation about React hooks
```

This will:
- Fetch latest React documentation via Context7 MCP
- Create slides for each hook (useState, useEffect, etc.)
- Include code examples with syntax highlighting
- Add lifecycle diagrams
- Use Reveal.js for presentation format

### 3. API Documentation

```
Create interactive API documentation for our REST endpoints
```

This will:
- Read routes and controllers from codebase
- Create tabbed dashboard interface
- Include request/response examples
- Add authentication flow diagrams
- Provide copy-to-clipboard for code snippets

### 4. Process Visualization

```
Visualize our customer onboarding process as an infographic
```

This will:
- Work from your description of the process
- Create flowcharts and swimlane diagrams
- Use vertical scroll format with large visuals
- Include minimal text, maximum visual impact
- Apply pastel color scheme throughout

### 5. Architecture Overview

```
Create an architecture visualization for our microservices system
```

This will:
- Analyze your codebase structure
- Create architecture diagrams showing services
- Include sequence diagrams for key flows
- Show component relationships
- Use dashboard or long-page format

## Tips for Best Results

1. **Be specific about format**: Mention "slideshow", "dashboard", "long-page", or "infographic" if you have a preference

2. **Provide context**: If the skill should analyze code, make sure your request mentions the specific area (e.g., "our authentication system", "payment processing")

3. **Mention diagrams**: If you want specific types of diagrams, ask for them (e.g., "include an ER diagram", "show the sequence flow")

4. **Specify audience**: Mention if it's for onboarding, documentation, presentation, or reference

## Output

The skill will create a self-contained HTML file that:
- **Saved to `/tmp` directory** with a timestamped filename (e.g., `/tmp/api-docs-20250104-143022.html`)
- **Automatically opens in your default browser** using `xdg-open`
- Works offline (all dependencies via CDN)
- Includes Mermaid diagrams with pastel colors
- Has syntax-highlighted code examples
- Is responsive and mobile-friendly
- Can be printed or exported to PDF
- Requires no build process - just open in browser

### File Location

All generated HTML files are saved to `/tmp` with timestamps:
- Format: `/tmp/{descriptive-name}-{timestamp}.html`
- Example: `/tmp/multi-tenancy-onboarding-20250104-143022.html`

The files remain available in `/tmp` until system restart or cleanup. You can:
- Reopen them anytime: `xdg-open /tmp/{filename}.html`
- List recent files: `ls -lt /tmp/*.html | head`
- Move to a permanent location: `mv /tmp/{filename}.html ~/Documents/`

## Customization

After the HTML is generated, you can:
- Edit content directly in the HTML file
- Adjust colors in the CSS section
- Modify Mermaid diagrams
- Add or remove sections
- Change the layout and styling

All templates are in the `templates/` directory for reference.
