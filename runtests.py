#!/usr/bin/env python
"""
Test runner script for X-Link Django project.

This script sets up the Django environment and runs all tests.
"""
import os
import sys
import django

def run_tests():
    """Run all Django tests for the X-Link project."""
    # Add the project directory to the Python path
    sys.path.insert(0, os.path.dirname(__file__))

    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    # Import test modules to check for syntax errors
    try:
        import core.tests
        import cards.tests
        import Billing.tests
        import site_management.tests
        import core.test_utils
        print("✓ All test modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import test modules: {e}")
        return False

    # Run tests using Django's test runner
    from django.test.utils import get_runner
    from django.conf import settings

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    # Run all tests
    failures = test_runner.run_tests([
        "core.tests",
        "cards.tests",
        "Billing.tests",
        "site_management.tests",
    ])

    return failures == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
