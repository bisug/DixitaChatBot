import glob
from os.path import basename, dirname, isfile

def __list_all_modules():
    """Scans the module directory and returns a list of all Python module names excluding __init__.py."""
    # Locate all Python files within the same directory as this __init__.py file
    mod_paths = glob.glob(dirname(__file__) + "/*.py")

    # Extract the file name without the extension for each module found
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    return all_modules

# Export a sorted list of all module names for dynamic loading
ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
