import os
import json
from jinja2 import Environment, PackageLoader

engine = Environment(loader=PackageLoader(__package__, 'templates'))


def create_module(name: str, parent: str = ""):
    module = {
        "name": name,
        "class_name": name.capitalize()
    }
    os.makedirs(f"{parent}{name}", exist_ok=True)
    with open(f"{parent}{name}/routes.py", "w") as f:
        f.write(engine.get_template("routes.py").render(module=module))
    with open(f"{parent}{name}/dtos.py", "w") as f:
        f.write(engine.get_template("dtos.py").render(module=module))
    with open(f"{parent}{name}/services.py", "w") as f:
        f.write(engine.get_template("services.py").render(module=module))
    with open(f"{parent}{name}/models.py", "w") as f:
        f.write(engine.get_template("models.py").render(module=module))
    with open(f"{parent}{name}/config.py", "w") as f:
        f.write(engine.get_template("module_config.py").render(module=module))

    config = {}
    path = f"{parent}config.json"
    if os.path.exists(path):
        with open(path) as f:
            config = json.load(f)

    if "modules.init" not in config:
        config["modules.init"] = []

    if f"{name}.config" not in config["modules.init"]:
        config["modules.init"].append(f"{name}.config")

    with open(path, "w") as f:
        json.dump(config, f, indent=4)
        



def init_project():
    os.makedirs("src", exist_ok=True)
    with open("requirements.txt", "w") as f:
        f.write(engine.get_template("requirements.txt").render())

    with open("src/app.py", "w") as f:
        f.write(engine.get_template("app.py").render())

    with open("src/config.py", "w") as f:
        f.write(engine.get_template("config.py").render())

    


