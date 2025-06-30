"""
By M4elstr0m (https://github.com/M4elstr0m)

This module provides built-in tools to make Minecraft block scanning easier using Minescript, especially for research purposes.
This should not be run directly.

 █▀▀ █▀█ █▀▀ █▀▄ █ ▀█▀ █▀\n
 █▄▄ █▀▄ ██▄ █▄▀ █ ░█░ ▄█

M4elstr0m (https://github.com/M4elstr0m) for conceiving this script (Megascan) you are currently reading

maxuser (https://github.com/maxuser0) for creating the wonderful Minescript mod

Refer to README.md for more user-friendly explanations

"""

import minescript as ms # obviously
import lib_blockpack_parser as msb # blockpack parser for Minescript

import time # for time related calculations
import pathlib # for external file manipulation (such as Megascan exports)

###

global currentFolder # contains the full path of this file's directory
currentFolder:str = str(pathlib.Path(__file__).resolve().parent)

global default_radius_x # will be used as default if none specified
global default_radius_y # will be used as default if none specified
global default_radius_z # will be used as default if none specified
global debug # must be set to True to access debug mode

"""     Settings     """
default_radius_x:int = 10
default_radius_y:int = 2
default_radius_z:int = 10

debug:bool = False
"""Debug variable for the Megascan module"""

"""                  """

def debug_echo(content:str) -> None:
     """
     Displays an in-game given text as a debug log from Megascan

     :param str content: Text content that you would like to display
     """
     ms.echo_json(
          {
               "text":"",
               "extra": [
               {
                    "text": "Debug: ",
                    "color": "#efc63f",
                    "bold": True
               },
               {
                    "text": f"{content}",
                    "color": "#f7ebc5",
                    "bold": False
               }
               ]
          }
     )

def debug_format_date() -> str:
    """
    Returns your current localtime date with the format YYYYMMDD-HHMMSS as string value

    :returns str: Localtime date with the format YYYYMMDD-HHMMSS
    """
    return f"{time.localtime().tm_year}{time.localtime().tm_mon}{time.localtime().tm_mday}-{time.localtime().tm_hour}{time.localtime().tm_min}{time.localtime().tm_sec}"

def PlayerCoordinates() -> tuple:
    """
    Basically shortens the minescript.player().position into one function

    :returns tuple(int,int,int): X, Y, and Z coordinates of the player
    """
    x, y, z = [round(p) for p in ms.player().position]
    return (x,y,z)

