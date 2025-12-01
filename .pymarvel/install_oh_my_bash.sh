if [ ! -d "$HOME/.oh-my-bash" ]; then
    echo "Oh-My-Bash is not installed. Installing now..."
    wget https://raw.github.com/ohmybash/oh-my-bash/master/tools/install.sh -O - | bash
else
    echo "Oh-My-Bash is already installed."
fi
