from pybreaker import CircuitBreaker

auth_breaker = CircuitBreaker(
    fail_max=5, # Number of failures before opening the circuit
    reset_timeout=60 # Time in seconds before the circuit can be reset
    )