import glob
import time
import os
import re

def move_extensions_to_folder(extensions_list, files, path):
    """Move files with the given extensions to a folder with the same name as the extension.

    Args:
        extensions (list): List of extensions to move.
        files (list): List of files to check.
        path (str): Path to the directory to move files to.
    """

    for f in files:
        ext = filename_to_ext[f]
        if ext not in extensions_list:
            continue
        if args.use_modified_time:
            t = time.localtime(os.path.getmtime(f))
            year = t.tm_year
            month = t.tm_mon
            day = t.tm_mday
            hour = t.tm_hour
            minute = t.tm_min
            second = t.tm_sec
        else:
            # use regex yyyy-mm-dd in filename to extract date
            m = re.search(r'(\d{4})-(\d{2})-(\d{2})', f)
            if m is None:
                raise Exception(f'Cannot find date in filename {f}')
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            hour = 0
            minute = 0
            second = 0
        new_filename = f'{year}{month:02d}{day:02d}_{hour:02d}{minute:02d}{second:02d}_{os.path.basename(f)}'
        new_path = f'{path}/{year}/{new_filename}'
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        os.rename(f, new_path)

    

# get path from command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="path to the folder containing the files", type=str, required=True)
parser.add_argument("-m", "--use_modified_time", help="use modified time instead of created time", type=bool, default=False)
parser.add_argument("-o", "--output_path", help="path to the folder to move files to", type=str, default="./")
args = parser.parse_args()

t0 = time.time()
files = glob.glob(f'{args.path}/**/*', recursive=True)
search_time = time.time() - t0

# filter out folder
files = [f for f in files if not os.path.isdir(f)]

# find out file extensions
filename_to_ext = {}
for f in files:
    ext = f.split('.')[-1]
    filename_to_ext[f] = ext
# count number of files for each extension
ext_to_count = {}
for ext in filename_to_ext.values():
    if ext not in ext_to_count:
        ext_to_count[ext] = 0
    ext_to_count[ext] += 1

# print sorted by number of occurrences
print('File extensions:')
for ext, count in sorted(ext_to_count.items(), key=lambda x: x[1], reverse=True):
    print(ext, count)

# sort files by modification time
files.sort(key=lambda x: os.path.getmtime(x))

move_extensions_to_folder(['jpg', 'jpeg', 'png', 'gif', 'bmp'], files, f'{args.output_path}images')
move_extensions_to_folder(['aac', '3gp', 'mp4', 'mov', 'MOV', 'avi', 'mkv', 'mpg', 'mpeg'], files, f'{args.output_path}videos')
move_extensions_to_folder(['amr', 'mp3', 'caf', 'wav', 'ogg', 'flac', 'm4a', 'opus'], files, f'{args.output_path}audio')
move_extensions_to_folder(['pdf', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt'], files, f'{args.output_path}documents')
move_extensions_to_folder(['vcf'], files, f'{args.output_path}contacts')
move_extensions_to_folder(['thumb'], files, f'{args.output_path}thumbnails')

# move all images to ./images/{image_creation_year} and rename them to yearmonthday_hourminsec_{original_filename}
print(f'Found {len(files)} files in {search_time:.2f} seconds')