# Unicode Spoof File Detector

This Python script detects and blocks potentially dangerous files that use Unicode characters to spoof file extensions, commonly used in phishing and malware distribution. It monitors the Downloads folder and alerts the user if a suspicious file is found.

## Features

*   **Unicode Character Detection:** Identifies files with suspicious Unicode characters in their names, often used to disguise file types.
*   **File Type Verification:** Uses `libmagic` to verify the actual file type and compares it against the apparent extension.
*   **Real-time Monitoring:** Continuously monitors the Downloads folder for new files.
*   **Blocking Execution:** Prevents the execution of detected spoofed files by modifying their access control lists (ACLs).
*   **Windows Service:** Runs as a Windows service for continuous background monitoring.
*   **Automatic Startup:** Configures the service to start automatically on boot.

## Installation

1.  **Dependencies:** Ensure you have Python 3 installed. Install the required packages:

    ```bash
    pip install pywin32 python-magic
    ```

    You may need to install `libmagic` separately depending on your system. On Windows, you can download a pre-compiled version and add its DLLs to your system's PATH.

2.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/](https://github.com/)[YourUsername]/unicode-spoof-detector.git
    cd unicode-spoof-detector
    ```

3.  **Install the Service:**

    ```bash
    python unicode_spoof_detector.py install
    ```

4.  **Start the Service:**

    ```bash
    python unicode_spoof_detector.py start
    ```

## Usage

The detector runs as a background service. Once installed and started, it automatically monitors the Downloads folder. If a suspicious file is detected, a warning popup will appear, and the file's execution will be blocked.

<details>
<summary>Customization</summary>

*   **`suspicious_unicode_patterns`:** You can modify the regular expressions in this list within the `UnicodeSpoofDetector` class to refine the Unicode character detection.
*   **`dangerous_extensions`:** This list contains the file extensions considered potentially dangerous. You can add or remove extensions as needed.
*   **`download_folder`:** The default monitored folder is the user's Downloads directory. You can change this by passing a different path to the `UnicodeSpoofDetector` constructor.

```python
class UnicodeSpoofDetector:
    def __init__(self, download_folder=None):
        self.download_folder = download_folder or os.path.expanduser('~\\Downloads')
        self.suspicious_unicode_patterns = [
            r'[\u200B-\u200D\u2060\u2061\u2062\u2063\u2064]', # Zero-width spaces and other invisible characters
            r'[\u202A-\u202E]', # Right-to-left and left-to-right overrides
            r'[^\x00-\x7F]', # Any character outside basic ASCII
            r'[\u2028\u2029]', # Line and paragraph separators
            r'[\uFFF0-\uFFFF]', # Specials
            r'[\u061C]' # Arabic Letter Mark
        ]
        self.dangerous_extensions = [
            '.exe', '.bat', '.cmd', '.vbs', '.ps1',
            '.msi', '.scr', '.jar', '.js', '.pif', '.cpl' #Added more
        ]
        # ... rest of the class
