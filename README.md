# MLAnimator
 Repo for storing the files I use to make animations with lucidrains's BigSleep and DeepDaze projects.
 
 `MLAnimator.py` sorts the output folder of BigSleep or DeepDaze and using FFMPEG can animate the results easily.

 BigSleep: https://github.com/lucidrains/big-sleep
 
 DeepDaze: https://github.com/lucidrains/deep-daze
 
 FFMPEG: https://www.ffmpeg.org/

 CoLab Notebook: https://colab.research.google.com/drive/12EU4iVue3I91Pfqo5hc0-gXOtc81e3kK?usp=sharing

# How to use:

Open the command window at the directory where you wish to store the output folder. Call `MLAnimator.py` in python with the argument `-dir` set to the directory that contains the unsorted image output (or the directory that contains the sorted folders after using MLAnimator on it.)

The program will ask you for a starting frame and an amount of frames to render. If you skip setting a starting frame, the frames will be chosen from the highest numbered files. If you do set a starting frame, the frames will be chosen starting with that image and selecting higher numbered frames.
You can also supply the starting frame and amount of frames with the arguments "-sf <number>" and "-f <number>". Use "-h" to see all the arguments available.

`MLAnimator.py` is also in the CoLab notebook, but you may want to make a zipped copy of your files before animating in case your runtime limit is hit.


# Known Issue:

If your path for `-dir` ends with a backslash and quotes `\"`, the program cannot run. Just remove the ending backslash.

	
# Stay tuned
	
I'm planning on updating this repo and making more in depth tutorials for machine learning projects soon!
