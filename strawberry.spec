%bcond tests 1
%bcond streamtagreader              1
%if %{defined rhel}
%bcond qpa_qplatformnativeinterface %[%{rhel} >= 10]
# https://bugzilla.redhat.com/show_bug.cgi?id=2358081
%bcond gpod                         0
%else
%bcond qpa_qplatformnativeinterface 1
%bcond gpod                         1
%endif

%global giturl https://github.com/strawberrymusicplayer/strawberry

Name:           strawberry
Version:        1.2.17
Release:        %autorelease
Summary:        Audio player and music collection organizer

# Apache-2.0:
#   src/core/logging.{cpp,h}
# MIT:
#   src/widgets/searchfield{.h,_qt.cpp}
#   src/widgets/searchfield_qt_private.{h,cpp}
#   3rdparty/discord-rpc/...
# GPL-2.0-or-later:
#   src/engine/gstengine.{cpp,h}
#   src/widgets/prettyslider.{cpp,h}
#   src/widgets/sliderslider.{cpp,h}
#   src/widgets/volumeslider.{cpp,h}
# GPL-3.0-or-later:
#   everything else
License:        Apache-2.0 AND GPL-2.0-or-later AND GPL-3.0-or-later AND MIT
URL:            https://www.strawberrymusicplayer.org/
Source:         %{giturl}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(alsa)
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
%if %{with streamtagreader}
BuildRequires:  pkgconfig(libsparsehash)
%endif
BuildRequires:  pkgconfig(sqlite3) >= 3.9
BuildRequires:  pkgconfig(taglib) >= 1.12
%if %{with gpod}
BuildRequires:  pkgconfig(libgpod-1.0)
%endif

BuildRequires:  cmake(kdsingleapplication-qt6)
BuildRequires:  cmake(RapidJSON)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Sql)
BuildRequires:  cmake(Qt6Widgets)
%if %{with qpa_qplatformnativeinterface}
BuildRequires:  cmake(Qt6XcbQpaPrivate)
%endif
%if %{with tests}
BuildRequires:  cmake(Qt6Test)
BuildRequires:  cmake(GTest)
BuildRequires:  pkgconfig(gmock)
%endif

Requires:       gstreamer1-plugins-good
Requires:       hicolor-icon-theme

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

%if %{with tests}
# Disable tests that need graphical environment and thus don't work in mock
sed -i '/add_test_file(.* true)/d' tests/CMakeLists.txt
%endif

%build
%{cmake} -DBUILD_WERROR:BOOL=OFF \
%if !%{with qpa_qplatformnativeinterface}
         -DENABLE_QPA_QPLATFORMNATIVEINTERFACE=OFF \
%endif
%if !%{with streamtagreader}
         -DENABLE_STREAMTAGREADER=OFF \
%endif
%if !%{with gpod}
         -DENABLE_GPOD=OFF \
%endif
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
%license COPYING
%license 3rdparty/discord-rpc/LICENSE
%doc Changelog
%{_bindir}/strawberry
%{_metainfodir}/org.strawberrymusicplayer.strawberry.appdata.xml
%{_datadir}/applications/org.strawberrymusicplayer.strawberry.desktop
%{_datadir}/icons/hicolor/*/apps/strawberry.*
%{_mandir}/man1/strawberry.1.*

%changelog
%autochangelog
