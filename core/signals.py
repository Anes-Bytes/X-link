from django.dispatch import Signal

# Signal sent when a new user is registered via custom signup view
user_registered = Signal()
