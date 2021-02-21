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
_NOC = '{RESET}'

def _remove_colors(s):
    if s is None:
        return ''
    return re.sub('{([A-Z0-9#_]+?)}', '', s)

def _field_date_time_tz():
    t = time.strftime('%y-%m-%d %H:%M:%S%z', time.localtime())
    return t[:-2] if t[-2:] == '00' else t


__xonsh__.env['PROMPT_FIELDS']['env_prefix'] = __xonsh__.env['PROMPT_FIELDS']['env_postfix'] = ''
__xonsh__.env['PROMPT_FIELDS']['cwd_abs'] = lambda: str(Path(__xonsh__.env['PROMPT_FIELDS']['cwd']()).expanduser())
__xonsh__.env['PROMPT_FIELDS']['date_time_tz'] = _field_date_time_tz
__xonsh__.env['PROMPT_FIELDS']['gitstatus_noc'] = lambda: _remove_colors(__xonsh__.env['PROMPT_FIELDS']['gitstatus']())
__xonsh__.env['PROMPT_FIELDS']['screens'] = lambda: ', '.join([l.split('\t')[1].split('.')[1] for l in $(screen -list).splitlines() if '\t' in l])

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
        if real_key in __xonsh__.env['PROMPT_FIELDS']:
            if callable(__xonsh__.env['PROMPT_FIELDS'][real_key]):
                v = __xonsh__.env['PROMPT_FIELDS'][real_key]()
            else:
                v = __xonsh__.env['PROMPT_FIELDS'][real_key]
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
    
    return f'{_BARBG}{_BARFG}{lpc}{_BARBG}{_BARFG}{w}{rpc}'

@events.on_postcommand
def _(**kwargs):
    print('')

__xonsh__.env['PROMPT_FIELDS']['prompt_bar'] = _prompt_bar
__xonsh__.env['PROMPT'] = "{prompt_bar}\n{WHITE}{prompt_end}{RESET} "
