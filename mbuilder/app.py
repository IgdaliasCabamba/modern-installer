from utils import *

def run_form():
    name = Prompt.ask("Enter Installer Name")
    while len(name) < 1:
        name = Prompt.ask("Please, Enter a Valid Installer Name [yellow]:warning:")

    env_path = Prompt.ask("Enter Env")
    while len(env_path) < 1 or not os.path.exists(env_path):
        env_path = Prompt.ask("Please, a Valid Enter Env Path [yellow]:warning:")

    bin = Prompt.ask("Enter Bin Path")
    while len(bin) < 1 or not os.path.exists(bin):
        bin = Prompt.ask("Please, Enter a Valid Bin Path [yellow]:warning:")
    
    setup_script = Prompt.ask("Enter a Setup Script Path (whole)")
    while len(setup_script) < 1 or not os.path.exists(setup_script):
        setup_script = Prompt.ask("Please, Enter a Setup Script Path (whole)[yellow]:warning:")

    template = Prompt.ask("Choice a Template", default="init")
    build_path = Prompt.ask("Enter a Build Path (whole)")
    compression_mode = Prompt.ask("Choice a compression_mode", choices = ["tar.xz", "zip"], default = "tar.xz")

    return {
        "name": name,
        "env_path": env_path,
        "bin": bin,
        "setup_script": setup_script,
        "template": template,
        "build_path": build_path,
        "compression_mode": compression_mode
    }


def analyze_data(form):
    console.print(Padding("[bold green] Your Data", (1, 1), expand=False))
    console.print_json(data=form)
    return Confirm.ask("[bold yellow] Do you want build? :warning:")


def finish():
    exit_confirmation = Confirm.ask("Do you want quit? [yellow]:warning:")
    if exit_confirmation:
        os._exit(0)
    else:
        menu()


def new():
    form = run_form()

    while not analyze_data(form):
        option = Prompt.ask("Enter an option",
                            choices=["menu", "edit"],
                            default="edit")

        if option == "menu":
            menu()
            
        else:
            form = run_form()

    build_package(form)


def help_page():
    console.rule("[bold green] Help", style="blue")
    console.print(Panel.fit(HELP_AND_CREDITS, title="Help"))


def menu():
    console.print(Panel.fit(MENU, title="Menu"))
    option = Prompt.ask("Enter an option",
                        choices=["1", "2", "3", "new", "help", "exit"],
                        default="1")

    if option in {"1", "new"}:
        new()

    elif option in {"2", "help"}:
        help_page()

    else:
        finish()


def build_package(form):
    with Progress(SpinnerColumn("simpleDots"),
                  TextColumn("{task.description}"), BarColumn(),
                  TimeElapsedColumn()) as progress:

        task1 = progress.add_task("[green]Making Dirs", total=100)
        task2 = progress.add_task("[green]Compressing", total=100)
        task3 = progress.add_task("[green]Finishing", total=100)
        task_main = progress.add_task("[green]Building", total=100)

        while not progress.finished:
            
            """ Task 1: Make dirs """
            need_dirs = [
                os.path.join(form['build_path'], "release"),
                os.path.join(form['build_path'], "release", "bin"),
                os.path.join(form['build_path'], "release", "install"),
                #os.path.join(form['build_path'], "release", "ui")
            ]

            for dir in need_dirs:
                if not os.path.exists(dir):
                    os.makedirs(dir)
            
            progress.update(task1, advance=100)
            progress.update(task_main, advance=25)
            
            """ Task 2: Compress Bin"""
            if form["compression_mode"].startswith("tar"):
                make_tarfile(os.path.join(form['build_path'], "release", "bin", "package.tar.xz"), form["bin"])

            progress.update(task2, advance=100)
            progress.update(task_main, advance=50)
            
            """ Task 3: Finishing"""
            shutil.copyfile(MAIN_FILE, os.path.join(form['build_path'], "release", "main.py"))
            shutil.copyfile(BACKEND_FILE, os.path.join(form['build_path'], "release", "backend.py"))
            shutil.copyfile(SPEC_FILE, os.path.join(form['build_path'], "release", "main.spec"))
            shutil.copyfile(form["setup_script"], os.path.join(form['build_path'], "release", "install", "setup"))
            progress.update(task3, advance=50)
            shutil.copytree(INIT_TEMPLATE, os.path.join(form['build_path'], "release", "ui"))
            progress.update(task3, advance=50)
            
            progress.update(task3, advance=100)
            progress.update(task_main, advance=25)

def init():
    console.rule(f"[bold #72c3f0] Modern Installer {VERSION}", style="blue")
    menu()


if __name__ == "__main__":
    console = Console()
    init()
