<p align="center">  
The bar theme for <a href="https://xon.sh">xonsh shell</a>.
</p>

<p align="center">  
<img src='https://raw.githubusercontent.com/anki-code/xontrib-prompt-bar/master/static/Demo.png' alt='[Demo]'>
<sup><i>Screenshot made in <a href="https://konsole.kde.org/">Konsole</a> with <code>$XONSH_COLOR_STYLE = "paraiso-dark"</code>.</i></sup>
</p>

<p align="center">  
If you like the idea of bar theme click ⭐ on the repo and stay tuned.
</p>

Features:

* Clear concept. The bar is a delimiter and information panel. Three attention aspects: command line and path, output, sections with additional info.

* The command beginning has fixed position to have a large command line every time and avoid mess of attention.

* The sections placed to right but not in the same line as command and it allows you to copy the command and output without environmental disclosure.

* Full customization. Change colors, add sections with info you need easily with Python.


## Install
```
xpip install -U xontrib-prompt-bar
echo 'xontrib load prompt_bar' >> ~/.xonshrc
# Reload xonsh
```

## Use cases

### Fields and colors
The bar theme supports [xonsh default fields and colors notation](https://xon.sh/tutorial.html#customizing-the-prompt).

To customize the appearance of the fields on the bar you can use wrappers:
* `{hostname}` - no wrapper
* `{hostname#section}` - add backlight for the text
* `{hostname#accent}` - bold font and lighter color
* Also you can create your own fields and wrapper. See the section below.

### Add custom fields and wrappers
How to add two new fields called `my_left_custom` and `my_right_custom` and one new wrapper called `brackets`.
```python
$PROMPT_FIELDS['my_left_custom'] = 'Hello left!'
$PROMPT_FIELDS['my_right_custom'] = lambda: '>'*3 + ' {YELLOW}Hello right!'

$XONTRIB_PROMPT_BAR_WRAPPERS = {
    'brackets': lambda v: f'[{v}]'
}

$XONTRIB_PROMPT_BAR_LEFT = '{hostname}{user}{pwd#accent}{my_left_custom#brackets}'
$XONTRIB_PROMPT_BAR_RIGHT = '{my_right_custom#section}{env_name#section}{gitstatus_noc#section}{date_time_tz}'

xontrib load prompt_bar
```
Result:

<img src='https://raw.githubusercontent.com/anki-code/xontrib-prompt-bar/master/static/Demo-custom.png' alt='[Demo custom fields]'>

## Additional links
* [xonsh default fields and colors notation](https://xon.sh/tutorial.html#customizing-the-prompt)
* [Meaning of git status symbols](https://xon.sh/envvars.html#xonsh-gitstatus) (●×+⚑✓↑↓)

## Known issues
### Spaces in the copied and pasted command line
Please update [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) to 3.0.7+ version:
```bash
$ xonfig | grep prompt
| prompt toolkit   | 3.0.3           |
| shell type       | prompt_toolkit  |

$ pip install -U prompt_toolkit
```

## Future
Asynchronous section rendering:
* [Use threads to offload prompt sections - xonsh/pull/3758](https://github.com/xonsh/xonsh/pull/3758)
* [Awesome example from Jonathan Slenders](https://github.com/prompt-toolkit/python-prompt-toolkit/blob/master/examples/prompts/fancy-zsh-prompt.py)
