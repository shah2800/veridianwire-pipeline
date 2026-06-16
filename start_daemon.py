#!/usr/bin/env python3
"""
Safe daemon startup script with dependency checks.
Verifies all requirements before starting the news daemon.
"""
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if all environment variables are set."""
    logger.info("Checking environment variables...")

    required_keys = [
        'GROQ_API_KEY',  # REQUIRED (free)
        'NEWSAPI_API_KEY',
        'SUPABASE_URL',
        'SUPABASE_SERVICE_KEY',
    ]

    optional_keys = [
        'OPENAI_API_KEY',  # OPTIONAL (can use free Groq instead)
    ]

    missing = []
    for key in required_keys:
        if not os.getenv(key):
            missing.append(key)

    if missing:
        logger.error(f"Missing REQUIRED environment variables: {', '.join(missing)}")
        logger.error("Please edit .env file and add these keys:")
        logger.error("  - GROQ_API_KEY (free): https://console.groq.com/keys")
        logger.error("  - NEWSAPI_API_KEY: https://newsapi.org/register")
        logger.error("  - SUPABASE_URL: https://supabase.com")
        logger.error("  - SUPABASE_SERVICE_KEY: (from Supabase project settings)")
        return False

    # Check optional keys
    for key in optional_keys:
        if not os.getenv(key):
            logger.warning(f"Optional key not set: {key} - using free Groq instead")

    logger.info("Environment variables OK")
    return True

def check_imports():
    """Check if all required modules can be imported."""
    logger.info("Checking Python imports...")

    modules = [
        'dotenv',
        'requests',
        'openai',
        'groq',
        'supabase',
        'feedparser',
    ]

    missing = []
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        logger.error(f"Missing Python modules: {', '.join(missing)}")
        logger.error("Run: pip install -r requirements.txt")
        return False

    logger.info("All Python imports OK")
    return True

def check_files():
    """Check if required files exist."""
    logger.info("Checking required files...")

    files = [
        '.env',
        'requirements.txt',
        'package.json',
    ]

    missing = []
    for f in files:
        if not Path(f).exists():
            missing.append(f)

    if missing:
        logger.error(f"Missing files: {', '.join(missing)}")
        return False

    logger.info("Required files OK")
    return True

def main():
    """Run pre-flight checks and start daemon."""
    logger.info("=" * 60)
    logger.info("Autonomous News Business Daemon - Pre-flight Check")
    logger.info("=" * 60)

    # Load .env
    from dotenv import load_dotenv
    load_dotenv()

    # Run checks
    checks = [
        ("Files", check_files),
        ("Environment", check_environment),
        ("Imports", check_imports),
    ]

    all_ok = True
    for name, check in checks:
        try:
            if not check():
                all_ok = False
        except Exception as e:
            logger.error(f"{name} check failed: {e}")
            all_ok = False

    if not all_ok:
        logger.error("\nFix the errors above and try again.")
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("All checks passed! Starting daemon...")
    logger.info("=" * 60)
    logger.info("Press Ctrl+C to stop")
    logger.info("")

    # Import and start daemon
    try:
        from daemon import NewsDaemon
        daemon = NewsDaemon()
        daemon.run()
    except Exception as e:
        logger.error(f"Failed to start daemon: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Daemon stopped by user")
        sys.exit(0)
