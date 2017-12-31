import os

__VERSION__ = '.3'

if 'KIVENT_PREVENT_INIT' not in os.environ:
    from nemo_sfx import sfx_renderer
    from nemo_sfx import sfx_formats
    from nemo_sfx import sfx
