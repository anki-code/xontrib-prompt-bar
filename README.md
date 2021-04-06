<p align="center">  
    The bar prompt for the <a href="https://xon.sh">xonsh shell</a> with customizable sections.
</p>

<p align="center">  
<img src='https://raw.githubusercontent.com/anki-code/xontrib-prompt-bar/master/static/Demo.png' alt='[Demo]'>
<sup><i>Screenshot made in <a href="https://konsole.kde.org/">Konsole</a> with <code>$XONSH_COLOR_STYLE = "paraiso-dark"</code>.</i></sup>
</p>

<p align="center">  
If you like the idea of bar theme click ⭐ on the repo and stay tuned.
</p>

Features:

* Zero dependencies. You don't need to install additional packages.

* Clear concept. The bar is a delimiter and information panel. Three attention aspects: command line and path, output, sections with additional info.

* The command beginning has fixed position to have a large command line every time and avoid mess of attention.

* The sections placed to right but not in the same line as command and it allows you to copy the command and output without environmental disclosure.

* Full customization. Change colors, add sections with info you need easily with Python.


## Install
```python
xpip install -U xontrib-prompt-bar
echo 'xontrib load prompt_bar' >> ~/.xonshrc
# Reload xonsh
```

## Use cases

### Fields

The bar theme supports fields:
* [xonsh default fields and colors notation](https://xon.sh/tutorial.html#customizing-the-prompt)
* `screens` - list of the windows that created by [screen window manager](https://www.gnu.org/software/screen/manual/screen.html#Overview)
* `cwd_abs` - current absolute path (`~` disabled)
* `date_time_tz` - date and time with timezone i.e. `21-12-25 18:00:00-01`
* `gitstatus_noc` - the same as xonsh `gitstatus` but without colors

To customize the appearance of the fields on the bar you can use wrappers and chaining them:
```python
$XONTRIB_PROMPT_BAR_RIGHT = '{hostname#accent#section}'
xontrib load prompt_bar
```
Available wrappers:
* `section` - add backlight for the text
* `accent` - bold font and lighter color
* `noesc` - remove ANSI escape characters (colors)
* `strip` - remove white spaces in the begin and end
* `nonl` - replace new line symbols to spaces
* `nocolorx` - remove xonsh color tags i.e. `{RED}` or `{#00ff00}`
* Also you can create your own fields and wrapper. See the section below.

### Add custom fields and wrappers
How to add two new fields called `my_left_custom` and `my_right_custom` and one new wrapper called `brackets`.
```python
$PROMPT_FIELDS['my_left_custom'] = 'Hello left!'
$PROMPT_FIELDS['my_right_custom'] = lambda: '>'*3 + ' {YELLOW}Hello right!'

$XONTRIB_PROMPT_BAR_WRAPPERS = {
    'brackets': lambda v: f'[{v}]'
}

$XONTRIB_PROMPT_BAR_LEFT = '{hostname}{user}{cwd_abs#accent}{my_left_custom#brackets}'
$XONTRIB_PROMPT_BAR_RIGHT = '{my_right_custom#section}{env_name#section}{gitstatus_noc#section}{date_time_tz}'

xontrib load prompt_bar
```
Result:

<img src='https://raw.githubusercontent.com/anki-code/xontrib-prompt-bar/master/static/Demo-custom.png' alt='[Demo custom fields]'>

### Themes and colors

To change the bar colors there is setting the theme:

```python
$XONTRIB_PROMPT_BAR_THEME = {
    'left':       '{hostname}{user}{cwd_abs#accent}',
    'right':      '{env_name#section}{gitstatus_noc#section}{date_time_tz}',
    'bar_bg':     '{BACKGROUND_#FF0000}',
    'bar_fg':     '{#AAA}',
    'section_bg': '{BACKGROUND_#444}',
    'section_fg': '{#CCC}',
    'accent_fg':  '{BOLD_#DDD}',
}
xontrib load prompt_bar
```

### Using [Starship](https://github.com/starship/starship) cross-shell prompt to rendering right sections

Barship using [xontrib-prompt-starship](https://github.com/anki-code/xontrib-prompt-starship):

```python
# First of all create a starship config to return sections in one line
$XONTRIB_PROMPT_STARSHIP_RIGHT_CONFIG = "~/.config/starship_xonsh_right.toml"
$XONTRIB_PROMPT_STARSHIP_REPLACE_PROMPT = False
$XONTRIB_PROMPT_BAR_RIGHT = '{starship_right#noesc#nonl#strip}'
xontrib load prompt_starship prompt_bar
```

Result:

<img src="https://raw.githubusercontent.com/anki-code/xontrib-prompt-bar/master/static/xontrib-prompt-bar-starship.png" alt="Prompt bar with starship sections.">


### Additional links
* [Asynchronous section rendering](https://xon.sh/envvars.html#enable-async-prompt)
* [xonsh default fields and colors notation](https://xon.sh/tutorial.html#customizing-the-prompt)
* [Meaning of git status symbols](https://xon.sh/envvars.html#xonsh-gitstatus) (●×+⚑✓↑↓)
* [Awesome example of rewriting the theme from Jonathan Slenders](https://github.com/prompt-toolkit/python-prompt-toolkit/blob/master/examples/prompts/fancy-zsh-prompt.py)
* [Customization the colors in the input line](https://github.com/xonsh/xonsh/pull/3878#issuecomment-707982828)

## Known issues
### Spaces in the copied and pasted command line
Please update [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) 
to 3.0.7+ version via `python -m pip install -U prompt_toolkit`.

## Credits 
* This package is the part of [ergopack](https://github.com/anki-code/xontrib-ergopack) - the pack of ergonomic xontribs.
* This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).
