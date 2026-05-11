import subprocess

def open_neovim():
    try:
        subprocess.Popen(['kitty', '--directory', '~/projects/A.R.C/', 'nvim', '.'])

        print("Welcome home sir!")
    except FileNotFoundError:
        print("kitty not found")
    except Exception as e:
        print(f"Error opening Neovim: {e}")

