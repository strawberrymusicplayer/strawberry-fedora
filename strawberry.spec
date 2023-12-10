%bcond_without tests

%global giturl https://github.com/strawberrymusicplayer/strawberry

Name:           strawberry
Version:        1.0.22
Release:        %autorelease
Summary:        Audio player and music collection organizer

# MIT:
#   3rdparty/kdsingleapplication
# Apache-2.0:
#   src/utilities/timeconstants.h
#   ext/libstrawberry-common/core/logging.{cpp,h}
#   ext/libstrawberry-common/core/messagehandler.{cpp,h}
# GPL-2.0-or-later:
#   src/engine/gstengine.{cpp,h}
# GPL-3.0-or-later:
#   everything else
License:        MIT AND Apache-2.0 AND GPL-2.0-or-later AND GPL-3.0-or-later
URL:            https://www.strawberrymusicplayer.org/
Source:         %{giturl}/archive/%{version}/%{name}-%{version}.tar.gz

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
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libchromaprint)
BuildRequires:  pkgconfig(libebur128)
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Sql)
%if %{with tests}
BuildRequires:  pkgconfig(Qt5Test)
%endif
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(sqlite3) >= 3.7
BuildRequires:  pkgconfig(taglib) >= 1.11
%ifnarch s390 s390x
BuildRequires:  pkgconfig(libgpod-1.0)
%endif
BuildRequires:  qt5-linguist

%if %{with tests}
BuildRequires:  cmake(GTest)
BuildRequires:  pkgconfig(gmock)
%endif

Requires:       gstreamer1-plugins-good
Requires:       hicolor-icon-theme

# Upstream: https://github.com/KDAB/KDSingleApplication/
# Has no soname nor Qt5/6 parallel installability support, so bundle it
# for now...
Provides:       bundled(kdsingleapplication)

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

# BSD-3-Clause.txt applies only to build files that are not included in
# strawberry's kdsingleapplication copy.
mv 3rdparty/kdsingleapplication/LICENSES/MIT.txt LICENSE-kdsingleapplication

# Remove unneeded 3rdparty to ensure they don't get accidentally bundled
rm -rf 3rdparty/getopt
rm -rf 3rdparty/SPMediaKeyTap

%if %{with tests}
# Disable tests that need graphical environment and thus don't work in mock
sed -i '/add_test_file(.* true)/d' tests/CMakeLists.txt
%endif

%build
%{cmake} -DBUILD_WERROR:BOOL=OFF \
         -DBUILD_WITH_QT5=ON \
         -DCMAKE_BUILD_TYPE:STRING=Release
%cmake_build

%install
%cmake_install

%check
%if %{with tests}
%{cmake_build} -t run_strawberry_tests
%endif

desktop-file-validate %{buildroot}%{_datadir}/applications/org.strawberrymusicplayer.strawberry.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.strawberrymusicplayer.strawberry.appdata.xml

%files
%license COPYING LICENSE-kdsingleapplication
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
