# AI Compiler System

A powerful system that converts natural language requirements into complete, validated application configurations. Just describe your app idea, and the system generates all the technical specifications.

## What It Does

Input: Plain English description of your application idea

Example: "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments"

Output: Complete technical specification including:
- UI Schema - Pages, components, layouts
- API Schema - Endpoints, methods, validation rules
- Database Schema - Tables, columns, relationships
- Auth System - Roles, permissions, access rules

## Features

- Multi-Stage Pipeline - Intent Extraction -> System Design -> Schema Generation -> Refinement
- Smart Validation - Auto-detects and fixes inconsistencies
- Execution Simulation - Shows how your app would run
- Professional Dashboard - Clean UI with dark/light theme
- Real-time Metrics - Tracks success rate, latency, repairs
- No API Key Required - Works out of the box

## Installation

Step 1: Create virtual environment
python -m venv venv

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

Step 2: Install dependencies
pip install -r requirements.txt

Step 3: Run the application
python backend/app.py

Step 4: Open in browser
http://localhost:5000

## How to Use

1. Enter your application requirements in plain English
2. Click "Compile" or press Ctrl+Enter
3. View the complete configuration in the Output tab
4. Check Execution tab for validation results
5. Monitor performance in the Metrics tab

Example Prompts:
- "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments"
- "Create an e-commerce store with product catalog, shopping cart, and user reviews"
- "Build a project management tool with task boards, team collaboration, and file sharing"

## How It Works

The system uses a 5-stage pipeline:
1. Intent Extraction - Understands your requirements
2. System Design - Creates application architecture
3. Schema Generation - Builds UI, API, DB, and Auth schemas
4. Validation and Repair - Checks consistency and fixes issues
5. Execution Simulation - Validates the configuration works

## Built With

Python 3.10+ - Backend runtime

Flask - Web framework

JavaScript - Frontend dashboard

HTML/CSS - User interface with dark/light theme

## License

MIT License
