import sys
import os

# Set dummy env vars for verification
os.environ["SECRET_KEY"] = "supersecretkey"
os.environ["DATABASE_URL"] = "postgresql://user:password@localhost/dbname"

# Add current directory to path
sys.path.append(os.getcwd())

try:
    print("Attempting to import app.main...")
    from app import main
    print("Successfully imported app.main")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

try:
    print("Attempting to import app.models.query_model...")
    from app.models import query_model
    print("Successfully imported app.models.query_model")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

print("All imports successful!")
