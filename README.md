## VIM commands to convert .txt file into .csv

### Remove preceding white space from all lines
:%s:[\s]+::

### Replace invariate length white space with a comma for all lines
:%s:[\s]+:,:g