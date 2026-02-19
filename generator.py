from pathlib import Path
from jinja2 import Template
import shutil

class CodeGenerator:
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
    
    def create_project(self, template: str, name: str):
        """Create project from template"""
        template_path = self.templates_dir / template
        if not template_path.exists():
            self._create_default_template(template)
        
        target = Path(name)
        if target.exists():
            raise ValueError(f"Directory '{name}' already exists")
        
        shutil.copytree(template_path, target)
        self._render_template_vars(target, {"project_name": name})
    
    def _create_default_template(self, template: str):
        """Create default template structure"""
        template_path = self.templates_dir / template
        template_path.mkdir(parents=True, exist_ok=True)
        
        if template == "fastapi":
            self._create_fastapi_template(template_path)
        elif template == "flask":
            self._create_flask_template(template_path)
        elif template == "react":
            self._create_react_template(template_path)
        elif template == "vue":
            self._create_vue_template(template_path)
        else:
            raise ValueError(f"Unknown template: {template}")
    
    def _create_fastapi_template(self, path: Path):
        (path / "main.py").write_text("""from fastapi import FastAPI

app = FastAPI(title="{{ project_name }}")

@app.get("/")
def read_root():
    return {"message": "Hello from {{ project_name }}"}
""")
        (path / "requirements.txt").write_text("fastapi>=0.104.0\nuvicorn>=0.24.0\n")
        (path / "README.md").write_text("# {{ project_name }}\n\nFastAPI project\n")
    
    def _create_flask_template(self, path: Path):
        (path / "app.py").write_text("""from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return {"message": "Hello from {{ project_name }}"}

if __name__ == '__main__':
    app.run(debug=True)
""")
        (path / "requirements.txt").write_text("flask>=3.0.0\n")
        (path / "README.md").write_text("# {{ project_name }}\n\nFlask project\n")
    
    def _create_react_template(self, path: Path):
        (path / "package.json").write_text("""{
  "name": "{{ project_name }}",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
""")
        src = path / "src"
        src.mkdir()
        (src / "App.jsx").write_text("""export default function App() {
  return <h1>{{ project_name }}</h1>
}
""")
        (path / "README.md").write_text("# {{ project_name }}\n\nReact project\n")
    
    def _create_vue_template(self, path: Path):
        (path / "package.json").write_text("""{
  "name": "{{ project_name }}",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "vue": "^3.3.0"
  }
}
""")
        src = path / "src"
        src.mkdir()
        (src / "App.vue").write_text("""<template>
  <h1>{{ project_name }}</h1>
</template>
""")
        (path / "README.md").write_text("# {{ project_name }}\n\nVue project\n")
    
    def _render_template_vars(self, path: Path, vars: dict):
        """Render Jinja2 variables in all files"""
        for file in path.rglob("*"):
            if file.is_file():
                try:
                    content = file.read_text()
                    template = Template(content)
                    rendered = template.render(**vars)
                    file.write_text(rendered)
                except:
                    pass
    
    def generate_code(self, type: str, name: str, output: str):
        """Generate code based on type"""
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if type == "crud":
            return self._generate_crud(name, output_path)
        elif type == "api":
            return self._generate_api(name, output_path)
        elif type == "model":
            return self._generate_model(name, output_path)
        elif type == "component":
            return self._generate_component(name, output_path)
        else:
            raise ValueError(f"Unknown type: {type}")
    
    def _generate_crud(self, name: str, path: Path):
        file = path / f"{name}_crud.py"
        file.write_text(f"""class {name.capitalize()}CRUD:
    def create(self, data: dict):
        pass
    
    def read(self, id: int):
        pass
    
    def update(self, id: int, data: dict):
        pass
    
    def delete(self, id: int):
        pass
""")
        return file
    
    def _generate_api(self, name: str, path: Path):
        file = path / f"{name}_api.py"
        file.write_text(f"""from fastapi import APIRouter

router = APIRouter(prefix="/{name}", tags=["{name}"])

@router.get("/")
def list_{name}():
    return []

@router.post("/")
def create_{name}(data: dict):
    return data

@router.get("/{{id}}")
def get_{name}(id: int):
    return {{"id": id}}
""")
        return file
    
    def _generate_model(self, name: str, path: Path):
        file = path / f"{name}_model.py"
        file.write_text(f"""from pydantic import BaseModel

class {name.capitalize()}(BaseModel):
    id: int
    name: str
""")
        return file
    
    def _generate_component(self, name: str, path: Path):
        file = path / f"{name.capitalize()}.jsx"
        file.write_text(f"""export default function {name.capitalize()}() {{
  return (
    <div className="{name}">
      <h2>{name.capitalize()}</h2>
    </div>
  )
}}
""")
        return file
