import os
import re
import time
from pathlib import Path
from string import Formatter

"""
Supported colors: https://xon.sh/tutorial.html#customizing-the-prompt
"""

_LEFT = __xonsh__.env.get('XONTRIB_PROMPT_BAR_LEFT', '{hostname}{user}{cwd_abs#accent}')
_RIGHT = __xonsh__.env.get('XONTRIB_PROMPT_BAR_RIGHT', '{env_name#section}{gitstatus_noc#section}{date_time_tz}')
_BARBG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_BG', '{BACKGROUND_#323232}')
_BARFG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_FG', '{#AAA}')
_SECTION_BG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_SECTION_BG', '{BACKGROUND_#444}')
_SECTION_FG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_SECTION_FG', '{#CCC}')
_ACCENT_FG = __xonsh__.env.get('XONTRIB_PROMPT_BAR_ACCENT_FG', '{BOLD_#DDD}')
_NOC = '{NO_COLOR}'

def _remove_colors(s):
    if s is None:
        return ''
    return re.sub('{([A-Z0-9#_]+?)}', '', s)

def _field_date_time_tz():
    t = time.strftime('%y-%m-%d %H:%M:%S%z', time.localtime())
    return t[:-2] if t[-2:] == '00' else t

$PROMPT_FIELDS['env_prefix'] = $PROMPT_FIELDS['env_postfix'] = ''
$PROMPT_FIELDS['cwd_abs'] = lambda: str(Path($PROMPT_FIELDS['cwd']()).expanduser())
$PROMPT_FIELDS['date_time_tz'] = _field_date_time_tz
$PROMPT_FIELDS['gitstatus_noc'] = lambda: _remove_colors($PROMPT_FIELDS['gitstatus']())

_wrappers = {
    'accent': lambda v: f'{_ACCENT_FG}{v}',
    'section': lambda v: f'{_SECTION_BG}{_SECTION_FG} {v} {_NOC}{_BARBG}{_BARFG}'
}

for k,f in __xonsh__.env.get('XONTRIB_PROMPT_BAR_WRAPPERS', {}).items():
    _wrappers[k] = f

def _format_sections(s):
    sections = [fname for _, fname, _, _ in Formatter().parse(s) if fname]
    sections_len = len(sections)
    map = {}
    for i, key in enumerate(sections):
        real_key = key
        wrapper = None
        if '#' in key:
            real_key, wrapper = key.split('#')
        if real_key in $PROMPT_FIELDS:
            if callable($PROMPT_FIELDS[real_key]):
                v = $PROMPT_FIELDS[real_key]()
            else:
                v = $PROMPT_FIELDS[real_key]
            if v is None or v == '':
                map[key] = ''
            elif wrapper in _wrappers:
                map[key] = _wrappers[wrapper](v)
            else:
                map[key] = str(v)

            if map[key] and i != sections_len-1:
                map[key] = map[key] + ' '
        else:
            map[key] = key
    return s.format_map(map)

def _prompt_bar():
    try:
        ts = os.get_terminal_size()
        cols = ts.columns
    except Exception as e:
        return f'xontrib-prompt-bar error: {e}'

    lpc = _format_sections(_LEFT)
    rpc = _format_sections(_RIGHT)
    lp = _remove_colors(lpc)
    rp = _remove_colors(rpc)

    w = ' ' * ( int(cols) - len(lp) - len(rp) )
    
    nl = '\n'
    try:
        if len(__xonsh__.history) and __xonsh__.history[-1].cmd.strip() in ['clear','']:
            nl = ''
    except:
        pass
    
    return f'{nl}{_BARBG}{_BARFG}{lpc}{_BARBG}{_BARFG}{w}{rpc}'

$PROMPT_FIELDS['prompt_bar'] = _prompt_bar
$PROMPT="{prompt_bar}\n{WHITE}{prompt_end}{NO_COLOR} "
