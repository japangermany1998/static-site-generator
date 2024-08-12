import os
import shutil

from src.markdown_block import markdown_to_html_node


def copy_paste_content(from_folder, to_folder):
    if not os.path.exists(from_folder):
        raise Exception("Folder to copy not exist")

    if not os.path.isfile(from_folder):
        if not os.path.exists(to_folder):
            print("create directory:", to_folder)
            os.mkdir(to_folder)
        else:
            print("delete directory:", to_folder)
            shutil.rmtree(to_folder)
            print("create directory:", to_folder)
            os.mkdir(to_folder)
    else:
        print("copy file to directory", to_folder)
        shutil.copy(from_folder, to_folder)
        return

    for sub in os.listdir(from_folder):
        from_path = os.path.join(from_folder, sub)
        to_path = os.path.join(to_folder, sub)

        copy_paste_content(from_path, to_path)

def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception("Cannot find title")

    return markdown.split("\n")[0].removeprefix("# ")

def generate_page(from_path, template_path, dest_path):
    template = open(template_path)
    markdown = open(from_path)

    template_content = template.read()
    markdown_content = markdown.read()
    title = extract_title(markdown_content)
    html_content = markdown_to_html_node(
        markdown_content).to_html()

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    f = open(os.path.join(dest_path, "index.html"), "w+")

    f.write(template_content)

    template.close()
    markdown.close()
    f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Folder content not exist")

    if not os.path.isfile(dir_path_content):
        if not os.path.exists(dest_dir_path):
            print("create directory:", dest_dir_path)
            os.mkdir(dest_dir_path)
    else:
        print("generate file to directory", dest_dir_path)
        generate_page(dir_path_content, template_path, os.path.dirname(dest_dir_path))
        return

    for sub in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, sub)
        to_path = os.path.join(dest_dir_path, sub)

        generate_pages_recursive(from_path, template_path, to_path)
