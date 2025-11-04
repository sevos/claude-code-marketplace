# Claude Code Marketplace

A personal marketplace for Claude Code plugins, commands, skills, and agents.

## Available Plugins

### Git Plugin
Set of commands, skills, and agents to manage git projects.

**Features:**
- `/open-pr` - Command for opening pull requests

### Rails Plugin
Set of commands, skills, and agents to work on Ruby on Rails projects.

**Features:**
- `/rails:plan` - Plan implementation of a Rails feature with multi-tenant architecture and DaisyUI

## Adding This Marketplace to Claude Code

To add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add sevos/claude-code-marketplace
```

That's it! Claude Code will automatically fetch the marketplace from GitHub.

### Alternative Methods

If you prefer to use the full Git URL:
```bash
/plugin marketplace add https://github.com/sevos/claude-code-marketplace.git
```

For local development or testing:
```bash
/plugin marketplace add /path/to/sevos-claude-code-marketplace
```

## Installing Plugins

Once you've added the marketplace, you can install plugins using one of these methods:

### Method 1: Browse and Install Interactively

Open the plugin menu in Claude Code:
```bash
/plugin
```

This will show you all available plugins from all your marketplaces. Browse and select the plugins you want to install.

### Method 2: Install Specific Plugins

Install a specific plugin from this marketplace:

```bash
/plugin install git@sevos-claude-code-marketplace
```

or

```bash
/plugin install rails@sevos-claude-code-marketplace
```

## Using Installed Plugins

After installing a plugin, its commands will be available in Claude Code:

### Git Plugin Commands
- `/open-pr` - Open a pull request with AI assistance

### Rails Plugin Commands
- `/rails:plan` - Plan Rails feature implementation

## Plugin Structure

Each plugin in this marketplace follows the standard Claude Code plugin structure:

```
plugins/
├── plugin-name/
│   ├── .claude-plugin/
│   │   └── plugin.json       # Plugin metadata
│   ├── commands/              # Slash commands
│   │   └── command.md
│   ├── skills/                # Agent skills
│   │   └── skill.md
│   └── agents/                # Specialized agents
│       └── agent.md
```

## Team Installation

For team projects, you can specify required marketplaces in `.claude/settings.json`:

```json
{
  "marketplaces": [
    {
      "name": "sevos-claude-code-marketplace",
      "source": {
        "type": "github",
        "repo": "sevos/claude-code-marketplace"
      }
    }
  ],
  "enabledPlugins": [
    "git@sevos-claude-code-marketplace",
    "rails@sevos-claude-code-marketplace"
  ]
}
```

When team members trust the repository folder, Claude Code automatically installs these marketplaces and plugins.

## Contributing

To add a new plugin to this marketplace:

1. Create a new directory under `plugins/`
2. Add a `.claude-plugin/plugin.json` file with plugin metadata
3. Add your commands, skills, or agents in the appropriate directories
4. Update the `.claude-plugin/marketplace.json` file to include your plugin
5. Submit a pull request

## License

This marketplace and its plugins are available for personal use.

## Author

Artur Roszczyk ([email protected])
