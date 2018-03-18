if [ "$TRAVIS_OS_NAME" == "osx" ]; then
  brew update
  brew install openssl realine
  brew outdated pyenv || brew upgrade pyenv

  brew install pyenv-virtualenv
  pytenv install $PYTHON
  export PYENV_VERSION=$PYTHON
  export PATH="/Users/travis/.pyenv/shims:${PATH}"
  pyenv-virtualenv env
  source env/bin/activate
  python --version
fi
