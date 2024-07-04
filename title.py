import pygetwindow as gw

# Function to sanitize window titles by removing non-ASCII characters
def sanitize_title(title):
    return ''.join(char if ord(char) < 128 else '?' for char in title)

# Get a list of all open windows
windows = gw.getAllTitles()

# Print the titles of all open windows
for i, title in enumerate(windows):
    sanitized_title = sanitize_title(title)
    print(f"{i + 1}: {sanitized_title}")
