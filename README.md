# Unicode Spoof File Detector

The **Unicode Spoof File Detector** is a Python-based security tool that monitors your system for files containing suspicious Unicode characters, often used to spoof file extensions. It blocks these files from execution and alerts the user, helping to prevent malicious activity.

## Features
- Detects filenames with suspicious Unicode characters (e.g., zero-width spaces, bidirectional controls).
- Verifies that file types match their extensions (e.g., `.exe` files are actually executables).
- Blocks execution of spoofed or dangerous files by modifying their permissions.
- Continuously monitors the `Downloads` folder (configurable).
- Operates as a Windows service, running silently in the background.
- Auto-starts on system boot once installed as a service.

---

## How It Works
1. **Suspicious Unicode Detection:**
   - Scans filenames for Unicode patterns commonly used in spoofing attacks.
   - Examples of blocked characters include:
     - Zero-width spaces (`\u200B-\u200D`)
     - Bidirectional controls (`\u202A-\u202E`)
     - Non-ASCII characters (`[^\x00-\x7F]`).

2. **File Type Verification:**
   - Uses the `python-magic` library to ensure the file type matches its extension.
   - Protects against files that disguise themselves (e.g., a `.docx` file that is actually an executable).

3. **Blocking Execution:**
   - Prevents execution by removing execute permissions via Windows security descriptors.

4. **Service Integration:**
   - Registers itself as a Windows service for seamless background operation.
   - Configures the service to auto-start on system boot.

---

<details>
<summary><strong>Customization</strong></summary>

### Change the Monitored Directory
By default, the tool monitors the `Downloads` folder. To monitor additional or different directories:
1. Open the `unicode-spoof-detector.py` file.
2. Locate the `self.download_folder` variable in the `UnicodeSpoofDetector` class.
3. Modify it to include the path of your desired directory:
   ```python
   self.download_folder = os.path.expanduser('~\\Desktop')
---

## Prerequisites
1. **Python 3.8 or later** installed on your system.
2. Required Python libraries:
   ```bash
   pip install pywin32 python-magic
   
