def missing_variable_fallback(error: str, variables: dict) -> str:
    known = ", ".join(sorted(variables.keys())) if variables else "none"
    return (
        "I need one more detail to continue this request. "
        f"Known fields: {known}. "
        f"Template issue: {error}"
    )
