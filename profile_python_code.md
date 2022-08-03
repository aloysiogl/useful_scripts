# How to profile python code

Run your scirpt with

```
python -m cProfile -o program.prof {script_path}
```

Then, to see the profile use *snakeviz*

```
snakeviz program.prof
```

