
# Deltafin - A Jellyfin CLI Client.

A basic CLI client for Jellyfin written in Python to playback videos.


## Features

- Login to a local/reverse proxy server
- Automatically logins in to publicly accessable users.
- Lists avaliable categories
- Properly navigates Movies, TV Shows and Music.
- Able to select and playback media.


## Prerequisites
- libmpv.so (needed for the MPV python module).


## Installation

Clone the repository

```bash
  git clone https://github.com/stackneo/deltafin
  cd deltafin
```

Install requirements.txt

```bash
  pip install -r requirements.txt
```

Run the main.py script
```bash
  python main.py
```


## Contributing

Contributions are welcomed and encouraged, feel free to open a PR if you have bug fixes or a new feature you'd like to implement!


## Roadmap

- Support logging in through API Key

- Find an alternative to using selenium to scrape public users

- Potentially make binaries for Windows/Linux.

- Create skynet.


## Acknowledgements

 - This client is powered by [jellyfin-apiclient-python](https://github.com/jellyfin/jellyfin-apiclient-python)
 - The CLI interface is powered by [click-shell](https://github.com/clarkperkins/click-shell)



## License

This project is licensed under the [GPLv3 License](https://choosealicense.com/licenses/gpl-3.0/)

