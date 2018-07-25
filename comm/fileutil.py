#coding:utf-8

from __future__ import with_statement

import os, stat, time, shutil
import time
current_milli_time = lambda: int(round(time.time() * 1000))
def get_files(dir):
    """获取一个文件夹下的所有文件"""
    if not dir or not os.path.isdir(dir):
        return []
    names = os.listdir(dir)
    files = []
    for name in names:
        name = os.path.join(dir, name)
        if os.path.isfile(name):
            files.append(name)
    return files

def walk_tree_files(dir):
    if dir and os.path.isdir(dir):
        for root, dirs, files in os.walk(dir):
            for name in files:
                yield os.path.join(root, name)

def walk_tree_dirs(dir):
    if dir and os.path.isdir(dir):
        for root, dirs, files in os.walk(dir):
            for name in dirs:
                yield os.path.join(root, name)

def count_files(path, ext=''):
    if os.path.isfile(path):
        return 1 if path.endswith(ext) else 0
    file_count = 0
    for filepath in walk_tree_files(path):
        if filepath.endswith(ext):
            file_count += 1
    return file_count

count_tree_files = count_files

def count_lines(path):
    count = 0
    if os.path.isdir(path):
        for filepath in walk_tree_files(path):
            count += count_lines(filepath)
    else:
        with open(path) as f:
            for line in f:
                count += 1
    return count

def get_ordered_tree_files(dir, asc = True):
    ordered_tree_files = list()
    for filepath in walk_tree_files(dir):
        ordered_tree_files.append(filepath)
    ordered_tree_files.sort(reverse = not asc)
    return ordered_tree_files
            
def get_dirs(dir):
    """获取一个文件夹下的所有文件"""
    if not dir or not os.path.isdir(dir):
        return []
    names = os.listdir(dir)
    files = []
    for name in names:
        name = os.path.join(dir, name)
        if os.path.isdir(name):
            files.append(name)
    return files

def get_tree_dirs(dir):
    return list(walk_tree_dirs(dir))

def get_tree_files(dir):
    return list(walk_tree_files(dir))

def ensure_dir_exists(*dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except OSError as e:
                if not e.args[0] in (183, 17):
                    raise

ensure_dirs_exists = ensure_dir_exists

def is_empty_dir(dir):
    files = get_tree_files(dir)
    try:
        files.next()
        return False
    except StopIteration:
        return True
    finally:
        files.close()

def remove_dir_tree(dir, include_self = True):
    if dir and os.path.isdir(dir):
        walker = os.walk(dir, False)
        for item in walker:
            for d in item[1]:
                p = os.path.join(item[0], d)
                os.rmdir(p)
            for f in item[2]:
                p = os.path.join(item[0], f)
                os.chmod(p, stat.S_IWUSR)
                os.remove(p)

        if include_self:
            os.rmdir(dir)

def get_dir_size(dir):
    if not dir or not os.path.exists(dir):
        return 0

    dir_size = 0

    walker = os.walk(dir, False)
    for item in walker:
        for file in item[2]:
            file_path = os.path.join(item[0], file)
            dir_size += os.path.getsize(file_path)
    return dir_size

def remove_empty_dir(dir, includeSelf = False):
    if not dir: return
    if not os.path.isdir(dir): return
    exceptions = ('.', '..')
    empty = True
    names = os.listdir(dir)
    for name in names:
        if name not in exceptions:
            name = os.path.join(dir, name)
            if os.path.isdir(name) and not remove_empty_dir(name, True):
                empty = False
                continue
            if os.path.isfile(name):
                empty = False
                break
    if includeSelf and empty:
        remove_dir_tree(dir)
        
    return empty

def remove_file_if_exists(filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        os.remove(filepath)
        
def get_file_mtime(filepath):
    return time.mktime(time.localtime(os.stat(filepath).st_mtime))  

def chmod(path, privilege):
    if os.path.isdir(path):
        for name in os.listdir(path):
            chmod(os.path.join(path, name), privilege)
    info = os.stat(path)
    if info.st_mode & privilege != privilege:
        os.chmod(path, info.st_mode | privilege)

def chmod_file_writable(path):
    chmod(path, stat.S_IWRITE)

def combine_text_files(input_filepaths, output_filepath, all_in_memory=False):
    temp_output_filepath = output_filepath + '.combine'
    with open(temp_output_filepath, 'w') as output_file:
        for input_filepath in input_filepaths:
            print('reading', input_filepath)
            with open(input_filepath) as input_file:
                if all_in_memory:
                    output_file.writelines(input_file.readlines())
                else:
                    line = input_file.readline()
                    while line:
                        output_file.write(line)
                        line = input_file.readline()
    shutil.move(temp_output_filepath, output_filepath)

def yield_lines(filepath):
    with open(filepath) as f:
        line = f.readline()
        while line:
            line = line.strip()
            if line:
                yield line
            line = f.readline()
            
def read_lines(filepath):
    return list(yield_lines(filepath))

def read_file(filepath):
    with open(filepath) as f:
        return f.read()


if __name__ == "__main__":
    import os
    os.chmod()
    dirpath = '/data/appdatas/cleanmaster_sync/stat_logs/packageintroquery/20131212'
    chmod(dirpath, 777)