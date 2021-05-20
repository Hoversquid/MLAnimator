# Sorts images made from BigSleep and DeepDaze into folders, and creates an animation from the files
# Animation outputs to current directory
# Animation frames can be selected in various ways:
    # Using --frames (-f <number>), frames are selected from the most recent iterations. Including a starting_frame will select the most recent frames starting with the number of the selected frame.
    # Using --starting_frame (-sf <number>), frames are selected from the selected number as its starting point. this will add the rest of the higher numbered frames, or a number of frames specified by --frames.
    # Using --reverse (-r), animation will be reversed
    # Using --no_mirror (-nm), animation will not include mirrored file list appending (mirrored file list makes the looping animation seemless, but doubles the file size)

from os import listdir, mkdir, path, rename, scandir, getcwd
from os.path import isfile, join
import argparse
import sys
import subprocess

image_file_types = ['png', 'jpg']

class MLAnimator:
    def __init__(self, name, starting_frame=None, length=None, frames=None):
        self.name = name
        self.starting_frame = starting_frame
        self.length = length
        self.frames = frames

    def set_frame_amt(self, max):
        print("\nEntering new frame amount (MAX FRAMES: %d)\n(Entering nothing selects max frames | Enter 's' to reselect starting frame)\n" % (max))
        frames = input("Enter amount of frames: ")
        try:
            frames = frames.strip()
            if frames in ("", None):
                self.frames = max
                return True
            if not frames.isnumeric():
                return False

            frames = int(frames)
            if frames > 1 and max >= frames:
                self.frames = frames
                return True

            if frames <= 1:
                print("Must have more than one frame to animate.")
                return False

        except ValueError:
            print("Value Error when setting frame amount.")

        return False

    def set_frame_info(self):
        print("\nSelect starting frame (MAX FRAMES: %d)\n(Entering nothing sets default | Enter 's' to skip this animation)\n" % (self.length))
        starting_frame = input("Enter starting frame selection: ")
        try:
            starting_frame = starting_frame.strip()
            if starting_frame in ("", None):
                if not self.set_frame_amt(self.length):
                    return False
                self.starting_frame = self.length - self.frames + 1
                return True
            elif not starting_frame.isnumeric():
                return None

            starting_frame = int(starting_frame)
            if starting_frame > 0 and self.length > starting_frame:
                self.starting_frame = starting_frame
                if self.set_frame_amt(self.length - self.starting_frame):
                    return True
                return False

            print("Invalid starting frame.")
            return False

        except ValueError:
            print("Value error getting starting frame.")
        return False

    def set_new_values(self):
        select = input("Set new frame values for %s? (y/n) : " % self.name)
        if select.strip().lower() in ("y", "yes", ""):
            values_set = False
            while not values_set:
                values_set = self.set_frame_info()
                if values_set == None:
                    print("Animation skipped.")
                    return None
            return True
        return None

    def check_valid_frames(self):
        if self.starting_frame == None:
            if self.frames == None:
                self.starting_frame = 1
                self.frames = self.length
                return True
        if self.starting_frame >= self.length:
            print("Invalid starting frame; must be below %d." % (self.length))
            return False
        if self.frames == None:
            frames = self.length - self.starting_frame
            return True
        if self.frames > self.length:
            print("Invalid frame amount; must be below max size of %d." % (self.length))
            return False
        if self.frames + self.starting_frame > self.length:
            print("Starting Frame + Frame Amount incompatible with max frame size of %d." % (self.length))
            return False
        if self.starting_frame < 0:
            self.starting_frame = 1
        return True

    def set_valid_frames(self):
        frames_ready = False
        while not frames_ready:
            frames_ready = self.set_new_values()
            if frames_ready == None:
                return False
        return True

