#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║         AUTOMATION FRAMEWORK — Project Generator CLI          ║
║    Create a new test project by just typing a command!        ║
╚═══════════════════════════════════════════════════════════════╝

Usage:
    python cli/create_project.py --name my_app --type android
    python cli/create_project.py --name my_api --type api --base-url https://api.example.com
    python cli/create_project.py --name my_web --type web --base-url https://example.com
    python cli/create_project.py  # interactive mode (asks questions)
"""
import argparse
import sys
import re
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import print as rprint
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
PROJECTS_DIR = ROOT / "projects"

console = Console() if _HAS_RICH else None


def _print(msg, style=""):
    if _HAS_RICH:
        console.print(msg, style=style)
    else:
        print(msg)


def _ask(prompt, default=""):
    if _HAS_RICH:
        return Prompt.ask(prompt, default=default)
    else:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default


def _confirm(prompt, default=True):
    if _HAS_RICH:
        return Confirm.ask(prompt, default=default)
    else:
        val = input(f"{prompt} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
        if val == "":
            return default
        return val in ("y", "yes")


def _to_class_name(name: str) -> str:
    """Convert 'my_app_login' -> 'MyAppLogin'"""
    return "".join(word.capitalize() for word in re.split(r"[_\-\s]+", name))


def _to_snake_case(name: str) -> str:
    """Convert 'MyApp' or 'my-app' -> 'my_app'"""
    name = re.sub(r"[\-\s]+", "_", name)
    name = re.sub(r"([A-Z])", r"_\1", name).lstrip("_").lower()
    return re.sub(r"_+", "_", name)


def gather_args_interactive(args) -> dict:
    """If args are missing, ask the user interactively."""
    if _HAS_RICH:
        console.print(Panel.fit(
            "[bold cyan]🚀 Automation Framework — New Project Generator[/bold cyan]\n"
            "Answer a few questions to scaffold your project.",
            border_style="cyan"
        ))

    name = args.name or _ask("📛 Project name (snake_case)", "my_project")
    type_ = args.type or _ask("🔧 Project type [android / web / api]", "api")
    base_url = args.base_url or ""

    if type_ in ("web", "api") and not base_url:
        base_url = _ask("🌐 Base URL", "https://jsonplaceholder.typicode.com")

    app_pkg = ""
    app_activity = ""
    if type_ == "android" and not args.app_package:
        if _confirm("📦 Do you have an app package/activity? (No = use APK path)", default=False):
            app_pkg = _ask("App package (e.g. com.example.myapp)")
            app_activity = _ask("App activity (e.g. .MainActivity)")

    return {
        "name": _to_snake_case(name),
        "type": type_.lower().strip(),
        "base_url": base_url,
        "app_package": app_pkg or (args.app_package if args.app_package else ""),
        "app_activity": app_activity or (args.app_activity if args.app_activity else ""),
    }


def create_project(cfg: dict):
    name = cfg["name"]
    ptype = cfg["type"]
    project_dir = PROJECTS_DIR / name

    if project_dir.exists():
        _print(f"[red]❌ Project '{name}' already exists at {project_dir}[/red]" if _HAS_RICH
               else f"ERROR: Project '{name}' already exists at {project_dir}")
        sys.exit(1)

    _print(f"\n[bold green]📁 Creating project: {name} (type={ptype})[/bold green]" if _HAS_RICH
           else f"\nCreating project: {name} (type={ptype})")

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    class_name = _to_class_name(name)

    # ─── Determine structure ──────────────────────────────────────────────────
    if ptype == "android":
        dirs = [
            project_dir / "screens",
            project_dir / "tests",
            project_dir / "test_data",
        ]
        screen_name = f"{class_name}Screen"
        screen_module = _to_snake_case(screen_name)

        # Page object
        po_src = env.get_template("page_object.py.j2").render(
            class_name=screen_name,
            page_url="N/A (Android screen)",
            mobile=True,
            docstring=f"Screen object for the {class_name} screen.",
        )
        # Test file
        test_src = env.get_template("android_test.py.j2").render(
            project_name=name,
            test_class_name=f"Test{class_name}",
            screen_class_name=screen_name,
            screen_module=screen_module,
            feature_name=class_name,
            docstring=f"Auto-generated tests for {class_name}.",
            test_methods=[
                {"name": "test_screen_displays", "title": f"{class_name} screen is visible",
                 "severity": "blocker", "marker": "smoke",
                 "docstring": "Verify the screen is shown after navigation."},
            ],
        )
        files = {
            project_dir / "screens" / f"{screen_module}.py": po_src,
            project_dir / "tests" / f"test_{_to_snake_case(class_name)}.py": test_src,
            project_dir / "test_data" / "data.yml": "# Add your YAML test data here\n",
        }

    elif ptype == "api":
        dirs = [project_dir / "tests", project_dir / "test_data"]
        test_src = env.get_template("api_test.py.j2").render(
            project_name=name,
            test_class_name=f"Test{class_name}",
            feature_name=class_name,
            base_url=cfg["base_url"],
            docstring=f"Auto-generated API tests for {class_name}.",
            test_methods=[
                {"name": "test_get_list", "title": "GET list returns 200",
                 "severity": "blocker", "marker": "smoke",
                 "docstring": "Verify the main list endpoint returns HTTP 200."},
            ],
        )
        files = {
            project_dir / "tests" / f"test_{_to_snake_case(class_name)}.py": test_src,
            project_dir / "test_data" / "data.yml": "# Add your YAML test data here\n",
        }

    elif ptype == "web":
        dirs = [project_dir / "pages", project_dir / "tests", project_dir / "test_data"]
        page_name = f"{class_name}Page"
        page_module = _to_snake_case(page_name)

        po_src = env.get_template("page_object.py.j2").render(
            class_name=page_name,
            page_url="/",
            mobile=False,
            docstring=f"Page object for the {class_name} page.",
        )
        test_src = env.get_template("web_test.py.j2").render(
            project_name=name,
            test_class_name=f"Test{class_name}",
            page_class_name=page_name,
            page_module=page_module,
            feature_name=class_name,
            page_url="/",
            docstring=f"Auto-generated web tests for {class_name}.",
            test_methods=[
                {"name": "test_page_loads", "title": f"{class_name} page loads",
                 "severity": "blocker", "marker": "smoke",
                 "docstring": "Verify the page loads without errors."},
            ],
        )
        files = {
            project_dir / "pages" / f"{page_module}.py": po_src,
            project_dir / "tests" / f"test_{_to_snake_case(class_name)}.py": test_src,
            project_dir / "test_data" / "data.yml": "# Add your YAML test data here\n",
        }

    else:
        _print(f"[red]Unknown project type: {ptype}. Use android, web, or api.[/red]" if _HAS_RICH
               else f"Unknown type: {ptype}")
        sys.exit(1)

    # Write .env template for project
    env_content = _build_env_template(ptype, cfg)
    files[project_dir / ".env.example"] = env_content

    # ─── Create dirs and write files ─────────────────────────────────────────
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        (d / "__init__.py").touch()
        _print(f"  [dim]📂 {d.relative_to(ROOT)}[/dim]" if _HAS_RICH
               else f"  Created dir: {d.relative_to(ROOT)}")

    (project_dir / "__init__.py").touch()

    for filepath, content in files.items():
        filepath.write_text(content, encoding="utf-8")
        _print(f"  [green]✔[/green] {filepath.relative_to(ROOT)}" if _HAS_RICH
               else f"  Created: {filepath.relative_to(ROOT)}")

    _print_next_steps(name, ptype, project_dir)


def _build_env_template(ptype, cfg):
    lines = ["# Copy this to .env and fill in your values\n"]
    if ptype == "android":
        lines += [
            f"APPIUM_SERVER_URL=http://127.0.0.1:4723",
            f"ANDROID_PLATFORM_VERSION=13",
            f"ANDROID_DEVICE_NAME=emulator-5554",
            f"ANDROID_APP_PATH=/path/to/your-app.apk",
            f"ANDROID_APP_PACKAGE={cfg.get('app_package', 'com.example.app')}",
            f"ANDROID_APP_ACTIVITY={cfg.get('app_activity', '.MainActivity')}",
        ]
    elif ptype == "api":
        lines += [f"API_BASE_URL={cfg.get('base_url', 'https://api.example.com')}", "API_TOKEN="]
    elif ptype == "web":
        lines += [
            f"BASE_URL={cfg.get('base_url', 'https://example.com')}",
            "BROWSER=chrome",
            "HEADLESS=false",
        ]
    return "\n".join(lines) + "\n"


def _print_next_steps(name, ptype, project_dir):
    steps = {
        "android": [
            "1. Start Appium:        npx appium",
            "2. Connect device/emulator and set caps in .env",
            f"3. Run tests:           pytest projects/{name}/ -m android -v",
        ],
        "api": [
            f"1. Set API_BASE_URL in .env",
            f"2. Run tests:           pytest projects/{name}/ -m api -v",
        ],
        "web": [
            "1. Set BASE_URL in .env",
            f"2. Run tests:           pytest projects/{name}/ -m web -v",
        ],
    }
    if _HAS_RICH:
        console.print(Panel(
            f"[bold green]✅ Project '{name}' created![/bold green]\n\n"
            + "\n".join(steps.get(ptype, [])),
            title="[cyan]Next Steps[/cyan]", border_style="green"
        ))
    else:
        print(f"\n✅ Project '{name}' created!")
        for s in steps.get(ptype, []):
            print(f"  {s}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a new automation test project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli/create_project.py --name my_app --type android
  python cli/create_project.py --name shop_api --type api --base-url https://api.shop.com
  python cli/create_project.py --name admin_portal --type web --base-url https://admin.example.com
  python cli/create_project.py   # interactive mode
        """,
    )
    parser.add_argument("--name", help="Project name (snake_case)")
    parser.add_argument("--type", choices=["android", "web", "api"], help="Project type")
    parser.add_argument("--base-url", dest="base_url", help="Base URL (web/api only)")
    parser.add_argument("--app-package", dest="app_package", help="Android app package")
    parser.add_argument("--app-activity", dest="app_activity", help="Android app activity")
    args = parser.parse_args()

    cfg = gather_args_interactive(args)
    create_project(cfg)


if __name__ == "__main__":
    main()
