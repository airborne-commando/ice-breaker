import os
import sys
import hashlib
import shutil
import time
import concurrent.futures
from pathlib import Path
import threading
import random
import signal

# Function to clean up and exit
def cleanup(signum, frame):
    print("\nInterrupt received, stopping all processes...")
    stop_event.set()  # notify all threads
    if 'executor' in globals():
        executor.shutdown(wait=False, cancel_futures=True)
    if 'output_path' in globals() and output_path.exists():
        output_path.unlink()
    sys.exit(1)

# Function to display usage
def usage():
    print(f"Usage: {sys.argv[0]} [Optional: first name] [Optional: full name] [Optional: email domain] [Optional: search directories or file...]")
    print(f"       {sys.argv[0]} /? (Display help)")
    print(f"       {sys.argv[0]} --file <search_terms_file> [Optional: search directories or file...]")
    print(f"       {sys.argv[0]} --single-file <file_to_search> [Optional: search terms or --file <search_terms_file>]")
    print(f"Example 1: {sys.argv[0]} 'Fiona' 'Fiona Scott' 'outlook.com' /path/to/your/data/")
    print(f"Example 2: {sys.argv[0]} 'Fiona' /path/to/your/data/")
    print(f"Example 3: {sys.argv[0]} 'outlook' /path/to/your/data/")
    print(f"Example 4: {sys.argv[0]} --file search_terms.txt /path/to/your/data/")
    print(f"Example 5: {sys.argv[0]} --single-file large_file.txt 'Fiona' 'outlook.com'")
    print(f"Example 6: {sys.argv[0]} --single-file large_file.txt --file search_terms.txt")
    print(f"Example 7: {sys.argv[0]} 'gmail' large_file.txt")
    sys.exit(1)

# Function to search for text in files and return matching lines
def search_file(file_path, search_terms):
    if stop_event.is_set():  # bail out if stopping
        return None, []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            matching_lines = []
            for line in file:
                if stop_event.is_set():  # check mid-file read
                    return None, []
                if all(term.lower() in line.lower() for term in search_terms):
                    matching_lines.append(line.strip())
            if matching_lines:
                return file_path, matching_lines
    except Exception as e:
        if not stop_event.is_set():
            print(f"Error reading {file_path}: {e}")
    return None, []

# Function to index files (updated to avoid duplicates)
def index_directory(directory, index_file):
    # Read existing index entries to avoid duplicates
    existing_entries = set()
    if index_file.exists():
        with open(index_file, "r") as index:
            existing_entries = set(line.strip() for line in index)

    # Write unique entries to the index file
    with open(index_file, "w") as index:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in existing_entries:
                    index.write(f"{file_path}\n")
                    existing_entries.add(file_path)

# Function to check if cache is valid based on TTL
def is_cache_valid(cache_file):
    if not cache_file.exists():
        return False, 0, 0
    with open(cache_file, "r") as file:
        try:
            # Read the first line (timestamp|ttl)
            timestamp, ttl = file.readline().strip().split("|")
            timestamp = float(timestamp)
            ttl = float(ttl)
            remaining_time = ttl - (time.time() - timestamp)
            return remaining_time > 0, remaining_time, ttl
        except ValueError:
            return False, 0, 0

# Function to format time in human-readable format (e.g., "1 hour and 30 minutes")
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    time_parts = []
    if hours > 0:
        time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0 and hours == 0:  # Only show seconds if no hours
        time_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    return " and ".join(time_parts)

# Function to parse human-readable time input (e.g., "5 minutes", "1 hour", "30 seconds", "1h", "30m", "15s")
def parse_ttl_input(ttl_input):
    try:
        # Handle shorthand inputs (e.g., "1h", "30m", "15s")
        if ttl_input.endswith("h"):
            return int(ttl_input[:-1]) * 3600
        elif ttl_input.endswith("m"):
            return int(ttl_input[:-1]) * 60
        elif ttl_input.endswith("s"):
            return int(ttl_input[:-1])
        else:
            # Handle full words (e.g., "1 hour", "30 minutes", "15 seconds")
            parts = ttl_input.strip().split()
            if len(parts) != 2:
                raise ValueError("Invalid format")
            
            value = int(parts[0])
            unit = parts[1].lower()

            # Convert to seconds based on unit
            if unit in ["second", "seconds", "s"]:
                return value
            elif unit in ["minute", "minutes", "m"]:
                return value * 60
            elif unit in ["hour", "hours", "h"]:
                return value * 3600
            else:
                raise ValueError("Unknown unit")
    except (ValueError, IndexError):
        return None

