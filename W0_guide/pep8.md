## Pep 8 Style guide in python

- Reference Link: https://peps.python.org/pep-0008/

### Indentation

- Indentation(들여쓰기)는 space 4칸으로 설정한다.
- 공식 문서에서는 Tab보다는 Space를 더 선호한다. (섞어서 쓰지 말 것!)
- hanging indentaiton을 진행할 때(여러 줄 걸쳐서), 개행이 있을 경우 상위 line에서 space 4칸을 추가로 들여쓰기하여 진행한다.
- 예시
    
    ```python
    # Correct:
    # Aligned with opening delimiter.
    foo = long_function_name(var_one, var_two,
                                var_three, var_four)
    
    # Add 4 spaces (an extra level of indentation) to distinguish arguments from the rest.
    def long_function_name(
            var_one, var_two, var_three,
            var_four):
        print(var_one)
        
    # Wrong:
    # Arguments on first line forbidden when not using vertical alignment.
    foo = long_function_name(var_one, var_two,
        var_three, var_four)
    
    # Further indentation required as indentation is not distinguishable.
    def long_function_name(
        var_one, var_two, var_three,
        var_four):
        print(var_one)
    ```
        
- 함수 / 자료구조를 정의 / 사용할 때 closing bracket ( ‘)’, ‘]’, … )은 아래 두 가지 모두 활용 가능
- 예시
    
    ```python
    my_list = [
        1, 2, 3,
        ]
        
    my_list = [
        1, 2, 3,
    ]
    ```
        

### Limit character per line

- 하나의 line에 79 character 이상을 작성하지 말자 (너무 길게 쓰지마라는 뜻)
- 길어질 경우 역 슬래시 ‘\’를 활용하여 적절하게 개행을 진행하자. 개행시에 Indentation는 필수
- 예시
    
    ```python
    with open('/path/to/some/file/you/want/to/read') as file_1, \
            open('/path/to/some/file/being/written', 'w') as file_2:
        file_2.write(file_1.read())
    ```
        

### Blank Lines

- Function과 Function, Class와 Class 사이는 기본적으로 2line 개행하는 것을 원칙으로 한다.
- Class 내부의 Method들은 1line을 개행하는 것을 원칙으로 한다.
- 예시
    
    ```python
    class Person:
            def __init__(self, name):
                    self.name = name
            
            def get_name(self):
                    return self.name
                    
    
    class Animal:
            def __init__(self, name):
                    self.name = name
            
            def get_name(self, name):
                    return self.name
    ```
        

### Imports

- 라이브러리를 import 할 때 기본적으로 한 line에 하나의 library만 import한다
- 패키지/타 모듈에서 라이브러리를 불러와 import하는 경우 한 번에 여러 개가 가능
- 패키지/타 모듈에서 import *을 하게 되면 패키지/모듈 내 모든 함수/클래스/변수를 사용할 수 있지만, 모듈 간 동일한 함수명이 존재하는 경우 충돌이 발생할 수 있으며 로딩하는 속도가 느리기 때문에 Pep8에서는 지양한다.
- 기본적으로는 절대 경로로 import하라고 권장한다. (상대 경로는 꼬일 수 있기 때문)
- 예시
    
    ```python
    import os, sys # Wrong
    import os
    import sys
    
    from subprocess import Popen, PIPE # Correct
    
    # Correct
    import pkgname.pkgfunc
    from pkgname import pkgfunc 
    ```
        

### Whitespace in Expressions and Statements

- 콤마(,)/콜론(:) 뒤에는 기본적으로 한 칸 띄어쓰기를 진행한다.
- Bracket 시작/끝에는 추가로 띄어쓰기를 진행하지 않는다.
- Func/Dict/ 뒤 Bracket의 경우 띄어쓰기를 진행하지 않는다.
- 예시
    ```python
    # Correct
    spam(ham[1], {eggs: 2})
    foo = (0,)
    if x == 4: print(x, y); x, y = y, x
    ```
    

### Additional Recommendations

- Arrow (→)를 사용할 때는 앞/뒤로 개행을 진행한다. ( () → ~~~: )
- parameter에 = sign을 사용할 때는 띄어쓰기를 진행하지 않는다. (param1=0.0)
- 그렇지만, Type Hinting(Annotation)을 사용할 때는 띄어쓰기를 진행한다
    - 예시
        
        ```python
        def complex(real, imag=0.0):
            return magic(r=real, i=imag)
            
        def munge(sep: AnyStr = None) -> None: ...
        def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...
        ```
        

### DocString

- 여러 줄에 걸쳐서 사용할 경우 아래 예시와 같이 진행한다.
- 한 줄에 사용할 경우 “”” “”” 을 한 줄에 모두 작성할 수 있도록 한다.
- 예시
    
    ```python
    """Return a foobang
    
    Optional plotz says to frobnicate the bizbaz first.
    """
    
    """Return an ex-parrot."""
    ```
        

### Naming Conventions

- 단일 문자 변수 이름으로 'l'(소문자 엘), 'O'(대문자 오) 또는 'I'(대문자 아이)를 사용하지 말자.
- 파이썬에서 클래스 이름은 CamelCase로 작성한다.
- 파이썬에서 함수 및 변수/모듈 이름은 snake_case로 작성한다.
- 파이썬에서 상수는 UPPER_SNAKE_CASE로 작성한다.
- 파이썬에서 변수 앞에 _, __을 붙일 경우 비공개 변수로써 선언할 수 있다.
- 파이썬에서 매직 메서드는 양쪽에 __init__ 던더 메서드가 붙는다.