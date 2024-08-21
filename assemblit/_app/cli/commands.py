""" Assemblit commands """

import os
from typing import Union, Literal
from assemblit._app import layer


# Define assemblit sub-command function(s)
def run(
    script: Union[str, os.PathLike]
):
    """ Runs a Python script.

    Parameters
    ----------
    script : `Union[str, os.PathLike]`
        The relative or absolute path to a local Python script.

    Help
    ----
    usage: assemblit run [-h] script

    positional arguments:
    script      The relative or absolute path to a local Python script.

    options:
    -h, --help  show this help message and exit

    Execute `assemblit run --help` for help.

    Examples
    --------
    ``` console
    assemblit run app.py
    ```

    """
    return layer.run(script=script).wait()


def build(
    app_type: Literal['demo']
):
    """ Builds a new project.

    Parameters
    ----------
    app_type : `Literal['demo']`
        The type of web-application.

    Help
    ----
    usage: assemblit build [-h] {demo}

    positional arguments:
    app_type {demo}      The type of web-application.

    options:
    -h, --help  show this help message and exit

    Execute `assemblit build --help` for help.

    Examples
    --------
    ``` console
    assemblit build demo
    ```
    """

    # Get current work-directory
    path = os.getcwd()

    # Build
    application = layer.build(app_type=app_type, path=path)

    # Run
    return layer.run(
        script=os.path.join(os.path.abspath(path), 'app.py'),
        application=application
    ).wait()
