# Auto Reaction Telegram Bot

## Overview

This is a Telegram bot that automatically reacts to messages with random emojis. The bot is designed to add fun and engagement to group chats and private conversations by responding to every message with one of the supported Telegram reaction emojis. The bot uses the python-telegram-bot library and can be easily deployed to cloud platforms.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Technology**: Python with python-telegram-bot library (>=22.3)
- **Design Pattern**: Event-driven architecture using handlers
- **Rationale**: The python-telegram-bot library provides a robust, well-maintained framework for Telegram bot development with built-in support for webhooks, polling, and comprehensive API coverage.

### Message Processing
- **Handler Architecture**: Uses separate handlers for commands (/start) and general messages
- **Auto-reaction Logic**: Responds to all messages in any chat type (private, group, supergroup) with random emoji reactions
- **Emoji Management**: Maintains a curated list of Telegram-supported reaction emojis to ensure compatibility

### Deployment Architecture
- **Stateless Design**: No persistent data storage required - the bot operates purely on incoming message events
- **Environment Configuration**: Uses the `TELEGRAM_BOT_TOKEN` secret for bot authentication
- **Logging**: Structured logging for monitoring and debugging message processing
- **Mode**: Long polling (application.run_polling)

### User Interaction Flow
- **Onboarding**: /start command provides introduction and group invitation link
- **Core Functionality**: Automatic reactions to all incoming messages
- **Group Integration**: Inline keyboard button for easy group addition

## Replit Setup

### Workflow
- **Name**: Start application
- **Command**: `python main.py`
- **Output Type**: console (this is a bot, not a web server)

### Required Secrets
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather

## External Dependencies

### Core Dependencies
- **python-telegram-bot**: Primary framework for Telegram Bot API integration
- **Telegram Bot API**: Official Telegram service for bot communication

### Runtime Environment
- **Python 3.11**: Runtime environment
- **Environment Variables**: TELEGRAM_BOT_TOKEN for authentication
- **Logging Framework**: Python's built-in logging module for system monitoring
