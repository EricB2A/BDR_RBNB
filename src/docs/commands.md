# What are commands
Commands are what the cli can do. Each command must contain a namespace that isn't already registered.

# Creating new command

```cli/commands/my_new_command.py```
```

```

Then you must change the ```cli/commands/__init__.py``` and add your new class like so
```
commands = {
   ....
   'my_new_command': MyNewCommand()
}
```