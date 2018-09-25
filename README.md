# Sublime ESLint Fix
A Sublime Text 3 plugin to run eslint --fix on the current file

## Installation

### Dependencies
This plugin requires ESLint in order to function. For information on installing ESLint, check out the [Getting Started guide](https://eslint.org/docs/user-guide/getting-started).

### Plugin Installation
This plugins is installable via [Package Control](https://packagecontrol.io/installation).

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `eslint fix`. Among the entries you should see `ESLint Fix`. Select this entry to install it.

## Commands
**Command Palette**

* ESLint Fix: Fix this file

**Default hotkeys:**

* Linux/Windows: [Ctrl + KE]
* Mac: [Cmd + KE]

## Settings

By default, the following settings are used:

```javascript
{
	// The paths to look for executables
	"paths": {
		"linux": [],
		"osx": [],
		"windows": []
	},

	// The location to search for a locally installed eslint package.
	// These are all relative paths to a project's directory.
	// If this is not found, it will try to fallback to a global package
	// (see 'eslint_path' below)
	"local_eslint_path": {
		"windows": "node_modules/eslint/bin/eslint.js",
		"linux": "node_modules/.bin/eslint",
		"osx": "node_modules/.bin/eslint"
	},

	// Specify this path to an eslint config file to override the default behavior.
	// Passed to eslint as --config. Read more here:
	// http://eslint.org/docs/user-guide/command-line-interface#c---config
	// If an absolute path is provided, it will use as is.
	// Else, it will look for the file in the root of the project directory.
	// Failing either, it will skip the config file
	"config_path": {
		"windows": "",
		"linux": "",
		"osx": ""
	},
}
```

You can modify any settings by going to `Preferences > Package Settings > ESLint Fix > Settings`.

### Project-Specific Settings Override

To override global plugin configuration for a specific project, add a settings object with an `eslint-fix` key in your `.sublime-project`. This file is accessible via `Project -> Edit Project`.

For example:

```
{
	"folders": [
		{
			"path": "."
		}
	],
	"settings": {
		"config_path": {
			"windows": "..."
		}
	}
}
```

### Acknowledgments
While the code is unique, some of it is inspired by [this plugin](https://github.com/TheSavior/ESLint-Formatter). My plugin differs by running on the current buffer instead of the last saved state of the file.
