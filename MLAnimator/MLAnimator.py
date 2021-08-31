# Sorts images made from BigSleep and DeepDaze into folders, and creates an animation from the files
# Animation outputs to current directory
# Animation frames can be selected in various ways:
# Using --frames (-f <number>), frames are selected from the most recent iterations. Including a starting_frame will select the most recent frames starting with the number of the selected frame.
# Using --starting_frame (-sf <number>), frames are selected from the selected number as its starting point. this will add the rest of the higher numbered frames, or a number of frames specified by --frames.
# Using --reverse (-r), animation will be reversed
# Using --mirror (-m), animation will include mirrored file list appending (mirrored file list makes the looping animation seemless, but doubles the file size)
# Using --info (-i), the frame information will be added to the file name

from os import listdir, mkdir, path, rename, scandir, getcwd
from os.path import isfile, join, splitext
import sys
import subprocess
import argparse
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

image_file_types = ['png', 'jpg']

class MLAnimator:
    def __init__(self, dir, framerate, starting_frame, frames, filetype, animate, reverse, mirror_list, info, all, Render_Frame_Text=False):
        animator_output_path = path.join(getcwd(), "AnimatorOutput")

        if framerate < 1:
            print("Invalid framerate.")
            return

        # Get all directories to check if they are sorted image folders
        dirs = [f for f in scandir(dir) if f.is_dir() and f.name != "Unsorted_Files"]

        # get list of files in the selected directory if they are a compatible file type
        files = self.confirm_files(dir)

        if not path.exists(animator_output_path):
            print("Creating main output folder at " + str(animator_output_path))
            mkdir(animator_output_path)

        self.animator_output_path = animator_output_path

        if not all:
            if starting_frame:
                if not starting_frame.isnumeric():
                    print("Invalid starting frame selection.")
                    return
                starting_frame = int(starting_frame)
                if starting_frame < 1:
                    starting_frame = 1

            if frames:
                if not frames.isnumeric() or int(frames) < 1:
                    print("Invalid frame selection.")
                    return
                frames = int(frames)

        sorted_folder = True

        # if there are files, then check to see if this is a sorted frame folder
        if len(files) > 0:
            # if there are no directories, check to see if the pictures are in numbered order
            if len(dirs) == 0:
                lastname = None
                for f in files:
                    checkedname = self.get_filename(f)
                    if checkedname:
                        if lastname and checkedname != lastname:
                            sorted_folder = False
                            break

                        lastname = checkedname

                    if not checkedname:
                        sorted_folder = False
                        break

            else: sorted_folder = False
            # If this is the sorted folder, do not sort again. Produces an animation file in its base directory's output folder
            if sorted_folder:
                if animate:
                    diroutname = path.basename(path.dirname(
                        path.dirname(dir))) + "_" + filetype + "_output"
                    self.create_animation_file(dirs, dir, self.get_filename(files[0]), framerate, frames, filetype, starting_frame, mirror_list, reverse, diroutname, info, all,Render_Frame_Text)
                    print("Animation file completed.")
                    return
            if not sorted_folder:
                for f in files:
                    # if filename is valid
                    filename = self.get_filename(f)
                    if filename:
                        self.sort_unsorted_image(dir, f, filename)
                    # if get_filename returns None, the file will be sorted with the other misc images
                    else:
                        print(f"Sorting misc image {f}")
                        self.move_misc_image(dir, f)

        if not animate:
            print("Files are in sorted folders.")
            return

        # Produces a folder of animation files in the main output directory.
        dirs = [f for f in scandir(dir) if f.is_dir() and f.name != "Unsorted_Files"]
        if len(dirs) > 0:
            basename = path.basename(dir)
            if basename == "":
                dir = path.basename(getcwd())
            diroutname = path.basename(dir) + "_" + filetype + "_output"
            for d in dirs:
                files = [f.name for f in scandir(d) if isfile(
                    join(d, f.name)) and f.name.split(".")[-1] in image_file_types]
                # Creates animation file if directory's contents are numbered frames.
                if len(files) > 2:
                    self.create_animation_file(dirs, d.path, d.name, framerate, frames, filetype,
                                          starting_frame, mirror_list, reverse, diroutname, info, all, Render_Frame_Text)
                    print("Animation file completed.")
                    continue

                print("No appropriate file list in %s" % (d))

    def create_animation_file(self, dirs, dirpath, dirname, framerate, frames, filetype, starting_frame, mirror_list, reverse, diroutname, info, all, Render_Frame_Text):

        diroutpath = self.set_sorted_folder(diroutname, filetype)
        files = []

        for f in scandir(dirpath):
            if isfile(f.path):
                checkedname = self.get_filename(f.name)
                if checkedname != None and checkedname == dirname and f.name.split('.')[-1] in image_file_types:
                    files.append(path.join(dirpath, f.name))

        files = sorted(files, key=lambda f: self.get_file_num(f, len(files)))
        if len(files) > 0:
            framefiletype = path.splitext(files[0])[1]

        # this is to fix file paths that include Windows styled paths and apostrophes
        files = [self.escape_str(f) for f in files]

        filename = dirname
        file_entry = "%s.%s" % (filename, filetype)
        frames_ready = False
        outpath = path.join(diroutpath, file_entry)

        # ask to overwrite before new frames are set
        if not all and not self.confirm_file_changes(outpath):
            print("Didn't confirm: %s" % outpath)
            return

        # sets to max
        if all:
            size = len(files)
            self.set_info(dirname, starting_frame=1, length=size, frames=size)
            frames_ready = True

        # using default settings lets user select frames
        elif not frames and not starting_frame:
            self.set_info(dirname, length=len(files))
            frames_ready = self.set_frame_amt()

        # non default sets any uninitialized setting to its max amount
        else:
            if not frames:
                if starting_frame:
                    frames = len(files) - starting_frame
                else:
                    frames = len(files)
            if not starting_frame:
                starting_frame = len(files) - frames + 1


            self.set_info(dirname, int(starting_frame), len(files), int(frames))
            print(f"frames: {self.frames}, start: {self.starting_frame}")
            frames_ready = self.check_valid_frames()

            # if frames didn't validate, ask to manually set
            if not frames_ready:
                select = input("Set new frame values for %s? (y/n) : " % dirname)
                if select.strip().lower() in ("y", "yes", ""):
                    frames_ready = self.set_frame_amt()

        # return if user canceled out of setting frames loop
        if not frames_ready:
            print("Skipping animation of %s." % (self.name))
            return

        # attach frame settings to filename if --info is set
        if info:
            filename = "%s(sf%d_f%d_fr%d)" % (
                dirname, self.starting_frame, self.frames, framerate)
            # outpath = path.join(diroutpath, filename + "." + filetype)

            # ask to overwrite before creating duplicate animation
            if not all and not self.confirm_file_changes(outpath):
                print("Skipping animation: %s" % self.name)
                return

        outpath = self.set_valid_filename(diroutpath, filename, filetype, 0)

        starting_frame = self.starting_frame - 1
        end_frame = self.frames + starting_frame
        print(f"end_frame: {end_frame}")
        file_list = files[starting_frame:end_frame]
        if reverse:
            file_list = [ele for ele in reversed(file_list)]

        # create animation file for the frames collected from dirpath
        self.run_FFMPEG(file_list, dirpath, end_frame, outpath, framerate, mirror_list)

        if Render_Frame_Text:
            outpathdirs = listdir(diroutpath)
            framesWithTextDir = self.set_valid_dirname(dirs, dirpath, filename + "_frameTextRendered")
            # framesWithTextDir = self.set_valid_dirname(outpathdirs, dirpath, filename + "_frameTextRendered", 0)
            print("framesWithTextDir: " + framesWithTextDir)
            fontPath = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
            i = 0
            for img_file in file_list:
                with Image.open(img_file) as img:
                    newfilename = self.image_output_path(framesWithTextDir, sequence_number=i)
                    print("newfilename: " + str(newfilename))
                    img = img.convert('RGB')
                    font = ImageFont.truetype(fontPath, 30)
                    txt = "Frame: " + str(i)
                    i += 1
                    draw = ImageDraw.Draw(img)
                    draw.text((img.size[0]/20, 0), txt, (0,0,0), font=font)
                    img.save(newfilename)

            # TODO: Change frame output to Output_directory, change animation output dir

            # dirpath => content/VQGAN_Output
            # newdirpath = self.set_valid_dirname(dirs, dirpath, )

            newdirpath = self.set_valid_dirname(dirs, dirpath, filename + "_frameTextRendered", 0)
            newoutpath = self.set_valid_filename(diroutpath, filename, filetype, 0)

            self.run_FFMPEG(file_list, newdirpath, end_frame, newoutpath, framerate, mirror_list)


    def run_FFMPEG(self, file_list, dirpath, end_frame, outpath, framerate, mirror_list):
        filelistpath = path.join(dirpath, "filelisttoanimation.txt")
        with open(filelistpath, "w", encoding="utf-8") as txtfile:
            for image in file_list:
                txtfile.write("file \'" + image + "\'\n")

            if mirror_list:
                reversed_list = [ele for ele in reversed(file_list)][1:]
                for image in reversed_list[:-1]:
                    txtfile.write("file \'" + image + "\'\n")

        listpath = self.escape_str(filelistpath)

        print("Animating: %s\nStarting frame: %d\nEnd Frame: %d\nFile List Length: %d\nSaving file to: %s" % (
            self.name, self.starting_frame, end_frame, self.frames, outpath))
        outpathStr = self.escape_str(outpath)

        cmdargs = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-r',
                   str(framerate), '-f', 'concat', '-safe', "0", '-i', listpath, outpathStr]
        subprocess.call(cmdargs)

    def set_valid_dirname(self, dirs, out, basename, i=0):
        if i > 0:
            newname = "%s(%d)" % (basename, i)
        else:
            newname = basename

        unique_dir_name = True

        if len(dirs) < 1:
            new_path = path.join(out, newname)
            mkdir(new_path)
            return new_path

        for dir in dirs:
            if path.basename(dir) == newname:
                unique_dir_name = False
                break

        if unique_dir_name:
            print(f"out: {out}\nnewname: {newname}")
            new_path = path.join(out, newname)

            mkdir(new_path)
            return new_path

        return self.set_valid_dirname(dirs, out, basename, i + 1)

    def get_filename(self, filename):
        namestr = filename.split(".")
        if namestr[len(namestr) - 2].isnumeric():
            return "".join(namestr[:-2])
        return None

    def get_file_num(self, f, lastnum):
        namestr = f.split(".")
        if namestr[-2].isnumeric():
            return int(namestr[-2])

    def get_frame_input(self, amt, max):
        if amt.strip() == "":
            return 0
        starting_frame = int(max) - int(amt)
        if starting_frame < 0:
            return -1

        return starting_frame

    def sort_unsorted_image(self, dir, f, sortedname):
        sortedpath = path.join(dir, sortedname)
        unsortedfile = path.join(dir, f)
        if not path.exists(sortedpath):
            mkdir(sortedpath)
        rename(unsortedfile, path.join(sortedpath, f))

    def set_valid_filename(self, filepath, basename, filetype, i):
        if i > 0:
            newname = "%s(%d)" % (basename, i)
        else:
            newname = basename

        newpath = "%s.%s" % (newname, filetype)
        filename = path.join(filepath, newpath)
        if isfile(filename):
            return self.set_valid_filename(filepath, basename, filetype, i + 1)

        return filename

    def confirm_file_changes(self, outpath):
        if isfile(outpath):
            confirmed = input(
                "\nAnimation file found: %s\n\nDo you wish to make another? (y/n) : " % outpath)
            if confirmed.strip().lower() in ("y", "yes"):
                return True

            return False

        # Safe to write file
        return True

    def confirm_files(self, dir):
        return [f.name for f in scandir(dir) if isfile(join(dir, f.name)) and f.name.split(".")[-1] in image_file_types]

    def move_misc_image(self, dir, filename):
        oldpath = path.join(dir, filename)
        unsorteddir = path.join(dir, "Unsorted_Files")
        if not path.exists(unsorteddir):
            mkdir(unsorteddir)
        rename(oldpath, path.join(unsorteddir, filename))

    def escape_str(self, a_str):
        return a_str.replace("\\", "\\\\").replace("\'", r"\'")

    def set_info(self, name, starting_frame=None, length=None, frames=None):
        self.name = name
        self.starting_frame = starting_frame
        self.length = length
        self.frames = frames

    def set_frame_amt(self):
        print("\nName: %s" % self.name)
        print("\nEntering new frame amount (MAX FRAMES: %d)\n(Entering nothing selects max frames | Enter 's' to skip animation)\n" % self.length)
        try:
            while True:
                max = self.length
                newframes = None

                frames = input("Enter amount of frames: ").strip()
                if not frames in ("", None):
                    if not frames.isnumeric():
                        return False
                    frames = int(frames)
                    if frames < 1:
                        print("Invalid frame amount.")
                        continue
                    if frames > self.length:
                        print("\nToo many frames selected. (Max: %d)\n" %
                              self.length)
                        continue

                    newframes = frames
                    max = self.length - frames + 1

                if self.set_starting_frame(max, newframes):
                    if newframes:
                        self.frames = newframes
                    else:
                        self.frames = self.length - self.starting_frame + 1
                    return True

                if frames <= 1:
                    print("\nMust have more than one frame to animate.\n")

        except ValueError:
            print("\nValue Error when setting frame amount.\n")
            return False

    def image_output_path(self, output_path, sequence_number=None):
        """
        Returns underscore separated Path.
        A current timestamp is prepended if `self.save_date_time` is set.
        Sequence number left padded with 6 zeroes is appended if `save_every` is set.
        :rtype: Path
        """
        base = path.basename(output_path)
        if sequence_number:
            sequence_number_left_padded = str(sequence_number).zfill(6)
            newname = f"{base}.{sequence_number_left_padded}"
        else:
            newname = base
        output_path = path.join(output_path, newname)
        return Path(f"{output_path}.png")

    def set_starting_frame(self, max, newframes):
        if not newframes:
            tip = "Entering nothing uses all frames."
        else:
            tip = "Entering nothing sets starting frame as high as possible."

        print("\nSelect starting frame (MAX #: %d)\n(%s | Enter 's' to go back to set frame amount)\n" % (max, tip))
        try:
            while True:
                starting_frame = input(
                    "Enter starting frame selection: ").strip()
                if starting_frame in ("", None):
                    if not newframes:
                        self.starting_frame = 1
                    else:
                        self.starting_frame = max
                    return True

                elif not starting_frame.isnumeric():
                    return False

                starting_frame = int(starting_frame)
                if starting_frame < 1:
                    print("Invalid starting frame.")
                    continue

                if starting_frame > max:
                    print("%s Error: Cannot render %d frames from starting image %d (Image amount: %d)" % (
                        self.name, self.length - starting_frame, starting_frame, self.length))
                    continue

                self.starting_frame = starting_frame
                return True

        except ValueError:
            print("Value error getting starting frame.")
        return False

    def check_valid_frames(self):
        # default frame count is distance from starting_frame to highest numbered frame.
        if not self.frames:
            if not self.starting_frame:  # both default settings mean to use all the frames
                self.starting_frame = 1
                self.frames = self.length
                return True
        if self.frames >= self.length:
            print(f"Selected too many frames from: {self.name}")
            select = input("Set to max frame amount %d? (y/n): " % (self.length))
            if select.strip().lower() in ("yes", "y"):
                self.starting_frame = 1
                self.frames = self.length
                return True
            return False
        if not self.starting_frame:  # default starting frame is highest numbered image minus the amount of frames
            self.starting_frame = self.length - self.frames + 1
            return True
        if self.starting_frame > self.length:
            print(f"ERROR: {self.name}")
            print("Invalid starting frame; must be below max size of %d." % (self.length))
            return False
        if self.frames + self.starting_frame - 1 > self.length:
            print(f"ERROR: {self.name}")
            print(
                "Starting Frame + Frame Amount incompatible with max frame size of %d." % (self.length))
            return False
        if self.starting_frame < 0:
            self.starting_frame = 1
        return True

    def set_sorted_folder(self, diroutname, filetype):
        diroutpath = path.join(self.animator_output_path, diroutname)
        if not path.exists(diroutpath):
            print("Creating sorted folder for " + str(diroutpath))
            mkdir(diroutpath)
        return diroutpath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make gifs of image lists in directories")
    parser.add_argument("-dir", "--dir", metavar="./dir/path", help="starting directory to check for files")
    parser.add_argument("-fr", "--framerate", metavar="20", help="framerate to be used by FFMPEG", default=14)
    parser.add_argument("-sf", "--starting_frame", metavar="5", help="frame to start on")
    parser.add_argument("-f", "--frames", metavar="50", help="frame amount to render")
    parser.add_argument("-ft", "--filetype", metavar="mp4", help="output file type", default="mp4")
    parser.add_argument("-s", "--sort_only", action="store_true", help="turn off ffmpeg animation")
    parser.add_argument("-r", "--reverse", action="store_true", help="turn off ffmpeg animation")
    parser.add_argument("-m", "--mirror", action="store_true", help="Turn on mirrored animation (seemless looping, but double filesize)")
    parser.add_argument("-i", "--info", action="store_true", help="add frame info to filename")
    parser.add_argument("-a", "--all", action="store_true", help="use all frames available in animation")
    parser.add_argument("-rt", "--rendertext", action="store_true", help="create a separate animation of images with frame info rendered on the image")
    args = parser.parse_args()
    MLAnimator(args.dir, int(args.framerate), args.starting_frame, args.frames, args.filetype, not args.sort_only, args.reverse, args.mirror, args.info, args.all, Render_Frame_Text=args.rendertext)
