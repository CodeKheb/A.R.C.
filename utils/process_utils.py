import subprocess

def open_neovim():
    try:
        subprocess.Popen(['kitty', '--directory', '~/projects/A.R.C/', 'nvim', '.'])

        print("Welcome home sir!")
    except FileNotFoundError:
        print("kitty not found")
    except Exception as e:
        print(f"Error opening Neovim: {e}")


def window_right():
    try:
        win_id = subprocess.check_output(
                ['xdotool', 'getactivewindow']
                ).decode().strip()

        width = 1920
        height = 1080

        screen = subprocess.check_output(
            ['xdpyinfo']
        ).decode()

        for line in screen.splitlines():
            if 'dimensions:' in line:
                resolution = line.split()[1]
                width, height = map(int, resolution.split('x'))
                break

        half_width = width // 2

        subprocess.run([
            'wmctrl',
            '-ir',
            win_id,
            '-b',
            'remove,maximized_vert,maximized_horz'
        ])

        subprocess.run([
            'wmctrl',
            '-ir',
            win_id,
            '-e',
            f'0,{half_width},0,{half_width},{height}'
        ])

    except Exception as e:
        print(f"Error Moving to Right: {e}")


def window_left():
    try:
        win_id = subprocess.check_output(
                ['xdotool', 'getactivewindow']
                ).decode().strip()

        width = 1920
        height = 1080

        screen = subprocess.check_output(
            ['xdpyinfo']
        ).decode()

        for line in screen.splitlines():
            if 'dimensions:' in line:
                resolution = line.split()[1]
                width, height = map(int, resolution.split('x'))
                break

        half_width = width // 2

        subprocess.run([
            'wmctrl',
            '-ir',
            win_id,
            '-b',
            'remove,maximized_vert,maximized_horz'
        ])

        subprocess.run([
            'wmctrl',
            '-ir',
            win_id,
            '-e',
            f'0,0,0,{half_width},{height}'
        ])

    except Exception as e:
        print(f"Error Moving to Right: {e}")
