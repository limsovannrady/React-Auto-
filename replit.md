# Auto Reaction Telegram Bot

## Overview

This is a Telegram bot that automatically reacts to messages with random emojis. The bot is designed to add fun and engagement to group chats and private conversations by responding to every message with one of the supported Telegram reaction emojis. The bot uses the python-telegram-bot library and can be easily deployed to cloud platforms.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Technology**: Python with python-telegram-bot library
- **Design Pattern**: Event-driven architecture using handlers
- **Rationale**: The python-telegram-bot library provides a robust, well-maintained framework for Telegram bot development with built-in support for webhooks, polling, and comprehensive API coverage.

### Message Processing
- **Handler Architecture**: Uses separate handlers for commands (/start) and general messages
- **Auto-reaction Logic**: Responds to all messages in any chat type (private, group, supergroup) with random emoji reactions
- **Emoji Management**: Maintains a curated list of Telegram-supported reaction emojis to ensure compatibility

### Deployment Architecture
- **Stateless Design**: No persistent data storage required - the bot operates purely on incoming message events
- **Environment Configuration**: Uses environment variables for bot token configuration
- **Logging**: Structured logging for monitoring and debugging message processing

### User Interaction Flow
- **Onboarding**: /start command provides introduction and group invitation link
- **Core Functionality**: Automatic reactions to all incoming messages
- **Group Integration**: Inline keyboard button for easy group addition

## External Dependencies

### Core Dependencies
- **python-telegram-bot**: Primary framework for Telegram Bot API integration
- **Telegram Bot API**: Official Telegram service for bot communication

### Runtime Environment
- **Python 3.x**: Runtime environment
- **Environment Variables**: BOT_TOKEN for authentication
- **Logging Framework**: Python's built-in logging module for system monitoring

### Deployment Platforms
- **Cloud Hosting**: Designed for deployment on platforms like Replit, Heroku, or similar PaaS providers
- **Webhook Support**: Can be configured for webhook-based or polling-based message reception