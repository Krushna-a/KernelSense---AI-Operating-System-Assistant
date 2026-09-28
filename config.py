"""
Configuration settings for KernelSense
Customize behavior and limits here
"""

# System Information Settings
SYSTEM_INFO = {
    'cpu_check_interval': 1,  # seconds to measure CPU usage
    'process_limit_default': 10,  # default number of processes to show
    'process_limit_max': 50,  # maximum processes to list
}

# File Operations Settings
FILE_OPERATIONS = {
    'search_limit': 50,  # maximum files to find
    'search_max_files': 100,  # maximum files to scan for content search
    'content_search_result_limit': 50,  # maximum content search results
    'default_search_extensions': ['.txt', '.log', '.md'],  # default file types for content search
}

# Security Settings
SECURITY = {
    'require_approval_for_high_risk': True,
    'require_approval_for_critical': True,
    'log_all_operations': True,
    'show_risk_warnings': True,
}

# Critical Processes (additional to default list)
# Add processes that should be treated as critical for your system
ADDITIONAL_CRITICAL_PROCESSES = [
    # Add custom critical processes here
    # Example: 'my_critical_app.exe'
]

# Logging Settings
LOGGING = {
    'log_directory': 'logs',
    'enable_text_log': True,
    'enable_json_log': True,
    'log_user_input': True,
    'log_errors': True,
}

# CLI Settings
CLI = {
    'show_confidence_warning': True,  # show warning when confidence is low
    'confidence_threshold': 0.5,  # minimum confidence to consider valid
    'show_session_stats': True,  # show stats on exit
    'enable_colors': True,  # enable colored output
}

# Display Settings
DISPLAY = {
    'max_message_length': 5000,  # truncate very long messages
    'show_timestamps': False,  # show timestamps in CLI output
    'verbose_mode': False,  # show detailed execution information
}

# Performance Settings
PERFORMANCE = {
    'cache_system_info': False,  # cache system info for repeated calls
    'cache_ttl_seconds': 5,  # how long to cache (if enabled)
}

# Feature Flags
FEATURES = {
    'enable_file_deletion': True,  # allow file deletion operations
    'enable_process_killing': True,  # allow process termination
    'enable_file_search': True,  # allow file searching
    'enable_content_search': True,  # allow content searching
    'enable_startup_apps': True,  # allow startup app listing
}

# Default Values
DEFAULTS = {
    'sort_by': 'memory',  # default sort for process list (memory or cpu)
    'search_path': None,  # None = current directory
}
