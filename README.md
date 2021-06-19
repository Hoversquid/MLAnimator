# MLAnimator
 Repo for storing the files I use to make animations with VQGAN + CLIP (Z+quantize method) and lucidrains's BigSleep and DeepDaze projects.
 
 `MLAnimator.py` sorts the output folder of big-sleep, deep-daze, or VQGAN + CLIP. It can use FFMPEG can animate the results easily.
 Notebooks have been simplified and include MLAnimator cells. The original notebooks should be in their source repos.

## Google Colab notebooks to try for yourself:
 
deep-daze + MLAnimator:   [![DeepDaze + MLAnimator CoLab Link](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/12EU4iVue3I91Pfqo5hc0-gXOtc81e3kK?usp=sharing)

big-sleep + MLAnimator:    [![BigSleep + MLAnimator CoLab Link](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/1oDYS2vJcuYfsqlqQvYkBf5lxxj6CKRvC?usp=sharing)

VQGAN + CLIP + MLAnimator: [![VQGAN + CLIP + MLAnimator CoLab Link](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/1ISGQEjl5-M7CDtngQE13D-IkGEjqKUCv?usp=sharing)

MLAnimator:     [![MLAnimator CoLab Link](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/1wS7SgGWqEYG0r9tXcJS3QRSntz5yBmbV?usp=sharing)

## Source Repos and Downloads:

 BigSleep: https://github.com/lucidrains/big-sleep
 
 DeepDaze: https://github.com/lucidrains/deep-daze
 
 VQGAN: https://github.com/CompVis/taming-transformers
 
 Original VQGAN + CLIP Notebook: [![VQGAN + CLIP CoLab Link](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/1L8oL-vLJXVcRzCFbPwOoMkPKJ8-aYdPN?usp=sharing)
 
 FFMPEG: https://www.ffmpeg.org/



# How to use:

Open the command window at the directory where you wish to store the output folder. Call `MLAnimator.py` in python with the argument `-dir` set to the directory that contains the unsorted image output (or the directory that contains the sorted folders after using MLAnimator on it.)

The program will ask you for a starting frame and an amount of frames to render. If you skip setting a starting frame, the frames will be chosen from the highest numbered files. If you do set a starting frame, the frames will be chosen starting with that image and selecting higher numbered frames.
You can also supply the starting frame and amount of frames with the arguments `-sf <number>` and `-f <number>`. Use `-h` to see all the arguments available.

You can use the argument `-m` to mirror the animation, making a seemless loop but doubling the file size.

Using the argument `-ft <filetype>` will let you set the animation to a `gif` or `mp4`.

`MLAnimator.py` is also in the CoLab notebook, but you may want to output your renders to Google Drive to save your images in case your runtime limit is hit. 


# Known Issue:

If your path for `-dir` ends with a backslash and quotes (like this: `\"`), the program may not run. Just remove the ending backslash.

	
# Stay tuned:
	
I'm planning on updating this repo and making more in depth tutorials for machine learning projects soon!
