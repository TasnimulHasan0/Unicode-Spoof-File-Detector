# Unicode Spoof File Detector

This Python script detects and blocks potentially dangerous files that use Unicode characters to spoof file extensions, commonly used in phishing and malware distribution. It monitors the Downloads folder and alerts the user if a suspicious file is found.

## Features

*   **Unicode Character Detection:** Identifies files with suspicious Unicode characters in their names, often used to disguise file types.
*   **File Type Verification:** Uses `libmagic` to verify the actual file type and compares it against the apparent extension.
*   **Real-time Monitoring:** Continuously monitors the Downloads folder for new files.
*   **Blocking Execution:** Prevents the execution of detected spoofed files by modifying their access control lists (ACLs).
*   **Windows Service:** Runs as a Windows service for continuous background monitoring.
*   **Automatic Startup:** Configures the service to start automatically on boot.

## Installation for Windows Users
## Installation for Windows Users

**1. Install Python (Admin):**

*   Download Python: https://www.python.org/downloads/windows/ (Check "Add Python 3.x to PATH")

**2. Install Git (If needed):**

*   https://git-scm.com/download/win

**3. Clone the Repository:**

*   Open CMD/PowerShell.
*   `cd C:\projects` (or your preferred directory)
*   Run:

    ```bash
    git clone https://github.com/TasnimulHasan0/Unicode-Spoof-File-Detector
    cd unicode-spoof-detector
    ```

**4. Install Dependencies (Admin):**

*   Open CMD/PowerShell as admin.
*   `cd C:\projects\unicode-spoof-detector` (or your path)
*   Run:

    ```bash
    pip install -r requirements.txt
    ```

**5. Install and Start Service (Admin):**

*   Run:

    ```bash
    python unicode_spoof_detector.py install
    python unicode_spoof_detector.py start
    ```

**6. Set Auto-Start (Admin):**

*   Run:

    ```bash
    python unicode_spoof_detector.py set_auto_start
    ```

**Alternative: Manual Service Management (Admin for some actions):**

*   Open Services app (`services.msc`).
*   Find "UnicodeSpoofDetector".
*   Right-click to manage.

**Important:** Admin privileges are required for service operations and blocking file execution.


## Usage

The detector runs as a background service. Once installed and started, it automatically monitors the Downloads folder. If a suspicious file is detected, a warning popup will appear, and the file's execution will be blocked.

<details>
<summary>Uninstallation</summary>

1.  **Stop the Service:**

    ```bash
    python unicode_spoof_detector.py stop
    ```

2.  **Remove the Service:**

    ```bash
    python unicode_spoof_detector.py remove
    ```

3.  **Delete the Repository:**

    ```bash
    cd ..
    rm -rf unicode_spoof_detector
    ```

</details>

<details>
<summary>Customization</summary>

*   **`suspicious_unicode_patterns`:** You can modify the regular expressions in this list within the `UnicodeSpoofDetector` class to refine the Unicode character detection.
*   **`dangerous_extensions`:** This list contains the file extensions considered potentially dangerous. You can add or remove extensions as needed.
*   **`download_folder`:** The default monitored folder is the user's Downloads directory. You can change this by passing a different path to the `UnicodeSpoofDetector` constructor.

</details>

<details>
<summary>Issues</summary>

If you encounter any issues or have suggestions for improvements, please open an issue on GitHub. When reporting an issue, please provide:

*   **Steps to reproduce the issue.**
*   **The operating system you are using.**
*   **Any relevant error messages or logs.**

</details>

<details>
<summary>Contributions</summary>

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch for your feature or bug fix.**
3.  **Make your changes and commit them.**
4.  **Push your changes to your fork.**
5.  **Submit a pull request.**

</details>

## License

This project is licensed under the [MIT License](LICENSE).
