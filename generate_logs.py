"""
Data Generator for Manufacturing Logs
Generates simulated sensor data with historical failure status for ML training.

Development Note: Created with AI assistance (Gemini/GitHub Copilot) for rapid prototyping.
"""

import csv
import random
from datetime import datetime, timedelta

# Configuration
NUM_RECORDS = 5000
FAILURE_RATE = 0.05  # 5% failure records
OUTPUT_FILE = "raw_manufacturing_logs.csv"

# Normal operating ranges
NORMAL_TEMP_RANGE = (65, 85)  # Celsius
NORMAL_VIBRATION_RANGE = (0.5, 2.5)  # arbitrary units

# Failure condition thresholds
FAILURE_TEMP_MIN = 95
FAILURE_VIBRATION_MIN = 4.0


def generate_timestamp(index):
    """Generate sequential timestamps starting from 30 days ago."""
    base_time = datetime.now() - timedelta(days=30)
    return (base_time + timedelta(minutes=index * 10)).strftime("%Y-%m-%d %H:%M:%S")


def generate_record(index, is_failure=False):
    """Generate a single manufacturing log record."""
    timestamp = generate_timestamp(index)
    serial_number = f"SN-{10000 + index:06d}"
    
    if is_failure:
        # Generate high-risk readings for failure cases
        component_temp_c = random.uniform(FAILURE_TEMP_MIN, FAILURE_TEMP_MIN + 15)
        vibration_level = random.uniform(FAILURE_VIBRATION_MIN, FAILURE_VIBRATION_MIN + 2)
        historical_failure_status = 1
    else:
        # Generate normal readings
        component_temp_c = random.uniform(*NORMAL_TEMP_RANGE)
        vibration_level = random.uniform(*NORMAL_VIBRATION_RANGE)
        historical_failure_status = 0
    
    return {
        "timestamp": timestamp,
        "serial_number": serial_number,
        "vibration_level": round(vibration_level, 2),
        "component_temp_C": round(component_temp_c, 1),
        "historical_failure_status": historical_failure_status
    }


def main():
    """Generate manufacturing logs CSV file."""
    # Determine which records will be failures
    num_failures = int(NUM_RECORDS * FAILURE_RATE)
    failure_indices = set(random.sample(range(NUM_RECORDS), num_failures))
    
    # Generate records
    records = []
    for i in range(NUM_RECORDS):
        is_failure = i in failure_indices
        records.append(generate_record(i, is_failure))
    
    # Write to CSV
    fieldnames = ["timestamp", "serial_number", "vibration_level", 
                  "component_temp_C", "historical_failure_status"]
    
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    # Summary output only (cost control: minimal printing)
    print(f"✓ Successfully generated {NUM_RECORDS} records")
    print(f"✓ Failure records: {num_failures} ({FAILURE_RATE * 100}%)")
    print(f"✓ Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
