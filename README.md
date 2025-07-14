# Claude Code

![](https://img.shields.io/badge/Node.js-18%2B-brightgreen?style=flat-square) [![npm]](https://www.npmjs.com/package/@anthropic-ai/claude-code)

[npm]: https://img.shields.io/npm/v/@anthropic-ai/claude-code.svg?style=flat-square

Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows -- all through natural language commands. Use it in your terminal, IDE, or tag @claude on Github.

**Learn more in the [official documentation](https://docs.anthropic.com/en/docs/claude-code/overview)**.

<img src="./demo.gif" />

## Get started

1. Install Claude Code:

```sh
npm install -g @anthropic-ai/claude-code
```

2. Navigate to your project directory and run `claude`.

## LM Studio Integration

Claude Code now supports integration with local LM Studio models through the MCP (Model Context Protocol). This allows you to use your own local models instead of or alongside Anthropic's Claude models.

### Quick Setup

1. **Install LM Studio** and load a model
2. **Start the local server** (usually on port 1234)
3. **Run the integration script**:
   ```bash
   python3 lm_studio_integration.py
   ```
4. **Use with Claude Code**:
   ```bash
   claude --mcp-config ~/.claude/mcp.json "your prompt here"
   ```

### Features

- **Automatic model discovery**: Lists all loaded models in LM Studio
- **Interactive model selection**: Choose which model to use
- **Health checking**: Verifies LM Studio server is running
- **MCP integration**: Works seamlessly with Claude Code's tool system

For detailed setup instructions, see [README_LM_STUDIO.md](README_LM_STUDIO.md).

## Reporting Bugs

We welcome your feedback. Use the `/bug` command to report issues directly within Claude Code, or file a [GitHub issue](https://github.com/anthropics/claude-code/issues).

## Data collection, usage, and retention

When you use Claude Code, we collect feedback, which includes usage data (such as code acceptance or rejections), associated conversation data, and user feedback submitted via the `/bug` command.

### How we use your data

We may use feedback to improve our products and services, but we will not train generative models using your feedback from Claude Code. Given their potentially sensitive nature, we store user feedback transcripts for only 30 days.

If you choose to send us feedback about Claude Code, such as transcripts of your usage, Anthropic may use that feedback to debug related issues and improve Claude Code's functionality (e.g., to reduce the risk of similar bugs occurring in the future).

### Privacy safeguards

We have implemented several safeguards to protect your data, including limited retention periods for sensitive information, restricted access to user session data, and clear policies against using feedback for model training.

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).
