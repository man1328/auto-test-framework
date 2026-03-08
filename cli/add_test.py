#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║         AUTOMATION FRAMEWORK — Add Test CLI                   ║
║    Add a new test file to an existing project by typing!      ║
╚═══════════════════════════════════════════════════════════════╝

Usage:
    python cli/add_test.py --project my_app --name LoginTest --type android
    python cli/add_test.py --project my_api --name CreateOrderTest --type api
    python cli/add_test.py  # interactive mode
"""
import argparse
import sys
import re
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt, Confirm
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
PROJECTS_DIR = ROOT / "projects"

console = Console() if _HAS_RICH else None


def _ask(prompt, default=""):
    if _HAS_RICH:
        return Prompt.ask(prompt, default=default)
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default


def _to_class_name(name: str) -> str:
    return "".join(word.capitalize() for word in re.split(r"[_\-\s]+", name))


def _to_snake_case(name: str) -> str:
    name = re.sub(r"[\-\s]+", "_", name)
    name = re.sub(r"([A-Z])", r"_\1", name).lstrip("_").lower()
    return re.sub(r"_+", "_", name)


def gather_test_methods_interactively():
    """Ask user to describe their test methods."""
    methods = []
    if _HAS_RICH:
        console.print("\n[cyan]📝 Let's add your test methods.[/cyan]")
        console.print("[dim]Press Enter with empty name to stop.[/dim]\n")

    i = 1
    while True:
        name = _ask(f"  Test method {i} name (e.g. test_login_success, or ENTER to stop)", "")
        if not name:
            break
        if not name.startswith("test_"):
            name = f"test_{name}"
        title = _ask(f"  Allure title for '{name}'", name.replace("_", " ").title())
        docstring = _ask(f"  Docstring for '{name}'", f"Verify {name.replace('test_', '').replace('_', ' ')}")
        severity = _ask(f"  Severity [blocker/critical/normal/minor/trivial]", "normal")
        marker = _ask(f"  Pytest marker [smoke/regression]", "regression")
        methods.append({
            "name": name,
            "title": title,
            "docstring": docstring,
            "severity": severity.upper(),
            "marker": marker,
        })
        i += 1

    return methods if methods else [
        {
            "name": "test_placeholder",
            "title": "Placeholder test",
            "docstring": "TODO: replace with real test logic.",
            "severity": "NORMAL",
            "marker": "regression",
        }
    ]


def add_test(cfg: dict):
    project_name = _to_snake_case(cfg["project"])
    test_name = cfg["name"]
    ptype = cfg["type"]

    project_dir = PROJECTS_DIR / project_name
    if not project_dir.exists():
        msg = f"Project '{project_name}' not found at {project_dir}. Create it first with create_project.py"
        print(f"ERROR: {msg}")
        sys.exit(1)

    class_name = _to_class_name(test_name)
    if not class_name.startswith("Test"):
        class_name = f"Test{class_name}"

    test_methods = cfg.get("methods") or gather_test_methods_interactively()
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

    if ptype == "android":
        # Try to find an existing screen or create a new one
        screens_dir = project_dir / "screens"
        screens_dir.mkdir(parents=True, exist_ok=True)
        screen_name = _ask("📱 Screen class name to use/create", f"{_to_class_name(project_name)}Screen")
        screen_module = _to_snake_case(screen_name)
        screen_file = screens_dir / f"{screen_module}.py"

        if not screen_file.exists():
            po_src = env.get_template("page_object.py.j2").render(
                class_name=screen_name, page_url="N/A", mobile=True,
                docstring=f"Screen object for {screen_name}."
            )
            screen_file.write_text(po_src, encoding="utf-8")
            print(f"  Created screen: {screen_file.relative_to(ROOT)}")

        test_src = env.get_template("android_test.py.j2").render(
            project_name=project_name, test_class_name=class_name,
            screen_class_name=screen_name, screen_module=screen_module,
            feature_name=test_name, docstring=f"{class_name} Android tests.",
            test_methods=test_methods,
        )
        test_file = project_dir / "tests" / f"test_{_to_snake_case(test_name)}.py"

    elif ptype == "api":
        test_src = env.get_template("api_test.py.j2").render(
            project_name=project_name, test_class_name=class_name,
            feature_name=test_name, base_url="",
            docstring=f"{class_name} API tests.",
            test_methods=test_methods,
        )
        test_file = project_dir / "tests" / f"test_{_to_snake_case(test_name)}.py"

    elif ptype == "web":
        page_name = _ask("🌐 Page class name to use/create", f"{_to_class_name(test_name)}Page")
        page_module = _to_snake_case(page_name)
        pages_dir = project_dir / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        page_file = pages_dir / f"{page_module}.py"

        if not page_file.exists():
            po_src = env.get_template("page_object.py.j2").render(
                class_name=page_name, page_url="/", mobile=False,
                docstring=f"Page object for {page_name}."
            )
            page_file.write_text(po_src, encoding="utf-8")
            print(f"  Created page: {page_file.relative_to(ROOT)}")

        test_src = env.get_template("web_test.py.j2").render(
            project_name=project_name, test_class_name=class_name,
            page_class_name=page_name, page_module=page_module,
            feature_name=test_name, page_url="/",
            docstring=f"{class_name} web tests.",
            test_methods=test_methods,
        )
        test_file = project_dir / "tests" / f"test_{_to_snake_case(test_name)}.py"

    else:
        print(f"Unknown type: {ptype}")
        sys.exit(1)

    if test_file.exists():
        overwrite = _ask(f"⚠️  '{test_file.name}' already exists. Overwrite? [y/N]", "n")
        if overwrite.lower() != "y":
            print("Aborted.")
            sys.exit(0)

    (project_dir / "tests").mkdir(parents=True, exist_ok=True)
    (project_dir / "tests" / "__init__.py").touch()
    test_file.write_text(test_src, encoding="utf-8")

    if _HAS_RICH:
        console.print(Panel(
            f"[bold green]✅ Test file created![/bold green]\n\n"
            f"[white]File:[/white] {test_file.relative_to(ROOT)}\n"
            f"[white]Class:[/white] {class_name}\n"
            f"[white]Methods:[/white] {len(test_methods)} test(s)\n\n"
            f"[cyan]Run:[/cyan] pytest {test_file.relative_to(ROOT)} -v",
            border_style="green"
        ))
    else:
        print(f"\n✅ Created: {test_file.relative_to(ROOT)}")
        print(f"   Run: pytest {test_file.relative_to(ROOT)} -v")


def main():
    parser = argparse.ArgumentParser(
        description="Add a new test file to an existing project",
        epilog="""
Examples:
  python cli/add_test.py --project my_app --name LoginTest --type android
  python cli/add_test.py --project my_api --name CreateOrderTest --type api
  python cli/add_test.py   # interactive mode
        """,
    )
    parser.add_argument("--project", help="Project name (must exist in projects/)")
    parser.add_argument("--name", help="Test class name (e.g. LoginTest)")
    parser.add_argument("--type", choices=["android", "web", "api"])
    args = parser.parse_args()

    if not args.project:
        args.project = _ask("🗂️  Project name", "")
    if not args.type:
        args.type = _ask("🔧 Test type [android / web / api]", "api")
    if not args.name:
        args.name = _ask("📝 Test class name (e.g. LoginTest)", "NewTest")

    add_test({"project": args.project, "name": args.name, "type": args.type})


if __name__ == "__main__":
    main()
