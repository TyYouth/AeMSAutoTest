##### PEP8

get more detail from https://realpython.com/python-pep8/
```
class: ClassName(object), Class(object)
method/function: method_name, method
variable: var, my_variable
Constant variable: CONSTANT,LOG_PATH
Module: module.py, my_module.py
package: package, mypackage
```

the name need to be clear and easy to read so that humands knows what it is about
example: ok_btn, username_text_input, is_selected

about the code layout: Ctrl + Alt + L to help in Pycharm
about the Tabs and Spaces: 4 Tabs is what we convention, setting in Pycharm python code style: tab size
* Prohibit mixed use of space and Tab  

Blank Lines:
Surround top-level functions and classes with two blank lines.
Surround method definitions inside classes with a single blank line.
Use blank lines sparingly inside functions to show clear steps
example: 
```
class MyFirstClass(object):
    def __init__(self):
        pass

    def first_method(self):  # a single lines to spearate with above inside method __init__
        for number in number_list:
            sum_list = sum_list + number
        mean = sum_list / len(number_list)

        sum_squares = 0  # Use blank lines sparingly inside functions to show clear steps
        for number in number_list:
            sum_squares = sum_squares + number**2
        mean_squares = sum_squares / len(number_list)
    
        return mean_squares - mean**2

class MySecondClass(object):  # two blank lines to spearate with MyFirstClass
    pass


def top_level_function():
    return None
```

Documentation Strings
* Surround docstrings with three double quotes on either side, as in """This is a docstring"""  
* Write them for all public modules, functions, classes, and methods  
* Put the """ that ends a multi-line docstring on a line by itself  
example:
```
the doc of unittest test case is neccessary:
    def test_00100_user_prompt(self):
        """test the prompt of user input box"""

The underlying function must be commented and provide at least one example 
function is BasePage, 
    def get_prompt_msg(self, show_value=None):
        """
        Most of the prompts include similar content
        <small class="help-block" ng-show="show value" >msg text</small>
        :param show_value: value of ng-show
        :return: str, prompt message
        prompt_msg = BasePage.get_prompt_msg(show_value='xxx')
        """

```


















