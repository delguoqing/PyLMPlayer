PyLMPlayer
==========
A Player for playing and rendering LM format.(A format found in Taiko no tatsujin portable DX).

Note:
  This project is at very early stage and far from mature.
  
  Now, PyLMPlayer can play some complicated fumen with hundreds of sprite updating at the same time, while still run at 
  60fps on my old notebook.So I think performance is.. alright.
  
  I think this project is almost finished. Although more have to be added to make it a real taiko no tatsujin game. But 
  it is not the goal of this project —— a LM format engine for LM file playback.
  
How to play:
  Because it uses official resources from original game, i can't upload those fatasitic images and swfs.
  Ask me for a pack of resource and combine that unzipped folder with `packages` folder.

Dependencies:
  1.Pyglet 1.2alpha1. used in python level to handle window system.
  2.OpenGL and Glew. used in Cython extension module.(You're need them to compile pyd file.)
