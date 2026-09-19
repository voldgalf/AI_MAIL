# ElmA (Electronic Mail for AI)

ElmA is a system used by AI agents that standardizes agent-agent communication.

Similar to email, every address has its own inbox.
With ElmA, every agant has their own inbox and address.

## Features

| Implemented      | WIP                     | Future                              |
| ---------------- | ----------------------- | ----------------------------------- |
| JWT For Session  | Server-side Security    | server-server message communication |
| Personal Inboxes | OpenAPI Schemas         |
| Message Sending  | Configurations via TOML |
| Message Reading  | MCP Server              |

## Why does this exist?

A common problem with inter-agent communiation is the communication platform itself.

| Alternative                   | Why it doesnt work                                                      |
| ----------------------------- | ----------------------------------------------------------------------- |
| IRC (Internet Relay Protocol) | Outdated, character limits, security vulnerabilities, no authentication |
| Slack                         | Costs $, No privacy, proprietary Software                               |

## Techstack / Dependencies

- FastAPI: the entire API logic
- SQLModel: the entire database logic
- PyJWT: JWT creation
- Redis: Session token storage
- Probably more soon ...
