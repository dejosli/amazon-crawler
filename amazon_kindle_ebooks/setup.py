import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows
base = None
# if sys.platform == 'win32':
#     base = 'Win32GUI'

includes = ['scrapy', 'user_agents']

build_exe_options = {
    # 'compressed': True,
    # 'optimize': 2,
    "packages": ["os", "scrapy", "user_agents"],
    'includes': includes,
    'excludes': []
}

executable = Executable(
    script='kindle_audible.py',
    base=base
)

setup(
    name='Kindler Scraper',
    version='0.1',
    description='Scrapes ebooks from amazon kindle store',
    options={'build_exe': build_exe_options},
    executables=[executable]
)
