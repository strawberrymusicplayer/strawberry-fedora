Name:           strawberry
Version:        1.0.3
Release:        %autorelease
Summary:        Audio player and music collection organizer

# Main program: GPLv3
# src/analyzer and src/engine/gstengine and src/engine/xineengine: GPLv2
# src/widgets/fancytabwidget and src/widgets/stylehelper: LGPLv2
# 3rdparty/singleapplication: MIT
# src/core/timeconstants.h and ext/libstrawberry-common/core/logging and ext/libstrawberry-common/core/messagehandler: ASL 2.0
License:        GPLv2 and GPLv3+ and LGPLv2 and ASL 2.0 and MIT and Boost
URL:            https://www.strawberrymusicplayer.org/
Source0:        https://github.com/strawberrymusicplayer/strawberry/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libchromaprint)
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(sqlite3) >= 3.7
BuildRequires:  pkgconfig(taglib) >= 1.11
%ifnarch s390 s390x
BuildRequires:  pkgconfig(libgpod-1.0)
%endif
BuildRequires:  qt5-linguist

Requires:       gstreamer1-plugins-good
Requires:       hicolor-icon-theme

Provides:       bundled(singleapplication)

%description
Strawberry is a audio player and music collection organizer.
It is a fork of Clementine. The name is inspired by the band Strawbs.

Features:
  * Play and organize music
  * Supports WAV, FLAC, WavPack, DSF, DSDIFF, Ogg Vorbis, Speex, MPC,
    TrueAudio, AIFF, MP4, MP3 and ASF
  * Audio CD playback
  * Native desktop notifications
  * Playlists in multiple formats
  * Advanced output and device options with support for bit perfect playback
    on Linux
  * Edit tags on music files
  * Fetch tags from MusicBrainz
  * Album cover art from Last.fm, Musicbrainz and Discogs
  * Song lyrics from AudD and API Seeds
  * Support for multiple backends
  * Audio analyzer
  * Equalizer
  * Transfer music to iPod, iPhone, MTP or mass-storage USB player
  * Integrated Tidal support
  * Scrobbler with support for Last.fm, Libre.fm and ListenBrainz

%prep
%autosetup -p1
mv 3rdparty/singleapplication/LICENSE LICENSE-singleapplication

# Remove unneeded 3rdparty to ensure they don't get accidentally bundled
rm -rf 3rdparty/getopt
rm -rf 3rdparty/macdeployqt
rm -rf 3rdparty/SPMediaKeyTap

%build
%{cmake} -DBUILD_WERROR:BOOL=OFF \
         -DCMAKE_BUILD_TYPE:STRING=Release
%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.strawberrymusicplayer.strawberry.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.strawberrymusicplayer.strawberry.appdata.xml

%files
%license COPYING LICENSE-singleapplication
%doc Changelog
%{_bindir}/strawberry
%{_bindir}/strawberry-tagreader
%{_metainfodir}/org.strawberrymusicplayer.strawberry.appdata.xml
%{_datadir}/applications/org.strawberrymusicplayer.strawberry.desktop
%{_datadir}/icons/hicolor/*/apps/strawberry.*
%{_mandir}/man1/strawberry.1.*
%{_mandir}/man1/strawberry-tagreader.1.*

%changelog
%autochangelog
