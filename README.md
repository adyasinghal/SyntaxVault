# SyntaxVault 

**SyntaxVault** is a high-performance CLI tool built to manage and retrieve reusable code snippets instantly. 

## Features
* **O(1) Search**: Snippets are stored in a hash map for near-instant retrieval.
* **Syntax Highlighting**: Beautiful terminal output powered by `rich`.
* **Auto-Clipboard**: Snippets are automatically copied to your system clipboard upon retrieval.
* **Template Support**: Quick-copy boilerplate code for Competitive Programming (LeetCode/Codeforces).
* **Architecture**: Separated storage logic and CLI interface.

## Tech Stack
- **Language:** Python 3.10
- **CLI Framework:** [Typer](https://typer.tiangolo.com/)
- **UI & Formatting:** [Rich](https://rich.readthedocs.io/)
- **Clipboard Management:** [Pyperclip](https://pyperclip.readthedocs.io/)

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/SyntaxVault.git
   cd SyntaxVault
   ```
2. **Set up a virtual environment**
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. **Create a global alias**
    ```
    nano ~/.zshrc
    ```
    Add this line at the bottom:
    ```
    alias sv='/path/to/SyntaxVault/venv/bin/python /path/to/SyntaxVault/main.py'
    ```
    Refresh your config:
    ```
    source ~/.zshrc
    ```

## Usage

| Command | Description|
| --- | --- |
| `sv add <name>`| Add a new code snippet|
| `sv list`| Show all code snippets in a table|
| `sv get <name>`| Display code and copy to clipboard|
| `sv edit <name>`| Modify an existing code snippet|  
| `sv search <query>`| Filter snippets by name or description|
| `sv template <lang>`| Copy a CP template (e.g., `sv template cpp`)| 

<img width="1470" height="956" alt="Screenshot 2026-01-13 at 11 27 46 AM" src="https://github.com/user-attachments/assets/aa65d1d6-0b91-4971-8116-b77f9fea5ec3" />
