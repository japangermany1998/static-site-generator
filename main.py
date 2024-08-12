from src.generate_content import copy_paste_content, generate_page, generate_pages_recursive


def main():
    copy_paste_content("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")

main()