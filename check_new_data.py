import os
import json

# Path to the dataset directory
dataset_dir = 'dataset/'  # Update with your actual dataset directory

# Path to the file that stores the previous count
previous_count_file = 'previous_count.txt'

# Threshold for the number of new files that trigger a training session
threshold = 10

def get_current_data_count():
    """Count the number of files in the dataset directory."""
    return len([f for f in os.listdir(dataset_dir) if os.path.isfile(os.path.join(dataset_dir, f))])

def get_previous_data_count():
    """Read the previous data count from the file."""
    if os.path.exists(previous_count_file):
        with open(previous_count_file, 'r') as file:
            return int(file.read().strip())
    return 0

def update_previous_data_count(new_count):
    """Update the previous data count in the file."""
    with open(previous_count_file, 'w') as file:
        file.write(str(new_count))

def verify_annotations():
    """Verify the presence of part numbers and values in the training data."""
    for filename in os.listdir(dataset_dir):
        if filename.endswith(".json"):
            with open(os.path.join(dataset_dir, filename), 'r') as file:
                data = json.load(file)
                for component in data.get('components', []):
                    if 'partNumber' not in component or 'value' not in component:
                        return False
    return True

def check_metadata_consistency():
    """Check the consistency and completeness of metadata files."""
    for filename in os.listdir(dataset_dir):
        if filename.endswith(".json"):
            with open(os.path.join(dataset_dir, filename), 'r') as file:
                data = json.load(file)
                if 'image_path' not in data or 'description' not in data or 'components' not in data:
                    return False
                for component in data['components']:
                    if 'type' not in component or 'coordinates' not in component:
                        return False
    return True

if __name__ == "__main__":
    current_count = get_current_data_count()
    previous_count = get_previous_data_count()

    new_files_count = current_count - previous_count

    if new_files_count >= threshold and verify_annotations() and check_metadata_consistency():
        print(f"New files detected: {new_files_count}, triggering training.")
        update_previous_data_count(current_count)
        exit(0)  # Exit with status 0 to trigger training
    else:
        print(f"Only {new_files_count} new files or annotations/metadata missing, training not triggered.")
        exit(1)  # Exit with status 1 to skip training
