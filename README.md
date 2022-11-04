# Numbers Labyrinth
---

Find Your way from the Start to the Exit, stepping only on adjacent numbers from geometrical and from mathematical perspectives.

![Screenshot](https://github.com/oliverbacsi/NumLaby/blob/master/Screenshot.png)

**Usage**:
```
numlaby.py [<width> <height>]
```

* &lt;width&gt; and &lt;height&gt; are integers and not less than 5
* They are either specified both or none of them
* If not specified, or don't get exactly 2 command line arguments, labyrinth size defaults to 40 x 20

**Game Rules**:

Use the cursor keys to navigate inside the labyrinth in the 4 basic directions. You can only step on laterally adjacent cells.
There is one rule though: You can only step on such cells where the number differs from Your current cell's number by 1.
So if You are standing on a cell with **`4`** in it, then You can only step onto cells with **`3`** or **`5`** , etc...
This also means that even if You are standing next to the exit cell, but its number differs by any other value than 1,
then You won't be able to exit...

**Screen Elements**:

* Player is displayed by a bold white **`@`**
    * as the Player covers the actual cell number, it is echoed below the labyrinth
* Visited cells will be turned reverse to indicate that they are already visited
* The last "known good path" (the path the Player got from the Start to the Current cell) is highlighted by a white trail
    * What means "good path": If You find a loop and meet Your previous path at a certain point, then the whole path is truncated to this joining point. So the path will not display how You actually got to Your current position, but how it would have been the shortest to that position.
    * It does not mean that it is the correct solution though.
* Start and Exit cells are highlighted with bright white on red background, and if Your terminal supports it, they are blinking

**Still to develop**:

* [ ] More fancy intro screen
* [ ] More fancy winners celebration
* [ ] Possibility to repeat game after finishing