def process_files():
    parser = argparse.ArgumentParser(description="Make gifs of image lists in directories")
    parser.add_argument("-dir", "--dir", metavar="./dir/path", help="starting directory to check for files")
    parser.add_argument("-fr", "--framerate", metavar="20", help="framerate to be used by FFMPEG", default=14)
    parser.add_argument("-sf", "--starting_frame", metavar="5", help="frame to start on")
    parser.add_argument("-f", "--frames", metavar="50", help="frame amount to render")
    parser.add_argument("-ft", "--filetype", metavar="gif", help="output file type", default="gif")
    parser.add_argument("-da", "--dont_animate", action="store_true", help="turn off ffmpeg animation")
    parser.add_argument("-r", "--reverse", action="store_true", help="turn off ffmpeg animation")
    parser.add_argument("-nm", "--no_mirror", action="store_true", help="turn off appending mirrored animation")

    args = parser.parse_args()
    dir = args.dir
    framerate = args.framerate
    starting_frame = args.starting_frame
    frames = args.frames
    filetype = args.filetype
    animate = not args.dont_animate
    reverse = args.reverse
    mirror_list = not args.no_mirror

    animator_output_path = path.join(getcwd(), "AnimatorOutput")

    if not path.exists(animator_output_path):
        print("Creating output folder at " + str(animator_output_path))
        mkdir(animator_output_path)

    if starting_frame:
        if not starting_frame.isnumeric():
            print("Invalid starting frame selection.")
            return
        if int(starting_frame) < 1:
            starting_frame = 1

    if frames:
        if not frames.isnumeric() or int(frames) < 1:
            print("Invalid frame selection.")
            return

    # get list of files in the selected directory if they are a compatible file type
    files = [f.name for f in scandir(dir) if isfile(join(dir, f.name)) and f.name.split(".")[-1] in image_file_types]

    if len(files) > 0:
        new_dirs = []
        file_listing = []
        collected_files = []
        nametomatch = get_filename(files[0])
        collected_files.append(files[0])

        # sorts files by file name into separate folders
        for f in files[1:]:
            checkedname = get_filename(f)
            if nametomatch == checkedname:
                collected_files.append(f)
            elif checkedname != None:
                file_listing.append(collected_files)
                new_dirs.append(nametomatch)
                nametomatch = checkedname
                collected_files = [f]

        # append last file set
        file_listing.append(collected_files)
        new_dirs.append(nametomatch)

        # Get all directories to check if they are sorted image folders
        dirs = [f for f in scandir(dir) if f.is_dir()]

        # If this is the sorted folder, do not sort again. Produces an animation file in the current directory and stops.
        if len(dirs) == 0 and len(new_dirs) == 1:
            if animate:
                outpath = path.join(animator_output_path, new_dirs[0] + "." + filetype)
                create_animation_file(dir, new_dirs[0], framerate, frames, filetype, starting_frame, mirror_list, reverse, outpath)
                return

            print("Files are in sorted folder and no action taken.")

        # If this folder contains more than one set of images, it will sort them into folders.
        else:
            dirrange = range(len(new_dirs))
            for i in dirrange:
                newpath = path.join(str(dir), str(new_dirs[i]))
                if not path.exists(newpath):
                    print("Creating sorted folder for " + str(newpath))
                    mkdir(newpath)
                for f in file_listing[i]:
                    filepath = path.join(dir, f)
                    rename(filepath, path.join(newpath, f))

    # Produces a folder of animation files in the current directory.
    if animate:
        dirs = [f for f in scandir(dir) if f.is_dir()]
        diroutname = path.basename(path.dirname(dir)) + "_" + filetype + "_output"
        if len(dirs) > 0:
            diroutpath = path.join(animator_output_path, diroutname)
            if not path.isdir(diroutpath): mkdir(diroutpath)
            for d in dirs:
                filelist_test = [f.name for f in scandir(d) if isfile(join(d, f.name)) and f.name.split(".")[-1] in image_file_types]
                if len(filelist_test) > 2:
                    outpath = path.join(diroutpath, d.name + "." + filetype)
                    create_animation_file(d.path, d.name, framerate, frames, filetype, starting_frame, mirror_list, reverse, outpath)
                else:
                    print("No appropriate file list in %s" % (d))

def get_filename(filename):
    namestr = filename.split(".")
    if namestr[len(namestr)-2].isnumeric():
        return "".join(namestr[:-2])
    return None

def get_file_num(f, lastnum):
    namestr = f.split(".")
    if namestr[-2].isnumeric():
        return int(namestr[-2])

def get_frame_input(amt, max):
    if amt.strip() == "":
        return 0
    starting_frame = int(max) - int(amt)
    if starting_frame < 0:
        return -1

    return starting_frame

def create_animation_file(dirpath, dirname, framerate, frames, filetype, starting_frame, mirror_list, reverse, outpath):
    files = []
    for f in scandir(dirpath):
        if isfile(f.path):
            checkedname = get_filename(f.name)
            if checkedname != None and checkedname == dirname and f.name.split('.')[-1] in image_file_types:
                files.append(path.join(dirpath, f.name))

    files = sorted(files, key=lambda f: get_file_num(f, len(files)))

    # this is to fix file paths that include Windows styled paths and apostrophes
    files = [escape_str(f) for f in files]
    frames_ready = False

    if not frames and not starting_frame:
        animator = MLAnimator(dirname, length=len(files))
        frames_ready = animator.set_valid_frames()
    else:
        if frames == None:
            frames = len(files)
        if starting_frame == None:
            starting_frame = len(files) - int(frames)

        animator = MLAnimator(dirname, int(starting_frame), len(files), int(frames))
        frames_ready = animator.check_valid_frames()
        if not frames_ready:
            frames_ready = animator.set_valid_frames()

    if not frames_ready:
        print("Skipping animation of %s" % (dirname))
        return

    starting_frame = animator.starting_frame - 1
    end_frame = animator.frames + starting_frame - 1
    file_list = files[starting_frame:end_frame]
    if reverse: file_list = [ele for ele in reversed(file_list)]

    filelistpath = path.join(dirpath, "filelisttoanimation.txt")
    with open(filelistpath, "w", encoding="utf-8") as txtfile:
      for image in file_list:
        txtfile.write("file \'"+image+"\'\n")

      if mirror_list:
        reversed_list = [ele for ele in reversed(file_list)][1:]
        for image in reversed_list[:-1]:
            txtfile.write("file \'"+image+"\'\n")

    listpath = path.join(dirpath, "filelisttoanimation.txt")
    listpath = escape_str(listpath)

    outpath = escape_str(outpath)
    print("Animating", outpath, "from frame", str(animator.starting_frame), "to frame", str(animator.starting_frame + animator.frames), "from a file list of", str(animator.length))
    cmdargs = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-r', str(framerate), '-f', 'concat', '-safe', "0", '-i', listpath, outpath]
    subprocess.call(cmdargs)

def escape_str(a_str):
    return a_str.replace("\\", "\\\\").replace("\'", r"\'")

if __name__ == "__main__":
    process_files()
