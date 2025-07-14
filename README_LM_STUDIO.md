# LM Studio Integration for Claude Code

This integration allows you to use local LM Studio models with Claude Code through the MCP (Model Context Protocol) framework.

## Features

- **Automatic model discovery**: Lists all loaded models in LM Studio
- **Interactive model selection**: Choose which model to use
- **Health checking**: Verifies LM Studio server is running
- **Model testing**: Tests the selected model before configuration
- **MCP integration**: Works seamlessly with Claude Code's MCP system

## Prerequisites

1. **LM Studio**: Download and install from [lmstudio.ai](https://lmstudio.ai)
2. **Python 3.8+**: Required for the integration scripts
3. **Claude Code**: Must be installed and configured

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start LM Studio

1. Open LM Studio
2. Download and load a model of your choice
3. Go to the "Local Server" tab
4. Click "Start Server" (default port 1234)

### 3. Run the Integration Script

```bash
python3 lm_studio_integration.py
```

The script will:
- Check if LM Studio server is running
- List all available models
- Let you select which model to use
- Test the selected model
- Create the MCP configuration for Claude Code

### 4. Use with Claude Code

Once configured, you can use Claude Code with your local LM Studio model:

```bash
claude --mcp lmstudio "your prompt here"
```

## Available MCP Tools

The integration provides several tools you can use:

- `health_check`: Check if LM Studio server is running
- `list_models`: List all available models
- `get_current_model`: Show the currently configured model
- `chat_completion`: Send messages to the local model

## Configuration

The integration creates a configuration file at `~/.claude/mcp.json` with the following structure:

```json
{
  "lmstudio": {
    "command": "python3",
    "args": ["/home/mark/claude-code/lm_studio_mcp_server.py"],
    "env": {
      "LM_STUDIO_BASE_URL": "http://localhost:1234",
      "LM_STUDIO_MODEL": "your-selected-model"
    }
  }
}
```

## Troubleshooting

### Server Not Running
- Make sure LM Studio is open and the local server is started
- Check that the server is running on port 1234
- Verify no firewall is blocking the connection

### No Models Available
- Load a model in LM Studio first
- Make sure the model is fully loaded (not just downloaded)
- Check the LM Studio console for any error messages

### Model Test Failed
- Try a different model
- Check if the model is compatible with chat completions
- Verify the model has sufficient memory allocation

## Environment Variables

You can customize the integration with these environment variables:

- `LM_STUDIO_BASE_URL`: Base URL for LM Studio API (default: http://localhost:1234)
- `LM_STUDIO_MODEL`: Model ID to use (set automatically by the integration script)

## API Compatibility

This integration uses LM Studio's OpenAI-compatible API, supporting:
- Chat completions
- Model listing
- Standard OpenAI parameters (temperature, max_tokens, etc.)

## Security Notes

- The integration runs locally and doesn't send data to external servers
- Only the placeholder API key "lm-studio" is used
- All communication is over HTTP on localhost