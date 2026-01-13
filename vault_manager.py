import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class VaultManager:
    def __init__(self):
        self.db_path = Path.home() / ".syntaxvault.json"
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.db_path.exists():
            with open(self.db_path, "w") as f:
                json.dump({}, f)

    def load_vault(self) -> Dict[str, Any]:
        try:
            with open(self.db_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_vault(self, data: Dict[str, Any]):
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=4)

    def add_snippet(self, name: str, code: str, language: str, description: str):
        vault = self.load_vault()
        vault[name] = {
            "code": code,
            "language": language.lower(),
            "description": description,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_vault(vault)

    def get_snippet(self, name: str) -> Optional[Dict[str, Any]]:
        vault = self.load_vault()
        return vault.get(name)

    def delete_snippet(self, name: str) -> bool:
        vault = self.load_vault()
        if name in vault:
            del vault[name]
            self.save_vault(vault)
            return True
        return False

    def search_snippets(self, query: str) -> Dict[str, Any]:
        vault = self.load_vault()
        query = query.lower()
        return {
            name: data for name, data in vault.items()
            if query in name.lower() or query in data["description"].lower()
        }
    
    def update_snippet(self, name: str, code: str = None, language: str = None, description: str = None):
        vault = self.load_vault()
        if name in vault:
            if code:
                vault[name]["code"] = code
            if language:
                vault[name]["language"] = language.lower()
            if description:
                vault[name]["description"] = description
            
            vault[name]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_vault(vault)
            return True
        return False