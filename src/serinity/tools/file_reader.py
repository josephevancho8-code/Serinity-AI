import os
from typing import Dict, Any

class FileReaderTool:
    name = "file_reader"
    description = "Reads text content from a specified local file."
    required_permission = "file_reader"

    def execute(self, file_path: str, **kwargs) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File '{file_path}' not found."}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
