# 🌍 Overview
<b>mc-megascan</b> is Python module to store a huge amount of Minecraft blocks using [Minescript](https://minescript.net/). It has a strong docstring within its source code, maintaining readability and accessibility for anyone aiming to use it in their projects.<br>

This module was conceived for the <b>[mc-MetalDetector](https://github.com/M4elstr0m/mc-metaldetector)</b> project using [Minescript](https://minescript.net/) v4.0

## <p align="center">Please star this repository if you find it useful ⭐</p>

### ⚠️ <ins>Disclaimer</ins>

I am <b>not responsible</b> of your usage of the mc-megascan, keep in mind that this may surely not be allowed in multiplayer.

Megascans have <b>some limitations</b> when scanning too far, I found a maximum radius of ~150 blocks.

I do not plan to make it available using `pip` since [Minescript](https://minescript.net/) is not yet available this way, moreover it is not related to Python but to Minecraft (this may change if a lot of people use it)

## 📦 Installation

1. Install [Minescript](https://minescript.net/)
2. Install [Minescript's Blockparser](https://minescript.net/sdm_downloads/lib_blockpack_parser-v1/)
3. Download <b>[mc-megascan](https://github.com/M4elstr0m/mc-megascan/)</b> and put `megascan.py` in your `minescript` folder (please refer to Minescript usage)

## 📚 Usage

<ins>This is a module that can be used in scripts with Minescript. This <b>should NOT be run directly</b>.</ins>

You can create any kind of scripts for Minescript using mc-megascan, this is like other Python modules, just `import` it in your own script (refer to Minescript usage)

## 📖 Documentation & Examples

As any other Python module, you must import `megascan` into your `.py` script to start using it

*If you feel uncomfortable with Python at this step, I suggest you to read [Python's documentation](https://docs.python.org/3/) instead*

```python
import megascan as mg
```

---

*In this section, `mega` will be the name of our Megascan's instance; Therefore `mega.content` corresponds to the `content` attribute of our `mega` object, which is an instance of `Megascan`*

As said earlier, <b>mc-megascan</b> is useful to store a consequent amount of blocks in a single variable, to perform searches afterwards.

When initializing a new Megascan object/instance, its content, accessible at `mega.content`, is a `dict` associating coordinates with block's name and will be empty at first 

```python
mega = mg.Megascan()
```

`Megascan` instance have multiple methods, not all of these will modify its attribute:

<b>Megascan.new()</b>

This method scans all the blocks within a specified radius from a world point and returns it as a dictionary without replacing current `mega` instance's content

```python
coordinates = mg.PlayerCoordinates()
print(mega.new(player_pos=coordinates, radius_x=10, radius_y=2, radius_z=10))
```

`player_pos` is a tuple corresponding to player's coordinates (x, y, z); Refer to <b>[PlayerCoordinates()](https://github.com/M4elstr0m/mc-megascan/blob/main/README.md#L161)</b> in order to get these

`radius_x` , `radius_y` and `radius_z` already have default values (respectively: 10, 2 and 10) if you let them empty, but you can fill it with your own integer values

*You are also able to change these default values in `megascan.py` in the [settings section](https://github.com/M4elstr0m/mc-megascan/blob/main/megascan.py#L34)* 

<b>Megascan.refresh()</b>

This method does basically the same as `mega.new()` but replaces Megascan object's content by the new scan

```python
coordinates = mg.PlayerCoordinates()
mega.refresh(player_pos=coordinates, radius_x=10, radius_y=2, radius_z=10)
print(mega.content)
```

Parameters follow the same guidelines as <b>[Megascan.new()](https://github.com/M4elstr0m/mc-megascan/blob/main/README.md#L52)</b>

<b>Megascan.extend()</b>

This method has a similar behavior as `mega.refresh()` but it will not strictly replace Megascan object's content. Instead, it will merge the old content with the new scan in a suppressive way, which means that new entries will overwrite old entries for the same coordinates

```python
coordinates = mg.PlayerCoordinates()
mega.refresh(coordinates) # which is the same as 'mega.refresh(player_pos=coordinates, radius_x=10, radius_y=2, radius_z=10)'
coordinates[0] += 100 # we will extend after being 100 blocks away from the initial scan
mega.extend(player_pos=coordinates, radius_x=10, radius_y=2, radius_z=10)
print(mega.content)
```

<b>Megascan.get()</b>

Returns the Megascan object's content as a dictionary; Allows user to view `mega.content` indirectly

```python
coordinates = mg.PlayerCoordinates()
mega.refresh(coordinates)
print(mega.get())
```

<b>Megascan.amount()</b>

Returns the amount of blocks/coordinates contained in the Megascan object

```python
coordinates = mg.PlayerCoordinates()
mega.refresh(coordinates)
print(mega.amount())
```

<b>Megascan.search()</b>

 Searches the Megascan for specific coordinates and returns the results of the search (a `dict` associating coordinates with block type)

```python
coordinates = mg.PlayerCoordinates()
mega.refresh(coordinates)
print(mega.search(coordinates_list=[(0,64,0)]))
```

`coordinates_list` is a list of tuples (a list of Minecraft block coordinates)

<b>Megascan.reverse_search()</b>

 Reverse-searches the Megascan for specific block types and returns once again a `dict` associating coordinates with block type

```python
coordinates = mg.PlayerCoordinates()
mega.refresh(coordinates)
print(mega.reverse_search(block_list=["minecraft:grass"]))
```

`block_list` is a list of blocks name in str (Minecraft format: 'minecraft:grass')

This is basically how <b>[mc-MetalDetector](https://github.com/M4elstr0m/mc-metaldetector)</b> was made

<b>Magic Methods</b>

`print(mega)` is equivalent to `print(mega.get())` or `print(mega.content)`

```python
coordinates = mg.PlayerCoordinates()
mega.refresh(coordinates)
print(mega)
```

`mega_1 + mega_2` merges two Megascan objects in a suppressive way (Refer to <b>[Megascan.extend()](https://github.com/M4elstr0m/mc-megascan/blob/main/README.md#L79)</b>) in the first one

```python
coordinates = mg.PlayerCoordinates()
mega_1.refresh(coordinates)
# player changes a few blocks
coordinates = mg.PlayerCoordinates()
mega_2.refresh(coordinates)
mega_1 + mega_2
print(mega_1)
```

---

<b>PlayerCoordinates()</b>

Returns player's in-game coordinates as a tuple of 3 integers

```python
import megascan as mg
coordinates = mg.PlayerCoordinates()
```

<b>debug_echo()</b>

Displays an in-game given text as a debug log from Megascan

```python
import megascan as mg
text = "Hello World!"
mg.debug_echo(content=text)
```

`content` is a string value that you would like to display

*This will only work if the `debug` boolean is set to `True` in the [settings section](https://github.com/M4elstr0m/mc-megascan/blob/main/megascan.py#L34)*

## 🗒️ Credits

<b>[M4elstr0m](https://github.com/M4elstr0m)</b> for conceiving this module (<b>mc-megascan</b>) you are currently consulting on Github

<b>[maxuser](https://github.com/maxuser0)</b> for creating the wonderful <b>[Minescript](https://minescript.net/)</b> mod
