#!/usr/bin/env python3

import os
import subprocess
import sys
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Constants
VERSIONS = ["5", "7", "8"]
LOG_FILENAME = "failed.log"
SUMMARY_FILENAME = "summary.txt"
SKIP_DIRECTORY = "skip"
COMMON_SKIP_FILE = "common.txt"
COMMON_LIST = os.path.join(SKIP_DIRECTORY, COMMON_SKIP_FILE)

# Default values are used if environment variables are unset
# Note: No username/password required for MaxScale test
MONGO_HOST = os.environ.get("MONGO_HOST", "127.0.0.1")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_USERNAME = os.environ.get("MONGO_USERNAME", "admin")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "password")
AUTHENTICATION_DATABASE = os.environ.get("AUTHENTICATION_DATABASE", "admin")
AUTHENTICATION_MECHANISM = os.environ.get("AUTHENTICATION_MECHANISM", "SCRAM-SHA-1")
USE_SSL = os.environ.get("USE_SSL", "false")
LOAD_BALANCE = os.environ.get("LOAD_BALANCE", "false")
TEST_DIRECTORY = os.environ.get("TEST_DIRECTORY", os.path.join(os.getcwd(), "mongo/jstests"))
LOG_DIRECTORY = os.environ.get("LOG_DIRECTORY", "logs")

if MONGO_USERNAME and MONGO_PASSWORD:
    creds = f"{MONGO_USERNAME}:{MONGO_PASSWORD}@"
    auth_part = f"?authMechanism={AUTHENTICATION_MECHANISM}&authSource={AUTHENTICATION_DATABASE}&ssl={USE_SSL}&loadBalanced={LOAD_BALANCE}"
else:
    creds, auth_part = "", ""


# Check if MongoDB version is valid.
def is_valid_version(version):
    return version in VERSIONS


# Ensure the existence of skip lists.
def check_list_existence(file_path, file_description):
    if not os.path.exists(file_path):
        print(f"\033[91m{file_description} not found\033[0m")
        sys.exit(1)


# Validate MongoDB connectivity and credentials.
def validate_connection(uri):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client[AUTHENTICATION_DATABASE].command("ping")
        print("Connected successfully to database")

    except ConnectionFailure:
        print("\033[91mFailed to connect to database\033[0m")
        sys.exit(1)

    except OperationFailure:
        print("\033[91mAuthentication failed for database\033[0m")
        sys.exit(1)


# Create MongoDB URI from user variables.
def create_mongo_uri():
    return f"mongodb://{creds}{MONGO_HOST}:{MONGO_PORT}/{auth_part}"


# Build the mongo command with the necessary arguments.
def build_mongo_command(script_path):
    mongo_command = ["mongo", f"mongodb://{creds}{MONGO_HOST}:{MONGO_PORT}/{auth_part}"]
    mongo_command.append(script_path)
    return mongo_command


# Run an individual script using subprocess.
def run_script(script_path):
    mongo_command = build_mongo_command(script_path)
    # print(mongo_command)
    try:
        subprocess.run(
            mongo_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,  # Set timeout to 60 seconds
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False


# Find all JS files that are not in the exclusion lists.
def find_js_files(directory, mongo_version):
    exclusions = set()
    with open(COMMON_LIST, "r") as f:
        exclusions.update([TEST_DIRECTORY + line.strip() for line in f])

    # Add specific mongo version exclusions.
    mongo_exclusions = f"{SKIP_DIRECTORY}/mongo{mongo_version}.txt"
    check_list_existence(mongo_exclusions, mongo_exclusions)
    with open(mongo_exclusions, "r") as f:
        exclusions.update([TEST_DIRECTORY + line.strip() for line in f])

    js_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".js"):
                full_path = os.path.join(root, file)
                if full_path not in exclusions:
                    js_files.append(full_path)

    if not js_files:
        print(f"No JS files found in {directory}")
        sys.exit(1)

    return js_files


# Main function.
if __name__ == "__main__":
    start_time = time.time()
    # Ensure there is at least one argument provided and it's valid
    if len(sys.argv) < 2 or not is_valid_version(sys.argv[1]):
        print("You must choose a MongoDB server version to compare against (5, 7 or 8)")
        print(f"Example usage: python3 {sys.argv[0]} 5")
        sys.exit(1)

    version = sys.argv[1]
    os.makedirs(LOG_DIRECTORY, exist_ok=True)
    mongo_list = os.path.join(SKIP_DIRECTORY, f"mongo{version}.txt")
    uri = create_mongo_uri()

    validate_connection(uri)

    script_files = sorted(find_js_files(TEST_DIRECTORY, version))
    total_scripts = len(script_files)
    success_count = 0
    failed_scripts = []

    for idx, script_path in enumerate(script_files, start=1):
        filename = os.path.basename(script_path)

        script_start = time.time()  # Start time for the current script
        success = run_script(script_path)
        script_end = time.time()  # End time for the current script

        # Calculate elapsed time for this script
        elapsed_time = script_end - script_start

        if success:
            success_count += 1
            print(
                f"Passed test {idx}/{total_scripts}: {filename} (Time: {elapsed_time:.4f}s)"
            )
        else:
            print(
                "\033[91m"
                + f"Failed test {idx}/{total_scripts}: {filename} (Time: {elapsed_time:.4f}s)"
                + "\033[0m"
            )
            failed_scripts.append(script_path)

    end_time = time.time()
    total_time = end_time - start_time
    success_percentage = (
        (success_count / total_scripts) * 100 if total_scripts > 0 else 0
    )
    summary_log = (
        f"\nTotal Tests Attempted: {total_scripts}\n"
        f"Total Successful Executions: {success_count}\n"
        f"Percentage Successful: {success_percentage:.2f}%\n"
        f"Total Execution Time: {total_time:.2f} seconds\n"
    )
    print(summary_log)

    summary_file_path = os.path.join(LOG_DIRECTORY, SUMMARY_FILENAME)
    with open(summary_file_path, "w") as summary_file:
        summary_file.write(summary_log)
        print(f"Summary have been written to: {summary_file_path}")

    log_file_path = os.path.join(LOG_DIRECTORY, LOG_FILENAME)
    if failed_scripts:
        with open(log_file_path, "w") as log_file:
            for failed_script in failed_scripts:
                relative_path = os.path.relpath(failed_script, TEST_DIRECTORY)
                log_file.write(f"{relative_path}\n")
        print(f"Failed scripts have been logged to: {log_file_path}")
