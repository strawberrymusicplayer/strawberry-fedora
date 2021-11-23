Name:           strawberry
Version:        0.9.3
Release:        %autorelease
Summary:        Audio player and music collection organizer

# Main program: GPLv3
# src/analyzer and src/engine/gstengine and src/engine/xineengine: GPLv2
# 3rdparty/taglib, src/widgets/fancytabwidget and src/widgets/stylehelper: LGPLv2
# 3rdparty/singleapplication: MIT
# 3rdparty/utf8-cpp: Boost
# src/core/timeconstants.h and ext/libstrawberry-common/core/logging and ext/libstrawberry-common/core/messagehandler: ASL 2.0
License:        GPLv2 and GPLv3+ amd LGPLv2 and ASL 2.0 and MIT and Boost
URL:            https://www.strawberrymusicplayer.org/
Source0:        https://github.com/strawberrymusicplayer/strawberry/archive/%{version}/%{name}-%{version}.tar.gz

Patch4:         strawberry-udisks-headers.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libchromaprint)
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudf)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(phonon4qt5)
BuildRequires:  pkgconfig(sqlite3) >= 3.7
BuildRequires:  pkgconfig(taglib) >= 1.11
%ifnarch s390 s390x
BuildRequires:  pkgconfig(libgpod-1.0)
%endif
BuildRequires:  qt5-linguist

Requires:       gstreamer1-plugins-good
Requires:       hicolor-icon-theme

Provides:       bundled(singleapplication)
Provides:       bundled(taglib) = 1.12-1
Provides:       bundled(utf8-cpp)

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

%build
# QT applications need to avoid local binding and copy relocations.  Forcing them to build with
# -fPIC solves that problem
export CXXFLAGS="-fPIC $RPM_OPT_FLAGS"
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
