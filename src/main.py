from textnode import TextNode, TextType
import os
import shutil
import markdown_helpers
import sys


def main():
    basepath = "/"
    serve_location = "./public"
    cliargs = sys.argv
    if len(cliargs) > 1:
        basepath = cliargs[1]
        serve_location = "./docs"
    print(basepath)

    copy_dir_contents("./static", serve_location)

    generate_page_recursive("./content", "./template.html", serve_location, basepath)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_contents = ""
    template_contents = ""
    with open(from_path) as f:
        markdown_contents = f.read()
        f.close()
    with open(template_path) as f:
        template_contents = f.read()
        f.close()

    markdown_html = markdown_helpers.markdown_to_html_node(markdown_contents).to_html()
    markdown_title = markdown_helpers.extract_title(markdown_contents)

    template_contents = template_contents.replace("{{ Title }}", markdown_title)
    template_contents = template_contents.replace("{{ Content }}", markdown_html)
    template_contents = template_contents.replace('href="/', f'href="{basepath}')
    template_contents = template_contents.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_contents)


def generate_page_recursive(
    from_path: str, template_path: str, dest_path: str, basepath
):
    if os.path.exists(from_path) is not True:
        raise FileNotFoundError(f"from directory {from_path} does not exist")
    if os.path.exists(template_path) is not True:
        raise FileNotFoundError(f"template path {template_path} does not exist")

    for item in os.listdir(from_path):
        item_path = os.path.join(from_path, item)
        if os.path.isfile(item_path) and item_path[-3:] == ".md":
            content_path = os.path.join(dest_path, item[:-3] + ".html")
            generate_page(item_path, template_path, content_path, basepath)
        else:
            content_new_dest_path = os.path.join(dest_path, item)
            generate_page_recursive(
                item_path, template_path, content_new_dest_path, basepath
            )


def copy_dir_contents(source_dir: str, dest_dir: str):
    if os.path.exists(source_dir) is not True:
        raise FileNotFoundError(f"static directory: {source_dir} was not found")

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)
        else:
            dest_path = os.path.join(dest_dir, item)
            os.mkdir(dest_path)
            copy_dir_contents(item_path, dest_path)


if __name__ == "__main__":
    main()
