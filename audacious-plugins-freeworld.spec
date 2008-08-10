%define         aud_ver 1.4.0

Name:           audacious-plugins-nonfree
Version:        1.4.5
Release:        1%{?dist}
Summary:        Nonfree plugins for the Audacious media player

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://audacious-media-player.org/
Source0:        http://static.audacious-media-player.org/release/audacious-plugins-%{version}.tgz
Source1:        audacious-mp3.desktop
Source2:        audacious-aac.desktop
Source3:        audacious-wma.desktop
Source4:        audacious-alac.desktop
Patch0:         audacious-plugins-1.3.4-sse-disable.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  audacious-devel >= %{aud_ver}
BuildRequires:  zlib-devel, desktop-file-utils >= 0.9
BuildRequires:  taglib-devel >= 1.4
BuildRequires:  lame-devel, libmms-devel, libmad-devel
BuildRequires:  gettext, libbinio-devel
BuildRequires:  dbus-devel >= 0.60, dbus-glib-devel >= 0.60

%description
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

%package        mp3
Summary:        MP3 playback plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious-plugins >= %{aud_ver}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

Provides:       bmp-mp3 = 0.9.7.1
Obsoletes:      bmp-mp3 <= 0.9.7.1

%description    mp3
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to play MP3 audio files.


%package        aac
Summary:        AAC playback plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious-plugins >= %{aud_ver}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

%description    aac
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to play AAC audio files.


%package        wma
Summary:        WMA playback plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious-plugins >= %{aud_ver}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

%description    wma
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to play WMA audio files.


%package        alac
Summary:        ALAC playback plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious-plugins >= %{aud_ver}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

%description    alac
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")

This is the plugin needed to play ALAC (Apple Lossless Audio Codec)
audio files.


%package        tta
Summary:        TTA playback plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious-plugins >= %{aud_ver}

%description    tta
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")

This is the plugin needed to play TTA audio files.


%package        mms
Summary:        MMS stream plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious-plugins >= %{aud_ver}

%description    mms
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to access MMS streams.


%prep
%setup -q -n audacious-plugins-%{version}

# Disable SSE2/AltiVec
# %patch0 -p1 -b .sse-disable

%build
%configure \
        --disable-rpath \
        --enable-gconf \
        --disable-gnome-vfs \
        --enable-chardet \
        --disable-amidiplug \
        --disable-adplug \
        --disable-esd \
        --disable-lirc \
        --disable-sndfile \
        --disable-modplug \
        --disable-flac \
        --disable-jack \
        --disable-arts \
        --disable-sid \
        --disable-alsa \
        --disable-musepack \
        --disable-timidity \
        --disable-vorbis \
        --disable-xspf \
        --disable-paranormal \
        --disable-sse2 \
        --disable-altivec \
        --disable-dependency-tracking
make V=1 %{?_smp_mflags} -C src/madplug
make V=1 %{?_smp_mflags} -C src/aac
make V=1 %{?_smp_mflags} -C src/wma
make V=1 %{?_smp_mflags} -C src/alac
make V=1 %{?_smp_mflags} -C src/tta
make V=1 %{?_smp_mflags} -C src/mms


%install
rm -rf $RPM_BUILD_ROOT
make -C src/madplug install DESTDIR=$RPM_BUILD_ROOT
make -C src/aac install DESTDIR=$RPM_BUILD_ROOT
make -C src/wma install DESTDIR=$RPM_BUILD_ROOT
make -C src/alac install DESTDIR=$RPM_BUILD_ROOT
make -C src/tta install DESTDIR=$RPM_BUILD_ROOT
make -C src/mms install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
    %{SOURCE1}

desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
    %{SOURCE2}

desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
    %{SOURCE3}

desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
    %{SOURCE4}

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%post mp3
update-desktop-database %{_datadir}/applications

%postun mp3
update-desktop-database %{_datadir}/applications

%post aac
update-desktop-database %{_datadir}/applications

%postun aac
update-desktop-database %{_datadir}/applications

%post wma
update-desktop-database %{_datadir}/applications

%postun wma
update-desktop-database %{_datadir}/applications

%post alac
update-desktop-database %{_datadir}/applications

%postun alac
update-desktop-database %{_datadir}/applications


%files mp3
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/madplug.so
%{_datadir}/applications/livna-audacious-mp3.desktop

%files aac
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/aac.so
%{_datadir}/applications/livna-audacious-aac.desktop

%files wma
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/wma.so
%{_datadir}/applications/livna-audacious-wma.desktop

%files alac
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/alac.so
%{_datadir}/applications/livna-audacious-alac.desktop

%files tta
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/tta.so

%files mms
%defattr(-,root,root,-)
%{_libdir}/audacious/Transport/mms.so

%changelog
* Tue Feb 12 2008 Ralf Ertzinger <ralf@skytale.net> 1.4.5-1
- Update to 1.4.5

* Wed Jan 02 2008 Ralf Ertzinger <ralf@skytale.net> 1.4.4-1
- Update to 1.4.4

* Wed Dec 12 2007 Ralf Ertzinger <ralf@skytale.net> 1.4.2-1
- Update to 1.4.2

* Thu Nov 22 2007 Ralf Ertzinger <ralf@skytale.net> 1.4.1-2
- Update to 1.4.1

* Sat Jun 09 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.5-1.fc8
- Update to 1.3.5
- Disable SSE2 patch (now upsteam)

* Fri Jun 01 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.4-2.fc8
- Disable SSE2/AltiVec

* Sat May 26 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.4-1.fc8
- Update to 1.3.4

* Sun Apr 22 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.3-1.fc7
- Update to 1.3.3
- Introduce aud_ver variable into specfile

* Thu Apr 12 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.2-1.fc7
- Update to 1.3.2

* Wed Apr 04 2007 Ralf Ertzinger <ralf@skytale.net> 1.3.1-3.fc7
- Update to 1.3.1

* Thu Nov 30 2006 Ralf Ertzinger <ralf@skytale.net> 1.2.5-1.fc7
- Update to 1.2.5

* Fri Nov 10 2006 Ralf Ertzinger <ralf@skytale.net> 1.2.2-1.fc7
- Update to 1.2.2

* Tue Nov 7 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.2-7.fc7
- Rebuild without gnome-vfs and Require: the correct audacious version
- Drop "X-Livna" and "Application" category from .desktop file

* Sat Oct 21 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info 1.1.2-5
- require audacious, not audacious-plugins-nonfree

* Wed Oct 18 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.2-4.fc6
- Add obsoletes/provides against bmp-mp3

* Mon Oct 16 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.2-2.fc6
- Fix directory name on %%setup

* Wed Sep 06 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.2-1.fc6
- Update to 1.1.2

* Tue Aug 15 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.1-4.fc6
- Properly add Requires(post/postun)
- Carry over changes from main audacious-1.1.1-4 package

* Sun Aug 01 2006 Ralf Ertzinger <ralf@skytale.net> 1.1.1-3.fc6
- Initial RPM for livna
