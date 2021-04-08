Name:           strawberry
Version:        0.9.2
Release:        1%{?dist}
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
* Thu Apr  8 18:18:11 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.9.2-1
- Update to 0.9.2
- Close: rhbz#1938490

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 14:43:43 CET 2021 Adrian Reber <adrian@lisas.de> - 0.8.5-2
- Rebuilt for protobuf 3.14

* Fri Jan  8 17:58:40 CET 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.5-1
- Update to 0.8.5
- Close: rhbz#1909456

* Sat Dec 05 14:57:04 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.4-1
- Update to 0.8.4
- Close: rhbz#1897885

* Mon Nov 09 08:13:59 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.3-1
- Update to 0.8.3 (#1891280, #1887027)

* Thu Oct 01 2020 Jeff Law <law@redhat.com> - 0.7.2-4
- Force -fPIC into build flags.  Re-enable LTO

* Wed Sep 30 15:15:27 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.2-3
- Disable LTO
- Fix #1878315

* Thu Sep 24 2020 Adrian Reber <adrian@lisas.de> - 0.7.2-2
- Rebuilt for protobuf 3.13

* Mon Aug 24 20:19:01 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.7.2-1
- Update to 0.7.2 (#1869008)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.13-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 05:56:51 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.13-1
- Update to 0.6.13 (#1856599)

* Sun Jun 21 2020 Adrian Reber <adrian@lisas.de> - 0.6.12-2
- Rebuilt for protobuf 3.12

* Tue Jun 16 22:48:55 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.12-1
- Update to 0.6.12

* Tue Mar 31 2020 Adrian Reber <adrian@lisas.de> - 0.6.8-3
- Rebuilt for libcdio-2.1.0

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 11 19:30:20 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.8-1
- Release 0.6.8 (#1788069)

* Thu Dec 19 2019 Orion Poplawski <orion@nwra.com> - 0.6.7-2
- Rebuild for protobuf 3.11

* Wed Dec 04 16:39:27 CET 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.7-1
- Release 0.6.7

* Thu Oct 10 20:22:06 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.5-1
- Release 0.6.5

* Wed Sep 25 19:58:52 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.4-1
- Release 0.6.4

* Thu Aug 08 23:06:50 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.6.3-1
- Release 0.6.3

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 05 21:55:17 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.5-1
- Release 0.5.5

* Sun May 05 20:10:21 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.4-1
- Release 0.5.4

* Fri May 03 23:14:14 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.3-2
- Rebuilt for new gstreamer

* Tue Apr 02 01:34:00 CET 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.3-1
- Release 0.5.3

* Thu Feb 21 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.2-2
- Remove unneeded BR

* Mon Feb 18 2019 Robert-André Mauchin <zebob.m@gmail.com> - 0.5.2-1
- Update to 0.5.2

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0.4.2-1
- Release 0.4.2

* Wed Nov 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.1-3
- Rebuild for protobuf 3.6

* Fri Nov 02 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0.4.1-2
- Remove extraneous Requires to qtiocompressor

* Thu Nov 01 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0.4.1-1
- Release 0.4.1

* Sat Oct 20 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0.3.3-1
- Initial package
