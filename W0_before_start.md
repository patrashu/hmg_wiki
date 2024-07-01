## Mac 환경 설정

### Homebrew 설치

- homebrew란 macOS 및 Linux용으로 설계된 패키지 관리 시스템으로써, 소프트웨어 패키지를 쉽게 설치하고 관리할 수 있도록 도와준다.
- ㄹhomebrew를 설치한 후에 “**brew install ~~**”와 같은 명령어를 통해 개발에 필요한 도구들(git, …)을 설치할 수 있다.
- 설치 방법 (생각보다 오래걸린다. 기다리도록)
    
    ```jsx
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
    
- Brew를 설치하지 않고 Git을 설정하려고 했을때 발생했던 Error
    - homebrew를 설치하지 않은 상태로 git을 사용하려고 시도했으나, xcode가 설치되어있지 않다고 에러가 떠서 실패했다.
    - 구글에 검색해서 PATH를 추가하면 xcode 설치없이도 해결이 가능하다고 말했으나, 해당 명령어를 사용했을 때 에러를 해결하지 못했다.
    - 맥북의 환경설정은 M1칩 이전과 이후로 약간의 차이를 보이며, 내가 참고했던 블로그는 M1이전 Intel CPU일 때 환경설정하는 방법이었다.
    - 참고 Link: https://cpdev.tistory.com/37
    
    ```bash
    echo "PATH=/usr/local/git/bin:\$PATH" >> ~/.bash_profile # M1 이전
    echo "PATH=/opt/homebrew/bin:\$PATH" >> ~/.bash_profile # M1 이후
    
    source ~/.bash_profile # 변경된 bash_profile 적용
    ```
    

### Git 설치 및 초기 계정 세팅

- Git은 개발자 간 협업을 위해 사용되는 도구로써, 브랜치 관리를 통해 코드의 버전 관리가 가능하며 각 커밋마다의 변경 사항을 쉽게 파악할 수 있다.
- 현재 작업 중인 코드를 Github에 올려두, 다른 환경에서도 개발이 가능하다는 장점이 존재한다.
- git 설치 및 초기 세팅
    
    ```bash
    brew install git
    
    # git 최초 설정
    git config --global user.name "user name"
    git config --global user.email "user email"
    
    # 확인
    git config --list
    ```
    
- Github Token은 최초 1회 open후 hide가 되기 때문에 기록해두자.

### 개발 환경 구축 (Pyenv + poetry)

- **Pyenv**는 다양한 파이썬 버전을 쉽게 설치하고 관리할 수 있도록 도와주는 도구로써, 동일한 시스템 내에서 서로 다른 프로젝트마다 다른 파이썬 버전을 활용하여 환경을 구축할 수 있습니다.
- 다양한 환경 (Mac, Linux, Windows)에서 모두 활용이 가능하여 범용성이 좋다.
- Conda를 사용하게 되면 초기 다운로드를 진행할 때 기본 Python 버전을 설치하게 되는데, 이 또한 너무 무겁고 잘 사용을 안하게 되더라~
- Pyenv + Virtualenv로 보통 프로젝트를 많이 진행함.

<br>

- **Poetry**는 파이썬 프로젝트의 의존성을 관리하고 패키지를 빌드하고 배포하는 것을 돕는 도구로써, Poetry를 사용하면 프로젝트 의존성 관리와 가상 환경 설정을 쉽게 할 수 있습니다
- 프로젝트 내 모든 의존성 패키지들은 “**pyproject.toml**”에 저장됨.
- 프로젝트별로 자동으로 가상환경을 생성하고 관리해주기 때문에 의존성 충돌을 방지할 수 있음.
- 개발/배포시 사용하는 라이브러리 환경을 다르게 관리할 수 있다는 장점이 존재함.

- Pyenv install in mac
    
    ```bash
    g# Install
    brew install pyenv 
    
    # 환경변수 설정
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    
    # 적용 (터미널 껏다가 켜도 됨)
    source ~/.zshrc
    
    # 원하는 파이썬 버전 install 후 global/local하게 적용
    pyenv install 3.x.x  # 원하는 Python 버전
    pyenv global 3.x.x   # 기본 Python 버전 설정
    pyenv local 3.x x # ~~ directory내 python 버전 설정
    ```
    
- poetry install in mac
    
    ```bash
    # install하기 전 pyenv/자체적인 python 설치 후에 실행되여야 함.
    curl -sSL https://install.python-poetry.org | python3 -
    
    # 환경변수 추가
    export PATH="/Users/admin/.local/bin:$PATH"
    
    # 적용
    source ~/.zshrc
    ```
    

### Iterms2 설치

- DownLoad Link: https://iterm2.com/downloads.html
- settings가서 터미널 꾸미기 진행(CPU / RAM / Network / Clock / …)
- Black화면 선호하면 color → background를 black으로 변경

### Oh my zsh 설치

- Oh My Zsh는 Zsh를 위한 커스터마이징 가능한 프레임워크로써, 다양한 테마와 플러그인을 제공하여 터미널 경험을 향상시킬 수 있다.
- oh my zsh install
    - 원하는 테마나 플러그인 (auto suggestion 같은 것들)은 원하는 개발환경에 맞게 세팅하면 됨
    
    ```bash
    # install 
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    
    # auto-suggestion plugin / zsh-syntax-highlighting 설치
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
    git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
    
    # plugin 환경변수 설정
    vi ~/.zshrc
    plugins=(git zsh-syntax-highlighting zsh-autosuggestions)
    
    # 적용
    source ~/.zshrc
    ```