# Security Notes

## Network input handling

The collector reads untrusted content from public sources. Treat every line as untrusted input.

Recommended safeguards:

- never run `eval` or `exec` on fetched content;
- never pass fetched content to a shell command;
- enforce request timeouts;
- limit response size before parsing in future fetcher improvements;
- keep parser and network validation separate;
- avoid exposing secrets to pull requests from forks.

## Static validation

`src/core/static_validator.py` provides a non-network validation layer for host, port, and private/reserved IP checks. It is safe to use in tests and future pipelines because it does not make outbound requests.

## Sensitive metadata

Metadata should not include tokens, private keys, passwords beyond the original public raw config, personal data, or private source URLs.
