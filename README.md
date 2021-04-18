<p align="center">  
    The bar prompt for the <a href="https://xon.sh">xonsh shell</a> with customizable sections.
</p>

<p align="center">  
<img src='https://raw.githubusercontent.com/anki-code/xontrib-prompt-bar/master/static/Demo.png' alt='[Demo]'>
<sup><i>Screenshot made in <a href="https://konsole.kde.org/">Konsole</a> with <code>$XONSH_COLOR_STYLE = "paraiso-dark"</code>.</i></sup>
</p>

<p align="center">  
If you like the idea of bar theme click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/anki-code/xontrib-prompt-bar" target="_blank">tweet</a>.
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

## Default theme

```python
$XONTRIB_PROMPT_BAR_THEME = {
    'left': '{hostname}{user}{cwd_abs#accent}',
    'right': '{env_name#strip_brackets#section}{gitstatus#nocolorx#section}{date_time_tz}',
    'bar_bg': '{BACKGROUND_#323232}',
    'bar_fg': '{#AAA}',
    'section_bg': '{BACKGROUND_#444}',
    'section_fg': '{#CCC}',
    'accent_fg': '{BOLD_#DDD}',
}
xontrib load prompt_bar
```

## Use cases

### Customize the fields

Supported fields:
* [xonsh default fields and colors notation](https://xon.sh/tutorial.html#customizing-the-prompt)
* `screens` - list of the windows that created by [screen window manager](https://www.gnu.org/software/screen/manual/screen.html#Overview) i.e. `screen -S mywin`.
* `cwd_abs` - current absolute path (`~` disabled).
* `date_time_tz` - date and time with timezone i.e. `21-12-25 18:00:00-01`.

To customize the appearance of the fields on the bar you can use wrappers and chaining them:
```python
$XONTRIB_PROMPT_BAR_RIGHT = '{hostname#accent#section} {gitstatus#nocolorx}'
xontrib load prompt_bar
```
Builtin wrappers:
* `section` - add backlight for the text.
* `accent` - bold font and lighter color.
* `noesc` - remove the ANSI escape characters (colors).
* `strip` - remove the white spaces in the begin and end.
* `strip_brackets` - remove the white spaces in the begin and end and then remove the brackets `()[]{}` if the text begins from brackets.
* `nonl` - replace the new line symbols to spaces.
* `nocolorx` - remove the xonsh color tags i.e. `{RED}` or `{#00ff00}`.

To create your own fields and wrapper see the section below.

### Add custom fields and wrappers
How to add two new fields called `my_left_custom` and `my_right_custom` and one new wrapper called `brackets`.
```python
$PROMPT_FIELDS['my_left_custom'] = 'Hello left!'
$PROMPT_FIELDS['my_right_custom'] = lambda: '>'*3 + ' {YELLOW}Hello right!'

$XONTRIB_PROMPT_BAR_WRAPPERS = {
    'brackets': lambda v: f'[{v}]'
}

$XONTRIB_PROMPT_BAR_LEFT = '{hostname}{user}{cwd_abs#accent}{my_left_custom#brackets}'
$XONTRIB_PROMPT_BAR_RIGHT = '{my_right_custom#section}{env_name#strip_brackets#section}{gitstatus#nocolorx#section}{date_time_tz}'

xontrib load prompt_bar
```
Result:

<img src='https://raw.githubusercontent.com/anki-code/xontrib-prompt-bar/master/static/Demo-custom.png' alt='[Demo custom fields]'>

### Themes and colors

To change the bar colors there is setting the theme:

```python
$XONTRIB_PROMPT_BAR_THEME = {
    'left':       '{hostname}{user}{cwd_abs#accent}',
    'right':      '{env_name#strip_brackets#section}{gitstatus#nocolorx#section}{date_time_tz}',
    'bar_bg':     '{BACKGROUND_#FF0000}',
    'bar_fg':     '{#AAA}',
    'section_bg': '{BACKGROUND_#444}',
    'section_fg': '{#CCC}',
    'accent_fg':  '{BOLD_#DDD}',
}
xontrib load prompt_bar
```
To choose the colors there is [HTML Color Picker](https://www.w3schools.com/colors/colors_picker.asp).

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
