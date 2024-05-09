from click_shell import shell
from jellyfin_apiclient_python import JellyfinClient
from login import login_func
from library import library_func

client = JellyfinClient()
client.config.app('your_brilliant_app', '0.0.1', 'machine_name', 'unique_id')


@shell(prompt='Deltafin > ', intro='Welcome to Deltafin! Type `help` to see available commands.')
def deltafin():
    pass


@deltafin.command()
def help():
    print("""Available commands:
    - help: Display this help message.
    - login: Log in to your Jellyfin server.
    - library: Output and explore existing library categories.
    - quit: Exit the Jellyfin CLI.
    """)


@deltafin.command()
def login():
    login_func(client)


@deltafin.command()
def library():
    library_func(client)


if __name__ == '__main__':
    deltafin()