class Megascan:
    """
    A Megascan class, for storing a huge amount of block coordinates associated with their block-types in a dictionary
    
    I (M4elstr0m) conceived this class to turn Minescript (4.0) logic into mine, basically more "methods oriented"
    
    Obviously made for Minecraft
    """

    def __init__(self) -> None:
        self.content:dict = {}
        """
        dictionary associating coordinates with blocktypes

        Trivia: Will always be a full blockpack (will not take the content of its search)"""

    def __add__(self, other:dict[tuple, str]) -> dict[tuple, str]:
        """
        Merges the content of a Megascan with a dictionary (Use it to merge a Megascan with its searches)

        Trivia: if coordinates value is already existing in Megascan.content, it replaces it with the new one
        
        :param dict[tuple:str] other: dictionary with the same format as a Megascan search

        :returns dict[tuple:str]: Megascan's new content
        """
        if not isinstance(other, dict): # Type checking was too crucial for me not to do it
            raise TypeError(
                "unsupported operand for +: "
                f"'{type(self).__name__}' and '{type(other).__name__}'"
            )
        for key in other:
            self.content[key] = other[key]
        
        return self.get()
        

    def __repr__(self):
        """
        Basically prints the string content of the Megascan

        :returns str: Megascan's content as string output
        """
        return str(self.content)

    def __replace(self, new_dict:dict[tuple, str]) -> None:
        """
        Replaces the content of the Megascan object (dict) by a given dict

        :param dict[tuple:str] new_dict: A dictionary with the same format as a Megascan.content
        """
        self.content = new_dict

        if debug:
            debug_echo("content replaced successfully")

        return None
    
    def __convert_search_to_new(self, search_results:list[tuple]) -> dict[tuple, str]:
        """
        Turns a search result (list of tuples) into a dictionary (with the format of a Megascan.content)

        :param list[tuple] search_results: Output of a Megascan.search() or reverse_search()

        :returns dict[tuple:str]: dictionary with the format of a Megascan.content
        """
        new_dict:dict = {}
        
        for i in range(len(search_results)):
            new_dict[search_results[i][0]] = search_results[i][1]

        if debug:
            debug_echo(f"search results converted to Megascan format successfully")

        return new_dict

    def new(self, player_pos:tuple, radius_x:int=default_radius_x, radius_y:int=default_radius_y, radius_z:int=default_radius_z) -> dict[tuple:str]:
        """
        Scans all the blocks within the specified radius and returns it as a dictionary

        Trivia: normally, you don't have to call it manually

        :param tuple(x, y, z) player_pos: Player in-game coordinates
        :param int radius_x: Radius of Minecraft X coordinates that the Megascan will explore
        :param int radius_y: Radius of Minecraft Y coordinates that the Megascan will explore
        :param int radius_z: Radius of Minecraft Z coordinates that the Megascan will explore

        :returns dict[tuple:str]: dictionary associating coordinates with its block
        """
        
        x, y, z = player_pos
        megascan_dict:dict = {}

        if debug:
            debug_echo(f"scan started at {debug_format_date()}")

        blockpack = ms.BlockPack.read_world((x-radius_x, y-radius_y, z-radius_z), (x+radius_x, y+radius_y, z+radius_z))
        parser = msb.BlockPackParser.parse_blockpack(blockpack)

        for tile in parser.tiles:
            for blockpos, blockid in tile.iter_setblock_params():
                megascan_dict[blockpos] = parser.palette[blockid]
            for blockpos, blockpos2, blockid in tile.iter_fill_params():
                megascan_dict[blockpos] = parser.palette[blockid]
                megascan_dict[blockpos2] = parser.palette[blockid]

        return megascan_dict
    
    def refresh(self, player_pos:tuple, radius_x:int=default_radius_x, radius_y:int=default_radius_y, radius_z:int=default_radius_z) -> dict[tuple:str]:
        """
        Same as new but replace the current Megascan content

        :param tuple(x, y, z) player_pos: Player in-game coordinates
        :param int radius_x: Radius of Minecraft X coordinates that the Megascan will explore
        :param int radius_y: Radius of Minecraft Y coordinates that the Megascan will explore
        :param int radius_z: Radius of Minecraft Z coordinates that the Megascan will explore

        :returns dict[tuple:str]: Megascan's new content
        """
        self.__replace(self.new(player_pos, radius_x, radius_y, radius_z))

        return self.get()

    def extend(self, player_pos:tuple, radius_x:int=default_radius_x, radius_y:int=default_radius_y, radius_z:int=default_radius_z) -> dict[tuple:str]:
        """
        Same as new but merges the new scan with the current Megascan content

        Trivia: May use a lot of memory after a certain amount of time ONLY if the player is moving farther and farther

        :param tuple(x, y, z) player_pos: Player in-game coordinates
        :param int radius_x: Radius of Minecraft X coordinates that the Megascan will explore
        :param int radius_y: Radius of Minecraft Y coordinates that the Megascan will explore
        :param int radius_z: Radius of Minecraft Z coordinates that the Megascan will explore

        :returns dict[tuple:str]: Megascan's new content
        """
        new:dict = self.new(player_pos, radius_x, radius_y, radius_z)

        self + new

        return new

    
    def get(self) -> dict[tuple, str]:
        """
        Returns the Megascan content as a dictionary

        :returns dict[tuple:str]: Megascan's content
        """
        return self.content

    def amount(self) -> int:
        """
        Returns the amount of blocks in the Megascan

        :returns int: Amount of blocks
        """
        return len(self.content)
    
    def search(self, coordinates_list:list[tuple]) -> dict[tuple, str]:
        """
        Searches the Megascan for specific coordinates and returns the results of the search (a dict associating coordinates with block type)
        
        :param list[tuple] coordinates_list: A list of tuples (a list of Minecraft block coordinates)

        :returns dict[tuple:str]: Search results with Megascan.content format
        """
        result:list[tuple] = [] # .items()
        
        for coor in coordinates_list:
            keys = list(self.content.keys())
            if coor in keys:
                for i in range(len(keys)):
                    if keys[i] == coor:
                        result.append(tuple(self.content.items())[i])
        if debug:
            debug_echo(f"searched in Megascan")
        
        return self.__convert_search_to_new(result)

    def reverse_search(self, block_list:list[str]) -> dict[tuple, str]:
        """
        Reverse-searches the Megascan for specific block types and returns a dictionary associating coordinates with block type
        
        :param list[str] block_list: A list of blocks name in str (Minecraft format: 'minecraft:grass')

        :returns dict[tuple:str]: Reverse-search results with Megascan.content format
        """
        result:list[tuple] = [] # .items()
        
        for block in block_list:
            values = list(self.content.values())
            if block in values:
                for i in range(len(values)):
                    if values[i] == block:
                        result.append(tuple(self.content.items())[i])

        if debug:
            debug_echo(f"reverse-searched in Megascan")

        return self.__convert_search_to_new(result)
    
"""                      
 █▀▀ █▀█ █▀▀ █▀▄ █ ▀█▀ █▀
 █▄▄ █▀▄ ██▄ █▄▀ █ ░█░ ▄█

M4elstr0m (https://github.com/M4elstr0m) for conceiving this script (Megascan) you are currently reading

maxuser (https://github.com/maxuser0) for creating the wonderful Minescript mod

Refer to README.md for more user-friendly explanations

"""