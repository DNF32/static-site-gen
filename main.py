import os
import shutil
from os.path import isfile


def copy_tree(source: str, dst: str, current_folder_tree: str):
    if os.path.isfile(source):
        
        dir_path = os.path.dirname(path).split(source, 1)[1]

        path = os.path.join(dst,)
        path = os.path.join(dst, current_folder_tree, os.path.basename())
    for path in os.listdir(source):
        path = os.path.join(source, path)
        if os.path.isfile(path):
            dir_path = os.path.dirname(path).split(source, 1)[1]
            dir_path_dst = os.path.join(dst, dir_path)
            if not os.path.exists(dir_path_dst):
                os.mkdir(dir_path_dst)
            shutil.copy(path, dir_path_dst)
        copy_tree(path, dst)


if __name__ == "__main__":
    copy_tree(
        "/Users/danielfonseca/my-git/boot/static-site/static/",
        "/Users/danielfonseca/my-git/boot/static-site/test/",
    )
