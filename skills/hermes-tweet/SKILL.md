---
name: hermes-tweet
description: Use Hermes Tweet for X/Twitter monitoring, account research, trend checks, and approval-gated social actions through the native Hermes Agent plugin.
---

# Hermes Tweet

Use this skill when a user wants X/Twitter research, monitoring, trend checks, or social actions through Hermes Agent.

Hermes Tweet source: https://github.com/Xquik-dev/hermes-tweet

Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.

## Setup

Install and enable the native Hermes Agent plugin:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Set `XQUIK_API_KEY` before calling read tools. Keep credentials in the user's local secret store or runtime environment, not in prompts, logs, or shared files.

Enable public or private actions only when the user explicitly requests them:

```bash
export HERMES_TWEET_ENABLE_ACTIONS=true
```

## Workflow

1. Prefer `tweet_explore` first for local planning, intent clarification, and query design.
2. Use `tweet_read` for X/Twitter account research, tweet lookup, timeline checks, search, trends, and monitoring inputs.
3. Summarize evidence with links, IDs, timestamps, and uncertainty before recommending an action.
4. Treat every `tweet_action` call and private endpoint as sensitive.
5. Require `HERMES_TWEET_ENABLE_ACTIONS=true` and explicit user approval before posting, replying, following, liking, retweeting, reading private data, sending DMs, changing media or profile state, creating monitors, sending webhooks, or starting extraction jobs.
6. Stop and ask the user when a request could publish content, alter an account, expose private data, or create persistent monitoring.

## Safety Rules

- Never invent tweet IDs, account handles, metrics, or URLs.
- Never repeat API keys, cookies, tokens, or private account data.
- Ask before any `tweet_action`, private read, public action, or account change.
- Do not bypass the plugin's `XQUIK_API_KEY` or `HERMES_TWEET_ENABLE_ACTIONS` gates.
- Use dry-run wording for drafts until the user approves the exact public action.

## Example Requests

- "Check recent posts from this account and summarize the themes."
- "Monitor this keyword and report notable spikes."
- "Draft a reply, but do not post it yet."
- "After I approve, publish this tweet through Hermes Tweet."
