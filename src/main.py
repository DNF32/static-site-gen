import os
import sys
from os.path import isfile
import re
import shutil
from converter import markdown_to_html_node


def copy_tree(source: str, dst: str) -> None:
    """
    Only produces side effect, we return the function call
    but it won't give nothing
    """
    shutil.rmtree(dst)

    def aux(source: str, dst: str):
        """
        source will be a full path
        dst will be a full path

        current_folder_tree vai ser so a base initial de onde comeca o dst
        - starts as "" and as we go deeper we had folder
        """
        if os.path.isfile(source):
            shutil.copy(source, dst)
            return

        for path in os.listdir(source):
            full_path = os.path.join(source, path)
            new_dst = os.path.join(dst, os.path.basename(source))
            if not os.path.exists(new_dst):
                os.mkdir(new_dst)
            aux(full_path, new_dst)
        return

    return aux(source, dst)


type Markdown = str


def extract_title(markdown: Markdown) -> str:
    # Assume title is the first line

    match = re.match(r"^# (.*)", markdown)
    if match:
        return match.group(1)
    raise Exception("There is no h1 header")


def generate_page(
    from_path: str, template_path: str, dest_path: str, dev=True, base_path="/"
):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as md_fd:
        md = md_fd.read()

    with open(template_path, encoding="utf-8") as tpl_fd:
        tpl = tpl_fd.read()

    title = extract_title(md)
    content_html_node = markdown_to_html_node(md)
    content_html = content_html_node.to_html()

    tpl.format(Title=title, Content=content_html)
    filled = tpl.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    if not dev:
        filled = tpl.replace('href="/', f'href="{base_path}').replace(
            'src="/', f'src="{base_path}'
        )

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    path = os.path.join(dest_path, "index.html")
    with open(path, "w", encoding="utf-8") as html:
        html.write(filled)

    return None


def generate_content(path: str, base_path="/", dev=True, serving_place="docs"):
    if os.path.isfile(path):
        dst = path.replace("content", f"{serving_place}")
        print(path)
        generate_page(
            path,
            "/home/dnf/code/static-site/template.html",
            os.path.dirname(dst),
            base_path=base_path,
            dev=dev,
        )
        return
    for listing in os.listdir(path):
        full_path = os.path.join(path, listing)
        generate_content(full_path)
    return


if __name__ == "__main__":
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    print(f"this is the path{base_path}")

    copy_tree(
        "/home/dnf/code/static-site/static/",
        "/home/dnf/code/static-site/docs/",
    )

    content_path = "/home/dnf/code/static-site/content/"
    generate_content(content_path, base_path=base_path, dev=False)
