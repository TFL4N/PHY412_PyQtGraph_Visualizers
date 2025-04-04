#original source: https://medium.com/@ealbanez/how-to-easily-convert-latex-to-images-with-python-9062184dc815
# Added resizing


import matplotlib
import matplotlib.pyplot as plt

# Runtime Configuration Parameters
matplotlib.rcParams["mathtext.fontset"] = "cm"  # Font changed to Computer Modern


def latex2image(
        latex_expression, image_name, align_bottom=True, padding=0.0, fontsize=50, dpi=200
):
    """
    A simple function to generate an image from a LaTeX language string.
    Autosizes images
    Transparent BG

    Parameters
    ----------
    latex_expression : str
        Equation in LaTeX markup language.
    image_name : str or path-like
        Full path or filename including filetype.
        Accepeted filetypes include: png, pdf, ps, eps and svg.
    align_bottom : Aligns bottom if True, else centers.  Useful for latex with superscripts and no subscripts 
    padding: padding in pixelsaround image
    fontsize : float or str, optional
        Font size, that can be expressed as float or
        {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}.

    Returns
    -------
    fig : object
        Matplotlib figure object from the class: matplotlib.figure.Figure.

    """
    fig = plt.figure(figsize=None, dpi=dpi, facecolor=None)
    text = fig.text(
        x=0.5,
        y=0.5,
        s=latex_expression,
        horizontalalignment="center",
        verticalalignment="baseline" if align_bottom else "center",
        fontsize=fontsize,
        color='white'
    )
    
    # must render to calculate bounding box
    plt.savefig(image_name, transparent=True)

    # resize image
    bbox = text.get_window_extent()
    
    # Add padding:
    width_px = bbox.width + 2 * padding
    height_px = bbox.height + 2 * padding

    # Convert to inches (figure size is in inches):
    width_in = width_px / fig.dpi
    height_in = height_px / fig.dpi
    fig.set_size_inches(width_in, height_in)

    # Adjust the text position (optional, to keep it centered):
    text.set_x(0.5)  # Center horizontally
    text.set_y(0.0 if align_bottom else 0.5)  # Center vertically
    
    plt.savefig(image_name, transparent=True)
    
    return fig
