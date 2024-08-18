"""
State manager for the status and state of the bot
"""

STATE = 1

def stop_state():
    STATE = 0

def restart_state():
    STATE = 1