A small script to help make graphic files for [NightGFX](https://www.tt-forums.net/viewtopic.php?t=69607), the OpenTTD graphic baseset 
 
main.py currently automatically makes, from an 8bpp sprite 
+ 32bpp sprite with transparent backgrounds and desaturated company color 1  (cc1)
+ 8bpp mask files with palette, that replace cc1 with color index 202 and preserves following colors:
  + 232-238   Fire Cycle
  + 239-240   Flashing Red
  + 241-244   Flashing Yellow

dependencies: pillow, numpy

usage: 
1. install [Python](https://www.python.org/downloads/) on your computer
2. open your terminal
3. download pillow and numpy by running these commands
   + `pip install pillow`
   + `pip install numpy`
4. download the script [main.py](https://github.com/Bohaska/nightgfx/blob/main/main.py) and move it to the folder where you have images
5. find the folder this script is located in and go to it in terminal with this command:
    + `cd path/to/your/folder` (replace path/to/your/folder with your folder)
6. run this script
   + `python main.py`
7. this script will ask you which image to process. Write the name of the file. Example:
    + `infra06`
    + `infra06.png`
    + make sure the image and the script are in the same folder
8. enjoy your new files
    + they will be at `infra06--mask.png` and `infra06--32bpp.png` if your file was `infra06.png`