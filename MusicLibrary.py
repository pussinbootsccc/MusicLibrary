import shlex
import sys
from Utils import *

__author__ = "Carol Cha"
__email__ = "rigi.thu@gmail.com"
__version__ = "0.01"

class Artist:
    def __init__(self, name):
        self.name = name
        self.albums = {}

    def find_album(self, name):
        """Fetch the album by the album name.
        """
        return self.albums[name] if name in self.albums else None

    def add_album(self, name):
        """Add a new album to the artist.
        """
        if name not in self.albums:
            self.albums[name] = Album(name)
            return True
        return False

class Album:
    def __init__(self, name):
        self.name = name
        self.tracks = {}

    def find_track(self, name):
        """Fetch the track by the track name.
        """
        return self.tracks[name] if name in self.tracks else None

    def add_track(self, name):
        """Add a new track to the album.
        """
        if name not in self.tracks:
            self.tracks[name] = Track(name)
            return True
        return False

class Track:
    def __init__(self, name):
        self.name = name

class MusicLibrary:
    def __init__(self):
        self.artists = {}
        self.artist_playcount = {}
        self.track_playcount = {}

        # cache variables for the leader board of tracks
        self.cache_tracks = None
        # indicates whether the tracks cache is up-to-date
        self.cache_tracks_up_to_date = False

        # cache variables for the leader board of artists
        self.cache_artists = None
        # indicates whether the artists cache is up-to-date
        self.cache_artists_up_to_date = False

    def add_artists(self, artist_name):
        """Add a new artist to the music library.
        """
        if artist_name in self.artists:
            display_error("Artist \"%s\" already exists." % artist_name)
            return
        artist = Artist(artist_name)
        self.artists[artist_name] = artist
        self.artist_playcount[artist] = 0
        self.cache_artists_up_to_date = False

    def find_artist(self, name):
        """Fetch the artist by the artist name.
        """
        return self.artists[name] if name in self.artists else None

    def smart_find(self, track_name=None, album_name=None, artist_name=None):
        """Fetch entities of different granularities based on the given input. 

        Usage:
            Find an artist:
                find(artist_name=artist_name)

            Find an album by some artist:
                find(album_name=album_name, artist_name=artist_name)

            Find a track on some album by some artist:
                find(track_name=track_name, album_name=album_name, artist_name=artist_name)
        """

        if not artist_name:
            return None, None, None

        artist = self.find_artist(artist_name)
        if not artist:
            display_error("Artist \"%s\" does not exist." % artist_name)
            return None, None, None

        if not album_name:
            return None, None, artist

        album = artist.find_album(album_name)
        if not album:
            display_error("Album \"%s\" does not exist by artist \"%s\"." % (album_name, artist_name))
            return None, None, artist

        if not track_name:
            return None, album, artist

        track = album.find_track(track_name)
        if not track:
            display_error("Track \"%s\" does not exist on album \"%s\" by artist \"%s\"." % (track_name, album_name, artist_name))
            return None, album, artist

        return track, album, artist

    def add_album(self, album_name, artist_name):
        """Add a new album to the library.
        """
        _, _, artist = self.smart_find(artist_name=artist_name)
        if not artist:
            return
        if not artist.add_album(album_name):
            display_error("Album \"%s\" already exists by artist \"%s\"." % (album_name, artist_name))
            return

    def show_albums(self, artist_name):
        """List all albums by the given artist.
        """
        _, _, artist = self.smart_find(artist_name=artist_name)
        if not artist:
            return
        display_table(artist.albums.keys(), "Albums of artist \"%s\"" % artist_name)

    def add_track(self, track_name, album_name, artist_name):
        """Add a new track to the library.
        """
        _, album, _ = self.smart_find(artist_name=artist_name, album_name=album_name)
        if not album:
            return
        if not album.add_track(track_name):
            display_error("Track \"%s\" already exists on album \"%s\" by artist \"%s\"." % (track_name, album_name, artist_name))
            return

        track = album.tracks[track_name]
        self.track_playcount[track] = 0
        self.cache_tracks_up_to_date = False

    def show_tracks(self, album_name, artist_name):
        """List all tracks on the given album by the given artist.
        """
        _, album, _ = self.smart_find(artist_name=artist_name, album_name=album_name)
        if not album:
            return
        display_table(album.tracks.keys(), "Tracks on album \"%s\" by artist \"%s\"" % (album_name, artist_name))

    def play(self, track_name, album_name, artist_name):
        """Listen to a track (play count +1).
        """
        track, _, artist = self.smart_find(track_name=track_name, album_name=album_name, artist_name=artist_name)
        if not track:
            return
        self.artist_playcount[artist] += 1
        self.track_playcount[track] += 1
        self.cache_tracks_up_to_date = False
        self.cache_artists_up_to_date = False

    def list_top_tracks(self, N):
        """List the top N tracks according to play count.
        """
        # The results are cached for speed-up.
        if self.cache_tracks_up_to_date and len(self.cache_tracks) >= N:
            tracks = self.cache_tracks[:N]
        else:
            tracks = heap_find_top_N(self.track_playcount, N)
            self.cache_tracks = tracks
            self.cache_tracks_up_to_date = True

        track_names = map(lambda x:x.name, tracks)
        display_table(track_names, "Top %d tracks" % N, displayNumber=True)

    def list_top_artists(self, N):
        """List the top N artists according to play count.
        """
        # The results are cached for speed-up.
        if self.cache_artists_up_to_date and len(self.cache_artists) >= N:
            artists = self.cache_artists[:N]
        else:
            artists = heap_find_top_N(self.artist_playcount, N)
            self.cache_artists = artists
            self.cache_artists_up_to_date = True

        artist_names = map(lambda x:x.name, artists)
        display_table(artist_names, "Top %d artists" % N, displayNumber=True)

    def invalid_input_handler(self):
        """Handle invalid user commands.
        """
        command = raw_input("Invalid input. Need help? [y/n] ")
        if command.lower() in ["y","yes"]:
            self.pop_help()

    def execute(self, command):
        """Parse and execute the command line input.
        """
        args = shlex.split(command.strip())

        try:
            if args[0] == "help":
                self.pop_help()
            elif args[0] == "add":
                if args[1] == "artist":
                    self.add_artists(args[-1])
                elif args[1] == "album":
                    self.add_album(args[2], args[-1])
                elif args[1] == "track":
                    self.add_track(args[2], args[4], args[-1])
                else:
                    self.invalid_input_handler()
                    return
            elif args[0] == "list":
                if args[1] == "albums":
                    self.show_albums(args[-1])
                elif args[1] == "tracks":
                    self.show_tracks(args[3], args[-1])
                elif args[1] == "top":
                    N = int(args[2])
                    if args[3] == "tracks":
                        self.list_top_tracks(N)
                    elif args[3] == "artists":
                        self.list_top_artists(N)
                    else:
                        self.invalid_input_handler()
                        return
                else:
                    self.invalid_input_handler()
                    return
            elif args[0] == "listen":
                self.play(args[2], args[4], args[-1])
            else:
                self.invalid_input_handler()
                return

        except IndexError:
            self.invalid_input_handler()

    def run_test(self, command_log_file):
        """Unit test using an external log of sample commands (e.g. sample_in.txt).
        """
        for command in open(command_log_file):
            self.execute(command)

    def run(self):
        """Launch the music library.
        """
        command = None
        while True:
            command = raw_input("cmd: ")
            if command == "quit":
                break
            self.execute(command)

    def pop_help(self):
        """Show help for the user.
        """
        print
	print "---- help ----"
	print " Add an artist:                                      add artist <artist>"
	print " Add an album:                                       add album <album> by <artist>"
	print " Add a track:                                        add track <track> on <album> by <artist>"
	print " Show albums by artist:                              list albums by <artist>"
	print " Show tracks by album:                               list tracks on <album> by <artist>"
	print " Listen to a track (increase its play count):        listen to <track> on <album> by <artist>"
	print " List the N most popular tracks by play count:       list top <N> tracks"
	print " List the N most popular artists by play count:      list top <N> artists"
	print " Quit:                                               quit"
        print

if __name__ == '__main__':
    ml = MusicLibrary()

    if len(sys.argv) >= 2:
        command_log_file = sys.argv[1]
        ml.run_test(command_log_file)
    else:
        ml.run()

