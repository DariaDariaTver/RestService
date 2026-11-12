ALLOWED_TRANSITIONS = {
    "new": ["confirmed", "cancelled"],
    "confirmed": ["preparing", "cancelled"],
    "preparing": ["delivering", "cancelled"],
    "delivering": ["completed"],
    "completed": [],
    "cancelled": []
}