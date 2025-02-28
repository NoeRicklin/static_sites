from textnode import TextNode, TextType, generate_pages_recursive
import os
import shutil
import sys


content_path = "content"
static_path = "static"
template_path = "template.html"
docs_path = "docs"


def main():
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "./"
    src_to_dst(static_path, docs_path, basepath)
    generate_pages_recursive(content_path, template_path, docs_path, basepath)


def src_to_dst(src_path, dst_path, basepath):
    if not os.path.exists(basepath + "/" + src_path):
        raise Exception("Invalid path")
    shutil.rmtree(basepath + "/" + dst_path)
    shutil.copytree(basepath + "/" + src_path, basepath + "/" + dst_path)


main()

