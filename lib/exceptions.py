class ChartConfigValidationError(KeyError):
    def __str__(self):
        return "Missing 'name', 'type', or 'streams' field in chart configuration."
