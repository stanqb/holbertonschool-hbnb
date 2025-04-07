#!/usr/bin/env python3
"""
Utility script to generate UUID4 values for SQL scripts
"""

import uuid


def generate_uuid():
    """Generate a UUID4 string"""
    return str(uuid.uuid4())


if __name__ == "__main__":
    # Generate and print a UUID
    print(f"Generated UUID: {generate_uuid()}")

    # Generate multiple UUIDs
    print("\nMultiple UUIDs:")
    for i in range(5):
        print(f"{i+1}. {generate_uuid()}")
