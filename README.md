# MLAnimator
 Repo for storing the files I use to make animations with lucidrains's BigSleep and DeepDaze projects.
 
 `MLAnimator.py` sorts the output folder of BigSleep or DeepDaze. It can use FFMPEG can animate the results easily.
 

## Google Colab notebooks to try for yourself
 
DeepDaze + MLAnimator:   [![DeepDaze + MLAnimator CoLab Link](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/12EU4iVue3I91Pfqo5hc0-gXOtc81e3kK?usp=sharing)

BigSleep + MLAnimator:    [![BigSleep + MLAnimator CoLab Link](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/1oDYS2vJcuYfsqlqQvYkBf5lxxj6CKRvC?usp=sharing)

MLAnimator:     [![MLAnimator CoLab Link](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/1wS7SgGWqEYG0r9tXcJS3QRSntz5yBmbV?usp=sharing)

## Source Repos and Downloads

 BigSleep: https://github.com/lucidrains/big-sleep
 
 DeepDaze: https://github.com/lucidrains/deep-daze
 
 FFMPEG: https://www.ffmpeg.org/

# How to use:

Open the command window at the directory where you wish to store the output folder. Call `MLAnimator.py` in python with the argument `-dir` set to the directory that contains the unsorted image output (or the directory that contains the sorted folders after using MLAnimator on it.)

The program will ask you for a starting frame and an amount of frames to render. If you skip setting a starting frame, the frames will be chosen from the highest numbered files. If you do set a starting frame, the frames will be chosen starting with that image and selecting higher numbered frames.
You can also supply the starting frame and amount of frames with the arguments `-sf <number>` and `-f <number>`. Use `-h` to see all the arguments available.

`MLAnimator.py` is also in the CoLab notebook, but you may want to make a zipped copy of your files before animating in case your runtime limit is hit.


# Known Issue:

If your path for `-dir` ends with a backslash and quotes (like this: `\"`), the program may not run. Just remove the ending backslash.

	
# Stay tuned
	
I'm planning on updating this repo and making more in depth tutorials for machine learning projects soon!
