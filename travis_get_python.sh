if [ "$TRAVIS_OS_NAME" == "osx" ]; then
  brew update
  #brew install openssl realine
  brew outdated pyenv || brew upgrade pyenv

  brew install python@{$PYTHON}
  brew link --overwrite python@{$PYTHON}
  sudo easy_install pip
  pip install --upgrade pip setuptools
  pip install virtualenv
  python -m virtualenv env
  source env/bin/activate
  python --version
fi
