# PHY412_PyQtGraph_Visualizers

While taking Electrodynamics taught by Professor Richard Kirian at Arizona State University, I shared my recently created [Lissajous Figure Generator](https://github.com/TFL4N/Lissajous-HTML5) with the class.  Lissajous figures are created from two orthogonal sinusoids.

Always trying to make class material more intuitive and understandable, Professor Kirian ask if I could help create visualizers for various concepts, in particular, the polarization of light that results from two orthogonal electromagnetic waves.  This repo contains the results of this collaboration 

The version of the electromagentic wave plane visualizer is interactive, i.e. the user can switch between parts and segments, move the camera, changes variables like angular frequency and relative phase.

In addition, this project includes step-by-step explainer of the simulations, which is located here [Explainer Slides](resources/explainer_slides.pdf).  These explainer slides can also be accessed from the GUI while using the `EXPLAINER` or `SUPER_USER` user modes.

![Gif of Polarization](doc/simulation_example.gif)

## Installation

This repo uses `conda` to make the python environment and dependencies

```shell
cd /path/to/install/dir
git clone git@github.com:TFL4N/PHY412_PyQtGraph_Visualizers.git

conda env create --file environment.yml
conda activate em_viz
```

## Usage
First follow the installation directions above to clone the repo and setup the python environment

```shell
# if conda envir not active
conda activate em_viz

cd /path/to/install/dir
python main.py
```

### User Modes
There three different user modes for this application.  The user modes hide or show different interactive elements, like debug, scene settings, and explainer link.

- SUPER_USER == 0
  - Displays all options, including debug options, scene settings, and the explainer link
- SIMULATION == 1
  - Only displays the simulation and simulation related elements, e.g. does not show the explainer link.  This saves screen real estate, if you're only interested in the similation
- EXPLAINER == 2 (The default option)
  - Displays the explainer link along with the simulation elements

Examples of invocating different user modes
```shell
# SUPER_USER mode
python main.py -u 0

# SIMULATION mode
python main.py -u 1

# EXPLAINER mode
python main.py -u 2
```

## Developer
To display LaTex in the simulation, `matplotlib` is used to create images which are loaded into `MyGLImageItem` scene objects

[latex2image.py](latex2image.py) contains the methods to create the images from a LaTex string
[test/latex_test.py](test/latex_test.py) contains examples of how create these images
