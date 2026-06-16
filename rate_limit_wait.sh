#!/bin/bash
# Circuit breaker: wait when rate limited
DELAY="${RATE_LIMIT_WAIT_SECONDS:-60}"
echo "Rate limit hit. Waiting ${DELAY}s..."
sleep "$DELAY"
