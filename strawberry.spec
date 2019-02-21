Name:           strawberry
Version:        0.5.2
Release:        2%{?dist}
Summary:        An audio player and music collection organizer

# Main program: GPLv3
# src/analyzer and src/engine/gstengine and src/engine/xineengine: GPLv2
# 3rdparty/taglib, src/widgets/fancytabwidget and src/widgets/stylehelper: LGPLv2
# 3rdparty/qocoa: MIT
# 3rdparty/singleapplication: MIT
# 3rdparty/utf8-cpp: Boost
# src/core/timeconstants.h and ext/libstrawberry-common/core/logging and ext/libstrawberry-common/core/messagehandler: ASL 2.0
# some icons in qocoa: CC-BY-SA
License:        GPLv2 and GPLv3+ amd LGPLv2 and ASL 2.0 and MIT and Boost and CC-BY-SA
URL:            http://www.strawbs.org/
Source0:        https://github.com/jonaski/strawberry/archive/%{version}/%{name}-%{version}.tar.gz

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

Requires:       gstreamer1-plugins-good
Requires:       hicolor-icon-theme

Provides:       bundled(singleapplication)
Provides:       bundled(singlecoreapplication)
Provides:       bundled(qocoa)
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

# Remove most 3rdparty libraries
# Unbundle taglib next release:
# https://github.com/taglib/taglib/issues/837#issuecomment-428389347
mv 3rdparty/{qocoa,singleapplication,taglib,utf8-cpp}/ .
rm -fr 3rdparty/*
mv {qocoa,singleapplication,taglib,utf8-cpp}/ 3rdparty/

mv 3rdparty/singleapplication/LICENSE 3rdparty/singleapplication/LICENSE-singleapplication
mv 3rdparty/qocoa/LICENSE.txt 3rdparty/qocoa/LICENCE-qcocoa.txt
mv 3rdparty/taglib/COPYING 3rdparty/taglib/COPYING-taglib



%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_WERROR:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  ..
popd

%make_build -C %{_target_platform}


%install
%make_install -C %{_target_platform}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/strawberry.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/strawberry.appdata.xml


%files
%license COPYING 3rdparty/qocoa/LICENCE-qcocoa.txt 3rdparty/taglib/COPYING-taglib 3rdparty/singleapplication/LICENSE-singleapplication
%doc Changelog
%{_bindir}/strawberry
%{_bindir}/strawberry-tagreader
%{_metainfodir}/strawberry.appdata.xml
%{_datadir}/applications/strawberry.desktop
%{_datadir}/icons/hicolor/*/apps/strawberry.*
%{_mandir}/man1/strawberry.1.*
%{_mandir}/man1/strawberry-tagreader.1.*


%changelog
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
