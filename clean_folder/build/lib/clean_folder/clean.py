import os
import shutil
import re
import sys
from pathlib import Path, PurePath
import normalize

extensions = {
    "archives": ['ZIP', 'GZ', 'TAR'],
    "video": ['AVI', 'MP4', 'MOV', 'MKV'],
    "audio": ['MP3', 'OGG', 'WAV', 'AMR'],
    "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PAGES'],
    "images": ['JPEG', 'PNG', 'JPG', 'SVG'],
    "unknown": []
}

processed_extentions = set()
unknown_extentions = set()

def unpack(archive_path, path_to_unpack):
    shutil.unpack_archive(archive_path, path_to_unpack)
    archive_path.unlink()


def mk_dir(path):
    for ext in extensions:
        dir_img = path / ext
        dir_img.mkdir(exist_ok=True)


def rename_dir(str_path):
    p = Path(str_path)
    for dir in p.iterdir():
        if dir.is_dir() and dir.stem not in extensions:
            rename_dir(str(dir))
            if not re.match(r"^\w+$", dir.stem):
                norm_path = Path(str(PurePath(dir).with_stem(normalize(dir.stem))))
                norm_path.mkdir(exist_ok=True)
                for el in dir.iterdir():
                    el.rename(norm_path.joinpath(el.name))


def rename_files(str_path):
    p = Path(str_path)
    for i in p.glob('**/*.*'):
        if not re.match(r"^\w+$", i.stem):
            norm_path = Path(str(PurePath(i).with_stem(normalize(i.stem)).with_suffix(i.suffix)))
            i.rename(norm_path)


def sort_files(path_dir, sort_dir):
    p = Path(path_dir)
    for i in p.iterdir():

        if i.is_dir() and i.stem not in extensions:
            sort_files(str(i), sort_dir)

        unknw = True

        for ext in extensions:
            dir_img = sort_dir / ext

            if i.suffix.upper().removeprefix('.') in extensions[ext]:
                dir_img = sort_dir / ext

                if ext == "archives" :
                    unpack(i, dir_img.joinpath(i.stem))
                else:
                    i.rename(dir_img.joinpath(i.name))

                processed_extentions.add(i.suffix)
                unknw = False

        if unknw and len(str(i.suffix)) > 0:
            unknown_extentions.add(i.suffix)
            i.rename(dir_img.joinpath(i.name))


def del_empty_dir(dir_path_str):
    for dirs in os.listdir(dir_path_str):
        dir = os.path.join(dir_path_str, dirs)
        if os.path.isdir(dir):
            del_empty_dir(dir)
            if not os.listdir(dir):
                os.rmdir(dir)


def print_res(p):
    print('\nFiles in the new folders:')
    for ext in extensions:
        print('\n' + ext)
        p_dir = p + '/' + ext
        if Path(p_dir).is_dir() and os.listdir(p_dir):
            ld = os.listdir(p_dir)
            for el in ld:
                print(el)
        else:
            print('no files')
    print('\nList of processed extensions: ') 
    for el in processed_extentions:
        print(el)
    print('\nList of unknown extensions: ')
    for el in unknown_extentions:
        print(el)


def main():
    if len(sys.argv)>1:
        sort_path_str = sys.argv[1]
    else:
        print("Please enter the folder path")
        return

    try:
        sort_path = Path(sort_path_str)
        if_ex = sort_path.is_dir()
    except AttributeError:
        print('Error')
        return

    if if_ex:
        mk_dir(sort_path)
        sort_files(sort_path_str, sort_path)
        rename_files(sort_path_str)
        rename_dir(sort_path_str)
        del_empty_dir(sort_path_str)
        print_res(sort_path_str)
    else:
        print("The folder doesn't exist, please enter the correct folder path")
    

if __name__ == "__main__":
    main()