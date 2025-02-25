# ICE BREAKER

Ice breaker is a tool designed to scan databases (leaked or simulated) with either a persons name or email

Name is based on the trait from [Deus Ex: GOTY](https://deusex.fandom.com/wiki/Computer_skill#Effects), was/is a fun little project :)

In order to generate names you'll need to download a name list [here](https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/fea1da1a3c4ce5c8e470f679a8e1bc741281a609/first-names.txt) and save as first-names.txt only or grab my [fork of that](https://gist.githubusercontent.com/airborne-commando/aa284cb7145b3c7c74881b39d4a679bc/raw/fea1da1a3c4ce5c8e470f679a8e1bc741281a609/first-names.txt) if missing.

to run the name gen do:

    python namegen.py

and input the file size.


Here’s a detailed discussion of the **changes made so far** to the script, including the new features and improvements:

---

### 1. **Search with a Text File**:
   - **What Changed**:
     - Added support for reading search terms from a **text file** using the `--file` option.
     - The script reads the file line by line and uses each non-empty line as a search term.
   - **Why It’s Useful**:
     - Users can now provide a list of search terms in a file, which is especially helpful for complex or repetitive searches.
     - This feature makes the script more flexible and user-friendly.
   - **Example**:
     - If `search_terms.txt` contains:
       ```
       Fiona
       outlook.com
       .gov
       ```
     - The script will search for all these terms in the specified directories.

---

### 2. **Help Command**:
   - **What Changed**:
     - Added a **help command** (`/?` or `--help`) to display usage instructions and examples.
     - The `usage()` function provides a clear explanation of how to use the script.
   - **Why It’s Useful**:
     - Users can quickly access help without needing to read external documentation.
     - The help command ensures users understand the script's capabilities and how to use it correctly.
   - **Example**:
     - Running `python ice-breaker.py /?` displays:
       ```
       Usage: ice-breaker.py [Optional: first name] [Optional: full name] [Optional: email domain] [Optional: search directories...]
              ice-breaker.py /? (Display help)
              ice-breaker.py --file <search_terms_file> [Optional: search directories...]
       Example 1: ice-breaker.py 'Fiona' 'Fiona Scott' 'outlook.com' /path/to/your/data/
       Example 2: ice-breaker.py 'Fiona' /path/to/your/data/
       Example 3: ice-breaker.py 'outlook.com' /path/to/your/data/
       Example 4: ice-breaker.py --file search_terms.txt /path/to/your/data/
       ```

---

### 3. **Time to Live (TTL) for Cache**:
   - **What Changed**:
     - Added support for a **TTL (Time to Live)** for cached results.
     - The user can specify the TTL in **human-readable format** (e.g., `1h`, `30m`, `15s`) or as full words (e.g., `1 hour`, `30 minutes`, `15 seconds`).
     - If the cache is expired, it is automatically **deleted**, and a new search is performed.
   - **Why It’s Useful**:
     - Ensures that cached results are not stale.
     - Provides flexibility for users to control how long cached results remain valid.
   - **Example**:
     - If the user sets the TTL to `30m`, the cache will be valid for 30 minutes. After that, it will be deleted, and a new search will be performed.

---

### 4. **Binary-Style Animation**:
   - **What Changed**:
     - Added a **binary-style animation** that runs while the search is being performed.
     - The animation uses random characters from the set `01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()`.
     - The animation is **15 characters long** and updates rapidly to simulate a "hacking" effect.
   - **Why It’s Useful**:
     - Provides visual feedback to the user while the script is working.
     - Adds a fun, retro-futuristic vibe to the script.
   - **Example**:
     - While searching, the console displays:
       ```
       aBcD1!@#kLmN&*()
       ```

---

### 5. **Cache Deletion on Expiry**:
   - **What Changed**:
     - If the cache is found but has expired, it is automatically **deleted**.
     - The script informs the user that the cache is expired and proceeds with a new search.
   - **Why It’s Useful**:
     - Ensures that outdated cache files do not linger and cause confusion.
     - Keeps the cache directory clean and up-to-date.
   - **Example**:
     - If the cache is expired, the script prints:
       ```
       Cache expired. Deleting old cache...
       No valid cache found. Performing search...
       ```

---

### 6. **Print Results**:
   - **What Changed**:
     - After the search is complete, the script **prints the results** from the output file to the console.
     - The results are displayed in a clean and readable format.
   - **Why It’s Useful**:
     - Allows users to immediately view the search results without opening the output file.
     - Provides a quick way to verify the results.
   - **Example**:
     - The script prints:
       ```
       Search Results:
       File: /path/to/file1.txt
       matching_line_1
       matching_line_2

       File: /path/to/file2.txt
       matching_line_3
       ```

---

### 7. **Threading for Animation**:
   - **What Changed**:
     - The animation runs in a **separate thread** while the search is being performed.
     - The animation thread is stopped once the search is complete.
   - **Why It’s Useful**:
     - Ensures that the animation does not block the main search process.
     - Provides a smooth user experience.
   - **Example**:
     - The animation runs in the background while the script searches files.

---

### 8. **Index File Handling**:
   - **What Changed**:
     - The script maintains an **index file** to avoid duplicate entries.
     - The index file is updated with unique file paths during each search.
   - **Why It’s Useful**:
     - Prevents redundant indexing of the same files.
     - Improves efficiency when searching large directories.
   - **Example**:
     - The index file (`index.txt`) contains:
       ```
       /path/to/file1.txt
       /path/to/file2.txt
       ```

---

### 9. **Error Handling**:
   - **What Changed**:
     - Added error handling for invalid TTL inputs.
     - If the user enters an invalid TTL format, the script falls back to the default value and displays a warning.
   - **Why It’s Useful**:
     - Prevents the script from crashing due to invalid inputs.
     - Provides clear feedback to the user.
   - **Example**:
     - If the user enters an invalid TTL, the script prints:
       ```
       Invalid TTL format. Using default value.
       ```

---

### 10. **User-Friendly Prompts**:
   - **What Changed**:
     - The script provides **clear prompts** for user input, including:
       - First name, full name, and email domain.
       - Search directories.
       - TLDs (e.g., `.gov`, `.edu`, `.mil`).
       - TTL for cache.
       - Output file name.
   - **Why It’s Useful**:
     - Makes the script easy to use, even for non-technical users.
     - Ensures users understand what input is expected.
   - **Example**:
     - The script prompts:
       ```
       Enter the first name (optional):
       Enter the full name (optional):
       Enter the email domain (optional, e.g., outlook.com):
       Enter the directory to search (default: current directory):
       ```

---

### 11. **Parallel Processing**:
   - **What Changed**:
     - The script uses **`concurrent.futures.ThreadPoolExecutor`** for parallel processing of file searches.
   - **Why It’s Useful**:
     - Improves performance when searching large directories.
     - Makes the script more efficient and faster.
   - **Example**:
     - Multiple files are searched simultaneously, reducing overall search time.

---

### 12. **Cache Key Generation**:
   - **What Changed**:
     - The cache key is generated using a **hash of the search terms** to ensure uniqueness.
     - The cache file is stored in a dedicated `cache` directory.
   - **Why It’s Useful**:
     - Ensures that each set of search terms has a unique cache file.
     - Prevents conflicts between different searches.
   - **Example**:
     - The cache key is generated as a hash of the search terms.

---

### 13. **Output File Handling**:
   - **What Changed**:
     - The search results are saved to an **output file** in the `text` directory.
     - The user can specify the output file name (default: `output.txt`).
   - **Why It’s Useful**:
     - Provides a persistent record of the search results.
     - Allows users to review results later.
   - **Example**:
     - The output file (`output.txt`) contains:
       ```
       1740171481.3128557|3600
       File: /path/to/file1.txt
       matching_line_1
       matching_line_2

       File: /path/to/file2.txt
       matching_line_3
       ```

---

### 14. **Signal Handling**:
   - **What Changed**:
     - Added a **signal handler** for `Ctrl+C` to clean up and exit gracefully.
     - If the script is interrupted, the output file is deleted (if it exists).
   - **Why It’s Useful**:
     - Ensures that the script exits cleanly without leaving behind incomplete files.
     - Provides a better user experience.
   - **Example**:
     - If the user presses `Ctrl+C`, the script prints:
       ```
       Interrupt received, stopping all processes...
       ```

---

### 15. **Directory Validation**:
   - **What Changed**:
     - The script checks if the specified **directories exist** before proceeding with the search.
     - If a directory does not exist, the script exits with an error message.
   - **Why It’s Useful**:
     - Prevents errors caused by invalid directory paths.
     - Provides clear feedback to the user.
   - **Example**:
     - If the directory does not exist, the script prints:
       ```
       Error: Directory /invalid/path does not exist.
       ```

---

### 16. **Default Values**:
   - **What Changed**:
     - Default values are provided for:
       - Search directory (current directory).
       - Output file name (`output.txt`).
       - TTL (1 hour).
   - **Why It’s Useful**:
     - Simplifies the user experience by reducing the need for input.
     - Ensures the script works out of the box with minimal configuration.
   - **Example**:
     - If the user does not specify a directory, the script uses the current directory.

---

### 17. **Human-Readable Time Format**:
   - **What Changed**:
     - The script converts time values (e.g., TTL, remaining time) into a **human-readable format** (e.g., `1 hour and 30 minutes`).
   - **Why It’s Useful**:
     - Makes it easier for users to understand time-related information.
     - Provides a more intuitive interface.
   - **Example**:
     - The script prints:
       ```
       Cache found and is valid for 15 minutes and 30 seconds.
       ```

---

### 18. **Clear Animation Line**:
   - **What Changed**:
     - After the animation stops, the animation line is **cleared** to avoid cluttering the console.
   - **Why It’s Useful**:
     - Keeps the console output clean and readable.
     - Provides a better user experience.
   - **Example**:
     - The animation line is cleared before displaying the search results.

---

### 19. **Interactive TLD Prompt**:
   - **What Changed**:
     - The script prompts the user to specify TLDs (e.g., `.gov`, `.edu`, `.mil`) if they want to search for specific domains.
     - The user can enter multiple TLDs separated by spaces.
   - **Why It’s Useful**:
     - Allows users to refine their search by focusing on specific domains.
     - Provides flexibility for different use cases.
   - **Example**:
     - The script prompts:
       ```
       Do you want to search for specific TLDs (e.g., .gov, .edu, .mil)? (y/n): y
       Enter the TLDs you want to search for, separated by spaces (e.g., .gov .edu .mil): .gov .edu
       ```
    

---

### 20. **Results Display**:
   - **What Changed**:
     - After the search is complete, the script **prints the results** from the output file to the console.
     - The results are displayed in a clean and readable format.
   - **Why It’s Useful**:
     - Allows users to immediately view the search results without opening the output file.
     - Provides a quick way to verify the results.
   - **Example**:
     - The script prints:
       ```
       Search Results:
       File: /path/to/file1.txt
       matching_line_1
       matching_line_2

       File: /path/to/file2.txt
       matching_line_3
       ```

---

### 21. A Windows Executable

Added in a windows executable so python wouldn't need to be installed for windows users.

### Summary of Key Features:
- **Flexible Search**: Supports optional arguments, interactive prompts, and search terms from a file.
- **Caching**: Implements a TTL-based caching mechanism with automatic deletion of expired cache.
- **Animation**: Displays a binary-style animation during the search.
- **Error Handling**: Handles invalid inputs, directory errors, and file reading errors.
- **Parallel Processing**: Uses threading for faster searches.
- **User-Friendly**: Provides clear prompts, human-readable outputs, and a help command.

---
