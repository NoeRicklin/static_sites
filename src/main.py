from textnode import TextNode, TextType, generate_pages_recursive
import os
import shutil


content_path = "/home/noeri/workspace/github.com/NoeRicklin/static_sites/content"
static_path = "/home/noeri/workspace/github.com/NoeRicklin/static_sites/static"
template_path = "/home/noeri/workspace/github.com/NoeRicklin/static_sites/template.html"
public_path = "/home/noeri/workspace/github.com/NoeRicklin/static_sites/public"


def main():
    src_to_dst(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path)


def src_to_dst(src_path, dst_path):
    if not os.path.exists(src_path):
        raise Exception("Invalid path")
    shutil.rmtree(dst_path)
    shutil.copytree(src_path, dst_path)


main()

