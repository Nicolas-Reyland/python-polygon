# Chaikin 3D

Expansion of the Chaikin Algorithm to the 3rd dimension.

(Polyhedral Approximation / Polyhedron Subdivisions / Subdivision Surface).

**_IMPORTANT NOTE_**: Some features are currently broken. Will fix them after my finals :)

# Contents

 - [Contents](#contents)
 - [Installation](#installation)
 - [Some explanations first](#some-explanations-first)
 - [Usage](#usage)
 - [Examples](#examples)
 - [Todo](#todo)
 - [Note](#note)


# Installation

You need to have python (version 3+) and pip installed.

Then, download the repo:
```
git clone https://github.com/Nicolas-Reyland/Chaikin3D
```

Then you will need some python packages :
```
pip install -r requirements
```

# Some explanations first

This project supports more "exotic" polyhedron (a polyhedron is a polygon in space/3D) types. In fact, since we are going to change the polyhedron, raw data of the verticies isn't sufficient. We need info about which edges are important, and which are not. For example, in a cube, the diagonal edge (to split the square into two triangles) is not "important": its purpose is only to bind two vertices so that triangle can be drawn to the screen. That's why we need to distinguish *main* and *graphical* connections between our nodes (vertices).

That is why the polyhedral approximation of meshes that were loaded from *.obj* files are not always as wanted. There is no way to know if a connection between two nodes is really a part of the mesh or if its only purpose is to form triangles (you can normally only draw triangles). There are no "graphical" connections in those meshes :(
Every time a vertex list has more than 3 vertices in a mesh file, they are binded with graphical connections to form triangles (there are no other polygons than triangles that are drawn in this project)

Here are the main connections of a cube:

<img src="pics/cube-main-connections.png"
     alt="Cube main connections"
     style="float: left; margin-left: 10px;" />

Here are the graphical connections of a cube:

<img src="pics/cube-graphical-connections.png"
     alt="Cube graphical connections"
     style="float: left; margin-left: 10px;" />

Here are all the connections of a cube:

<img src="pics/cube-all-connections.png"
     alt="Cube all connections"
     style="float: left; margin-left: 10px;" />

And when you draw all this:

<img src="pics/simple-cube.png"
     alt="Simple cube rendering"
     style="float: left; margin-left: 10px;" />


For examples of what I mean with "graphical" connections, try these commands: ```python chaikin3d.py -s cube -p full -cg 0``` and ```python chaikin3d.py -s cube -p full -cg 1```. The grapchical connections are the black lines, while the main connections are the red lines.


# Usage

To get help, use the ```python chaikin3d.py -h``` command.
See the [additional info tab](#additional-info) to get info about how exactly to enter your values.

## Loading the polyhedron

Loading a polyhedron is the only thing you must do. You will get an error if you do not. If the only thing you do is loading a mesh, it will simply be drawn to the screen using the default settings.

### Related Options:

 * ```-i```/```--input```
 * ```-e```/```--evaluate```

### Input option

You will first have to select a polyhedron/mesh to render or use. You can load a *.obj* (only supported extension, for now) file using the ```-i``` (```--input```) option like this: ```python chaikin3d.py -i data/dog.obj``` (if you try this and the mesh is somehow rotated, please add this to your command line: ```-rm true```).

[Here](https://people.sc.fsu.edu/~jburkardt/data/obj/obj.html) is a link to lots of *.obj* files which you can download and test. You only need the *.obj* file. Only vertices and faces are read by the program.

### Evaluate option

The ```-e```/```--evaluate``` option can be used in two ways (or more):

The evaluation options takes a string as input, which will be run as python code right after the loading of the polyhedron mesh file (if any has been given). You should use this option to generate your own polyhedrons or to customize the one that has been loaded. There are a few things you should know:

You have access, in the local variables to the following python objects:
 * ```Polyhedron``` (*polyhedron.py*)
 * ```WaveFrontReader``` (*wavefront_reader.py*)
 * ```Renderer``` (*plotly_renderer.py* / *mpl_renderer.py*)

The loaded polyhedron object is named ```poly```. If you did not load a file, there is no such variable. You then have to create it. When you create the ```poly``` variable, it must be of type ```Polhyhedron```.

### Examples

Load a a cube, then apply the chaikin algorithm on it:
```
python chaikin3d.py -i data/cube.obj -e "poly = poly.Chaikin3D()"
```

<img src="pics/simple-cube-chaikin.png"
alt="1 chaikin iteration on cube"
style="float: left; margin-left: 10px;" width="20%;" />

*Note: this is equivalent to ```python chaikin3d.py -i data/cube.obj -cg 1```*

Load a tetrahedron, then rotate it by 45° with code you potentially wrote in a file named "my_own_code.py":
```
python chaikin3d.py -i data/tetrahedron.obj -e "poly = __import__('my_own_code').rotate_tetrahedron(poly, x_rot = 12, y_rot = 45, z_rot = 0)"
```

Generate a new polyhedron
```
python chaikin3d.py -e "poly = __import__('evaluations').generate_diamond(num_points = 25)"
```


## Chaikin Algorithm

### Related Options:

 * ```-cg```/```--chaikin-generations```
 * ```-cc```/```--chaikin-coef```

### Chaikin Generations

To choose the number of Chaikin generations (or iterations) you want to run on the given polyhedron, you should be using the ```-cg```/```--chaikin-generations``` option. The default value is 0. To run one iteration, you could use ```-cg 1``` (for 2 iterations : ```-cg 2```, you got it).

### Chaikin Coeffiecient

You might also want to control the *Chaikin coefficient*. This is done using the ```-cc``` option. This value is used to *cut* the edges at 1/coef and (coef-1)/coef. George Chaikin chose "4" as beeing the right coefficient. This cust the edges into three parts: first 25%, 50%, 25% ([2D Chaikin's Corner Cutting Algorithm](https://sighack.com/post/chaikin-curves)).

### Examples

One iteration on a deeer (yes, a deer)
```
python chaikin3d.py -i data/deer.obj -cg 1
```

<img src="pics/simple-deer-chaikin.png"
alt="2 chaikin iteration on deer"
style="float: left; margin-left: 10px;" width="20%;" />

Two iterations on a cube
```
python chaikin3d.py -i data/cube.obj -cg 2
```

<img src="pics/simple-cube-chaikin-cg-2.png"
alt="1 chaikin iteration on cube"
style="float: left; margin-left: 10px;" width="20%;" />

One iteration on a tetrahedron, with a coefficient of 3
```
python chaikin3d.py -i data/tetrahedron.obj -cg 1 -cc 3
```

<img src="pics/simple-tetrahedron-chaikin-cc-3.png"
alt="1 chaikin iteration on deer"
style="float: left; margin-left: 10px;" width="20%;" />


## Graphical Options

Graphical options let you choose how you want to plot your mesh. You can customize most of the graphical aspects of your plots.

### Related Options

 * ```-p```/```--plot```
 * ```-a```/```--alpha```
 * ```-r```/```--renderer``` (DO NOT USE)
 * ```-sn```/```--show-nodes```
 * ```-smc```/```--show-main-connections```
 * ```-sgc```/```--show-graphical-connections```
 * ```-rm```/```--rotate-mesh``` (only with the ```-i``` option)
 * ```-nc```/```--node-color```
 * ```-pc```/```-polygon-color```
 * ```-mcc```/```--main-connection-color```
 * ```-gcc```/```--graphical-connection-color```

### Plot Types

There are 4 types of plots (see examples below):
 * "simple" plot : this plot only draws your polyhedron to the screen
 * "full" plot : this one draws a lot of data separately: your connections (by type, etc.), your vertices and different mesh representations. Useful for understanding how things work and debugging in general
 * "evolution" plot : the evolution plot takes into account the number of chaikin generations that you want (```-cg``` option). I will render one generation after another in a grid-format (like the "full" plot)
 * "animation" plot (DO NOT USE) : this plot should, in theory, create an animation, rendering all the chaikin generations from 0 to the value given in the ```-cg``` option
The default value is "simple"

### How to plot (colors, etc.)

The ```-a```/```--alpha``` switch allows you to change the alpha/opacity value (ranging from 0.0 to 1.0) of the faces in the "simple", "evolution" and "animation" plots (every plot except the "full" plot <- there are already alpha changes). Default value: 0.8

You should not mess with the ```-r```option, but it exists (even I don't mess with -> the mpl renderer is BROKEN). Default value: "plotly"

You can dis/en-able the rendering of nodes with the ```-sn```/```--show-nodes``` option. Default value: "true"

The ```-smc``` switch allows to choose if you want to render the main connections for the "simple", "evolution" and "animation" plots. Default value: "true"

The ```-sgc``` switch allows to choose if you want to render the graphical connections for the "simple", "evolution" and "animation" plots. Default value: "false"

Use the ```-rm```/```--rotate-mesh``` to rotate meshes that look ... rotated **on load** (therefore, you can only use this option with the ```-i```/```--input``` option).

The ```-nc```, ```-pc```, ```-mcc``` and ```-gcc``` options let you customize the colors for the nodes (df. green), polygons (df. lightblue), main connections (df. darkred) and graphical connections (df. black). You can give color-names or colors with this format: *#12ab34*. The value *random* is valid and will generate a new random color for each node/polygon/main connection/graphical connection.

### Examples

Show a cube with no transparency at all and only (yellow) graphical connections
```
python chaikin3d.py -i data/cube.obj -cg 3 -cc 5 -pc mediumaquamarine -smc false -sgc true -gcc yellow
```
<img src="pics/simple-cube-chaikin-cg-3-cc-5-colors.png"
alt="special colors chaikin cube cg 3 cc 5"
style="float: left; margin-left: 10px;" width="20%;" />



## Other Options

```-v```/```--verbose```
```-t```/```--test```

There is a ```-v```/```--verbose``` switch too. If you turn it on, you will get info about the chaikin algorithm progress. This might be useful for meshes with a lot of vertices or when having a lot of iterations. The default value is "false".

## Additional info

### Global option rule

Every option takes either a **bool** (see below), **string**, **int** & **float**. There are no *standalone* options (which take no argument).


### Colors

You can use the [CSS color code](https://www.w3.org/wiki/CSS/Properties/color/keywords) (extended colors too) to specify a color. An rgb value can be passed through the format *#rrggbb*, or any valid VSS color value.

### Boolean values

For boolean values, *1*, *t* and *true* (case insensitive) will mean "true". And *0*, *f*, *false* (case insensitive) will mean "false".


# Examples

Here are some more examples of what can be done:


### Dogs

```
python chaikin3d.py -i data/dog.obj -rm true -sgc true
```
```
python chaikin3d.py -i data/dog.obj -rm true -sgc true -cg 1
```

<img src="pics/simple-dog.png"
alt="simple dog"
style="float: left; margin-left: 10px;" width="48%;" /> <img src="pics/simple-dog-chaikin.png"
alt="simple dog chaikin"
style="float: right; margin-right: 10px;" width="48%;" />


### Cubic evolution

```
python chaikin3d.py -i data/cube.obj -p evolution -cg 5
```

![cube evolution](pics/evolution-cube-chaikin.png)


### Full of triangles

```
python chaikin3d.py -i data/tetrahedron.obj -p full -cg 1 -cc 3
```

![full triangle chaikin with coeff 3](pics/full-triangle-chaikin-cc-3.png)

*The "solid" statement means that the alpha value of the triangles has been set to 1.0 (no transparency)*


### Bigger meshes

```
python chaikin3d.py -i data/deer.obj -rm true -a 1.0
```
```
python chaikin3d.py -i data/deer.obj -rm true -a 1.0 -smc false
```
<img src="pics/simple-deer.png"
alt="1 simple deer no main connections alpha 1"
style="float: left; margin-left: 10px;" width="48%;" /> <img src="pics/simple-deer-no-smc.png"
alt="2 simple deer no main connections alpha 1"
style="float: right; margin-right: 10px;" width="48%;" />

```
python chaikin3d.py -i data/deer.obj -rm true -a 1.0 -smc true -cg 1 -v 1
```
```
python chaikin3d.py -i data/deer.obj -rm true -a 1.0 -smc true -cg 1 -v 1
```

<img src="pics/simple-deer-chaikin.png"
alt="1 simple deer no main connections alpha 1"
style="float: left; margin-left: 10px;" width="48%;" /> <img src="pics/simple-deer-chaikin-no-smc.png"
alt="2 simple deer no main connections alpha 1"
style="float: right; margin-right: 10px;" width="48%;" />

*Verbose switch (```-v true```) not mandatory. There are 25486 nodes in the last deer mesh. Loading thoses meshes should take at least a few minutes.*


# TODO

 * Fix issue where plotly would just freeze the program (Windows only & might be a plotly issue ?)
 * Add example pics after every example line in README (e.g. ```-e``` option examples)
 * Better memory optimization (should come with C/C++ FFI implementation)
 * Save result to .obj file (keeping original textures ??)
 * Finish animation plot
 * Optimization of the Chaikin3D algorithm
     - maybe parallelism ?
     - FFI with C++ or C (much more likely to happen than parallelism + much faster)
 * Fix issue of python crashing (no errors, just crashing) when trying to apply chaikin3D on a large number of nodes & connections
 * Change scale when plotting (e.g. data/cat.obj)


# Note

If you have any issues using this project or need any help, please feel free to tell me [on github](https://github.com/Nicolas-Reyland/Chaikin3D/issues) !
If you want to help me developping this project, please tell me too !



*Author: Nicolas Reyland*
