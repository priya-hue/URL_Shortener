from datetime import datetime
import threading

# database
url_map = {}

# Thread safety lock
lock = threading.Lock()
