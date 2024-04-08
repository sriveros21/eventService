import sys
print("\n".join(sys.path))

import os

# Print all environment variables
for key, value in os.environ.items():
    print(f"{key}: {value}")