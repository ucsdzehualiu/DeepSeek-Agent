# DeepSeek AI Agent

## Overview
DeepSeek AI Agent is an intelligent assistant powered by the **DeepSeek 70B LLaMA model**, deployed using **Ollama**. It integrates **Tavily** as a search tool to enhance real-time information retrieval.

## Features
- **Real-time Search**: Integrates Tavily for fetching up-to-date information from the web.
- **Flexible Deployment**: Runs locally or on cloud platforms using Ollama.

## Installation
### Prerequisites
Ensure you have the following installed:
- [Ollama](https://ollama.com/) (for deploying DeepSeek 70B)
- Python 3.10+
- `pip` (Python package manager)

### Steps


1. **Start the Ollama server and load DeepSeek 70B**
   ```bash
   ollama pull deepseek-70b
   ollama serve
   ```

2. **Run the AI Agent**
   ```bash
   python agent.py
   ```

## Usage
- Send queries to the AI agent.
- It will generate responses using DeepSeek 70B.
- When required, it will fetch real-time information using Tavily.

## Configuration
You can customize API keys and parameters in the `tool.py` file:
```env
TAVILY_API_KEY=your_api_key_here
```

## License
This project is open-source under the [MIT License](LICENSE).

## Contributions
Pull requests are welcome! Please follow the standard guidelines for contributing.

