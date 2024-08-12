from src.generate_content import copy_paste_content, generate_page


def main():
    # copy_paste_content("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public")
main()