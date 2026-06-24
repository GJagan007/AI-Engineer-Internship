# AI Compiler System

A production-ready system that converts natural language requirements into executable application configurations using a multi-stage pipeline.

## Features

- **Multi-Stage Pipeline**: Intent Extraction → System Design → Schema Generation → Refinement
- **Validation & Repair**: Automatic detection and fixing of inconsistencies
- **Execution Awareness**: Simulates runtime execution and validates configuration
- **Professional UI**: Dark/Light theme, tabbed interface, real-time progress
- **Metrics Dashboard**: Track success rate, latency, retries, and repairs
- **Production Ready**: Modular architecture, proper error handling, logging

## Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API Key (optional - mock mode works without)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-compiler-system.git
cd ai-compiler-system

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
```bash
pip install -r requirements.txt

4. Copy environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