# Function to display a binary-style animation
def binary_animation(stop_event):
    chars = "01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"
    while not stop_event.is_set():
        # Generate a random line of 15 characters
        random_line = "".join(random.choice(chars) for _ in range(15))
        sys.stdout.write(f"\r{random_line}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 15 + "\r")  # Clear the animation line

# Function to read search terms from a file
def read_search_terms_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error reading search terms file: {e}")
        sys.exit(1)

# Function to parse TLDs from user input
def parse_tlds(tld_input):
    tlds = []
    if tld_input:
        tlds = [tld.strip() for tld in tld_input.replace(",", " ").split() if tld.strip()]
    return tlds

# Main script
if __name__ == "__main__":
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, cleanup)

    # Check if no arguments are provided (only the script name is present)
    if len(sys.argv) == 1:
        usage()

    # Check for help command
    if "/?" in sys.argv or "--help" in sys.argv:
        usage()

    # Initialize variables
    first_name = None
    full_name = None
    email_domain = None
    directories = []
    search_terms = []
    use_tlds = True  # Default to asking about TLDs
    single_file_mode = False
    file_to_search = None

    # Check if we're in single file mode
    if "--single-file" in sys.argv:
        try:
            file_index = sys.argv.index("--single-file")
            file_to_search = sys.argv[file_index + 1]
            if not os.path.isfile(file_to_search):
                print(f"Error: File {file_to_search} does not exist or is not a file.")
                sys.exit(1)
            single_file_mode = True
        except IndexError:
            print("Error: No file specified after --single-file")
            usage()

    # Check for search terms file (can be used with or without --single-file)
    if "--file" in sys.argv:
        try:
            file_index = sys.argv.index("--file")
            search_terms_file = sys.argv[file_index + 1]
            search_terms = read_search_terms_from_file(search_terms_file)
            use_tlds = False  # Skip TLD prompt if using a file
            
            # If not in single file mode, get directories from remaining args
            if not single_file_mode:
                directories = sys.argv[file_index + 2:]
        except IndexError:
            print("Error: No search terms file provided.")
            usage()
    else:
        # Parse arguments (only if we're not using --file)
        remaining_args = sys.argv[1:]
        if single_file_mode:
            # Skip the --single-file and file path arguments
            remaining_args = sys.argv[sys.argv.index("--single-file") + 2:]
        
        for arg in remaining_args:
            if " " in arg:  # Full name
                full_name = arg
            elif "@" in arg:  # Email domain
                email_domain = arg
            elif os.path.isdir(arg):  # Directory
                directories.append(arg)
            elif os.path.isfile(arg) and not single_file_mode:  # Single file (if not already in single file mode)
                file_to_search = arg
                single_file_mode = True
            else:  # First name or other search term
                first_name = arg

        # If no arguments are provided, default to help
        if not first_name and not full_name and not email_domain and not directories and not single_file_mode:
            usage()

        # Build search terms
        if first_name:
            search_terms.append(first_name)
        if full_name:
            search_terms.append(full_name)
        if email_domain:
            search_terms.append(email_domain)

    # If in single file mode and no search terms were provided via arguments or --file, prompt for them
    if single_file_mode and not search_terms:
        search_input = input("Enter search terms separated by spaces: ").strip()
        if search_input:
            search_terms = search_input.split()

    # If no directories are provided and not in single file mode, use the current directory
    if not directories and not single_file_mode:
        directories = ["."]

    # Check if the directories exist
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Error: Directory {directory} does not exist.")
            sys.exit(1)

    # Ask the user if they want to search for specific TLDs (unless using a file or in single file mode)
    tlds = []
    if use_tlds and not single_file_mode:
        while True:
            tld_prompt = input("Do you want to search for specific TLDs (e.g., .gov, .edu, .mil)? (y/n): ").strip().lower()
            if tld_prompt in ["y", "n"]:
                break
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

        if tld_prompt == 'y':
            tld_input = input("Enter the TLDs you want to search for, separated by commas or spaces (e.g., .gov, .edu, .mil): ").strip()
            tlds = parse_tlds(tld_input)

    # Add TLDs to search terms
    if tlds:
        search_terms.extend(tlds)

    # Use a fixed directory instead of the PyInstaller temp directory
    persistent_dir = Path.home() / "icebrkr_data"
    text_dir = persistent_dir / "text"
    cache_dir = persistent_dir / "cache"
    index_dir = persistent_dir / "index"

    # Ensure directories exist
    text_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)

    # Output file paths
    output_path = text_dir / "output.txt"
    index_file = index_dir / "index.txt"

    # Generate cache key based on search terms and file path (if in single file mode)
    if single_file_mode:
        cache_key = hashlib.md5(("_".join(search_terms) + file_to_search).encode()).hexdigest()
    else:
        cache_key = hashlib.md5("_".join(search_terms).encode()).hexdigest()
    cache_file = cache_dir / f"{cache_key}.cache"

    # Set TTL (Time to Live) for cache (default: 1 hour = 3600 seconds)
    ttl = 3600  # Default TTL in seconds
    default_ttl_human = format_time(ttl)  # Convert default TTL to human-readable format
    ttl_prompt = input(f"Enter the TTL (Time to Live) for cache (e.g., '1h', '30m', '15s', default: {default_ttl_human}): ").strip()
    if ttl_prompt:
        parsed_ttl = parse_ttl_input(ttl_prompt)
        if parsed_ttl is not None:
            ttl = parsed_ttl
        else:
            print("Invalid TTL format. Using default value.")

    # Check if cache is valid
    is_valid, remaining_time, cache_ttl = is_cache_valid(cache_file)
    if is_valid and cache_ttl == ttl:  # Ensure the TTL matches the user's setting
        remaining_time_human = format_time(remaining_time)  # Convert remaining time to human-readable format
        print(f"Cache found and is valid for {remaining_time_human}. Using cached results.")
        shutil.copy(cache_file, output_path)
        print(f"Results retrieved from cache and saved to {output_path}")
    else:
        if cache_file.exists():
            print("Cache expired. Deleting old cache...")
            cache_file.unlink()  # Delete the expired cache file

        print("No valid cache found. Performing search...")

        # Start the binary-style animation
        stop_event = threading.Event()
        animation_thread = threading.Thread(target=binary_animation, args=(stop_event,))
        animation_thread.start()

        matching_results = []

        if single_file_mode:
            # Single file search mode
            file_path, matching_lines = search_file(file_to_search, search_terms)
            if matching_lines:
                matching_results.append((file_path, matching_lines))
        else:
            # Directory search mode
            # Use ThreadPoolExecutor for parallel processing
            with concurrent.futures.ThreadPoolExecutor() as executor:
                globals()['executor'] = executor  # so cleanup() can access it
                futures = []
                for directory in directories:
                    index_directory(directory, index_file)
                    for root, _, files in os.walk(directory):
                        for file in files:
                            if stop_event.is_set():
                                break
                            file_path = Path(root) / file
                            futures.append(executor.submit(search_file, file_path, search_terms))

                for future in concurrent.futures.as_completed(futures):
                    if stop_event.is_set():
                        break
                    file_path, matching_lines = future.result()
                    if matching_lines:
                        matching_results.append((file_path, matching_lines))

        # Stop the animation
        stop_event.set()
        animation_thread.join()

        # Save results to the output file
        with open(output_path, "w") as output:
            # Write the current timestamp and TTL as the first line
            output.write(f"{time.time()}|{ttl}\n")
            for file_path, matching_lines in matching_results:
                output.write(f"File: {file_path}\n")
                for line in matching_lines:
                    output.write(f"{line}\n")
                output.write("\n")

        # Cache the results
        shutil.copy(output_path, cache_file)
        print(f"Search results saved to {output_path}")
        print(f"Results cached in {cache_file}")
        if not single_file_mode:
            print(f"Index saved to {index_file}")

    # Print the results from the output file
    print("\nSearch Results:")
    with open(output_path, "r") as file:
        print(file.read())
