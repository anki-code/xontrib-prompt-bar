import os
import re
import time
from pathlib import Path
from string import Formatter
from xonsh.tools import is_superuser

"""
Themes:
 * Supported colors: https://xon.sh/tutorial.html#customizing-the-prompt
"""
_pb_themes = {
    'default': {
        'left': '{hostname}{user}{cwd_abs#accent}',
        'right': '{env_name#strip_brackets#section}{gitstatus#nocolorx#section}{date_time_tz}',
        'bar_bg': '{BACKGROUND_#323232}',
        'bar_fg': '{#AAA}',
        'section_bg': '{BACKGROUND_#444}',
        'section_fg': '{#CCC}',
        'accent_fg': '{BOLD_#DDD}',
    }
}

_THEME = __xonsh__.env.get('XONTRIB_PROMPT_BAR_THEME', 'default')

if type(_THEME) is dict:
    _pb_themes['custom'] = _THEME
    _THEME = 'custom'

_LEFT = __xonsh__.env.get('XONTRIB_PROMPT_BAR_LEFT', _pb_themes[_THEME]['left'])
_RIGHT = __xonsh__.env.get('XONTRIB_PROMPT_BAR_RIGHT', _pb_themes[_THEME]['right'])
_BAR_BG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_BG', _pb_themes[_THEME]['bar_bg'])
_BAR_FG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_FG', _pb_themes[_THEME]['bar_fg'])
_SECTION_BG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_SECTION_BG', _pb_themes[_THEME]['section_bg'])
_SECTION_FG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_SECTION_FG', _pb_themes[_THEME]['section_fg'])
_ACCENT_FG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_ACCENT_FG', _pb_themes[_THEME]['accent_fg'])
_NOC = '{RESET}'

def _remove_colors(s):
    if s is None:
        return ''
    return re.sub('{([A-Z0-9#_]+?)}', '', s)

# https://stackoverflow.com/a/14693789/14470020
_ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
def _remove_escape(txt):
    return _ansi_escape.sub('', txt)

# https://stackoverflow.com/a/49986645
def _replace_emoji(text, replace_char=r'EE'):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(replace_char, text)

def _field_date_time_tz():
    t = time.strftime('%y-%m-%d %H:%M:%S%z', time.localtime())
    return t[:-2] if t[-2:] == '00' else t

__xonsh__.env['PROMPT_FIELDS']['prompt_end_xonsh'] = "#" if is_superuser() else "@"
__xonsh__.env['PROMPT_FIELDS']['cwd_abs'] = lambda: str(Path(__xonsh__.env['PROMPT_FIELDS']['cwd']()).expanduser())
__xonsh__.env['PROMPT_FIELDS']['date_time_tz'] = _field_date_time_tz

# DEPRECATED: use `{gitstatus#nocolorx}` instead of `{gitstatus_noc}`
__xonsh__.env['PROMPT_FIELDS']['gitstatus_noc'] = lambda: _remove_colors(__xonsh__.env['PROMPT_FIELDS']['gitstatus']())

def _screens():
    line = []
    sty = None
    for l in __xonsh__.subproc_captured_stdout(['screen', '-ls']).splitlines(): 
        if '\t' in l:
            screen_name = l.split('\t')[1].split('.')[1]
            if sty is None:  # lazy load
                sty = __xonsh__.env.get('STY', '.').split('.')[1]
            line.append(f"({screen_name})" if sty == screen_name else screen_name)
    return ', '.join(line)
__xonsh__.env['PROMPT_FIELDS']['screens'] = _screens

def _strip_brackets(v):
    v = v.strip()
    return v.strip("()[]{} \n\r") if v and v[0] in '([{' else v

_wrappers = {
    'accent': lambda v: f'{_ACCENT_FG}{v}',
    'section': lambda v: f'{_SECTION_BG}{_SECTION_FG} {v} {_NOC}{_BAR_BG}{_BAR_FG}',
    'noesc': lambda v: _remove_escape(v),
    'nocolorx': lambda v: _remove_colors(v),
    'nonl': lambda v: v.replace('\n', ' '),
    'strip': lambda v: v.strip(),
    'strip_brackets': _strip_brackets
}

for k,f in __xonsh__.env.get('XONTRIB_PROMPT_BAR_WRAPPERS', {}).items():
    _wrappers[k] = f

def _format_sections(s):
    sections = [fname for _, fname, _, _ in Formatter().parse(s) if fname]
    sections_len = len(sections)
    map = {}
    for i, key in enumerate(sections):
        real_key = key
        wrappers = None
        if '#' in key:
            real_key, wrappers = key.split('#', 1)
            wrappers = wrappers.split('#')
        if real_key in __xonsh__.env['PROMPT_FIELDS']:
            if callable(__xonsh__.env['PROMPT_FIELDS'][real_key]):
                v = __xonsh__.env['PROMPT_FIELDS'][real_key]()
            else:
                v = __xonsh__.env['PROMPT_FIELDS'][real_key]

            if v is None or v == '':
                map[key] = ''
            elif wrappers:
                map[key] = v
                for wrapper in wrappers:
                    if wrapper in _wrappers:
                        map[key] = _wrappers[wrapper](map[key])
            else:
                map[key] = str(v)

            if map[key] and i != sections_len-1:
                map[key] = map[key] + ' '
        else:
            map[key] = key
    return s.format_map(map)

def _prompt_bar():
    # Jump to parent if the current directory does not exist.
    try:
        d = Path(__xonsh__.env['PWD'])
        nd = d
        while not nd.exists():
            nd = nd.parent
        if nd != d:
            printx(f'{{YELLOW}}The directory {d} does not exist. Jump to parent: {nd}{{RESET}}')
            execx(f'cd {repr(str(nd))}')
    except:
        pass

    # Get the terminal size
    try:
        ts = os.get_terminal_size()
        cols = ts.columns
    except Exception as e:
        return f'xontrib-prompt-bar error: {e}'

    # Formatting the sections and calculating the bar length
    lpc = _format_sections(_LEFT)
    rpc = _format_sections(_RIGHT)
    lp = _replace_emoji(_remove_colors(lpc))
    rp = _replace_emoji(_remove_colors(rpc))
    w = ' ' * ( int(cols) - len(lp) - len(rp) )
    
    # Rendering the prompt
    return f'{_BAR_BG}{_BAR_FG}{lpc}{_BAR_BG}{_BAR_FG}{w}{rpc}'

@events.on_postcommand
def _(**kwargs):
    print('')

__xonsh__.env['PROMPT_FIELDS']['prompt_bar'] = _prompt_bar
__xonsh__.env['PROMPT'] = "{prompt_bar}\n{WHITE}{prompt_end_xonsh}{RESET} "
