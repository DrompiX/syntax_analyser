## Syntax analyzer for Python 3.6

We wrote the syntax analyzer for programming language Python 3.6 on the programming language Python 3.6 for all programming language structures and using additional tool ANTLR4. More information about ANTLR you can find on the website [here](http://www.antlr.org/). <br>
> Full grammar for python can be found in src/Python3.g4.


#### Installation of additional libraries
        
1. You should install Python 3.7 from [official website](https://www.python.org/downloads/)

2. Also you should install additional library antlr4-python3-runtime by running command: 
`pip3 install -r requirements.txt`

#### Program start

1. You should put python 3 code inside `in.txt` (remember, in the end of python file should be new line);
2. To run program you should write `python3 launcher.py` (can be `python`) in terminal;
3. Output can be found inside `out.txt`. It has json structure and in case there were no syntax errors there will be correct json-like tree, otherwise it will contain report about errors.