# Draft claims log — python logging / Sentry (AUG-8 SHAPE, SYNTHETIC)

## Key claims log

| Claim | Status | Source(s) |
|---|---|---|
| Handlers attach to loggers and propagate to ancestors by default | verified | [python docs](https://docs.python.org/3/library/logging.html), [pilosus](https://blog.pilosus.org/posts/2020/01/24/python-logging/) |
| Sentry's Python SDK installs a logging integration by default | single-source | [sentry docs](https://docs.sentry.io/platforms/python/) |
| OTel log records carry a severity number distinct from severity text | single-source | [otel](https://opentelemetry.io/docs/specs/otel/logs/) |

## Source shelf

- [python docs](https://docs.python.org/3/library/logging.html) — stdlib reference **(read)**
- [pilosus](https://blog.pilosus.org/posts/2020/01/24/python-logging/) — practitioner writeup **(read)**
- [sentry docs](https://docs.sentry.io/platforms/python/) — SDK reference **(read)**
- [otel](https://opentelemetry.io/docs/specs/otel/logs/) — spec **(read)**
