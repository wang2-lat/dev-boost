from pathlib import Path
import yaml

class SnippetManager:
    def __init__(self):
        self.snippets_dir = Path.home() / ".dev-boost" / "snippets"
        self.snippets_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.snippets_dir / "index.yaml"
        if not self.index_file.exists():
            self.index_file.write_text("snippets: []\n")
    
    def add_snippet(self, name: str, file_path: str):
        """Add a new snippet"""
        source = Path(file_path)
        if not source.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        target = self.snippets_dir / f"{name}.txt"
        target.write_text(source.read_text())
        
        index = yaml.safe_load(self.index_file.read_text())
        if not any(s["name"] == name for s in index["snippets"]):
            index["snippets"].append({
                "name": name,
                "description": f"Snippet from {file_path}"
            })
            self.index_file.write_text(yaml.dump(index))
    
    def list_snippets(self):
        """List all snippets"""
        index = yaml.safe_load(self.index_file.read_text())
        return index["snippets"]
    
    def get_snippet(self, name: str):
        """Get snippet content"""
        file = self.snippets_dir / f"{name}.txt"
        if not file.exists():
            raise FileNotFoundError(f"Snippet not found: {name}")
        return file.read_text()
