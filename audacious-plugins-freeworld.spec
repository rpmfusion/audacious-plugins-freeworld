%global aud_plugin_api %(grep '[ ]*#define[ ]*_AUD_PLUGIN_VERSION[ ]\\+' %{_includedir}/audacious/plugin.h 2>/dev/null | sed 's!.*_AUD_PLUGIN_VERSION[ ]*\\([0-9]\\+\\).*!\\1!')
%if 0%{aud_plugin_api} > 0
%global aud_plugin_dep Requires: audacious(plugin-api)%{?_isa} = %{aud_plugin_api}
%endif

Name:           audacious-plugins-freeworld
Version:        3.3.2
Release:        1%{?dist}
Summary:        Additional plugins for the Audacious media player

Group:          Applications/Multimedia
License:        GPLv3
URL:            http://audacious-media-player.org/
Source0:        http://distfiles.audacious-media-player.org/audacious-plugins-%{version}.tar.bz2
Source1:        audacious-mp3.desktop
Source2:        audacious-aac.desktop
Source3:        audacious-ffaudio.desktop

BuildRequires:  audacious-devel >= 3.3
BuildRequires:  zlib-devel, libxml2-devel, desktop-file-utils >= 0.9
BuildRequires:  taglib-devel >= 1.4
BuildRequires:  libmms-devel, libmpg123-devel
BuildRequires:  gettext, libbinio-devel
BuildRequires:  dbus-devel >= 0.60, dbus-glib-devel >= 0.60
# ffaudio plugin
BuildRequires:  faad2-devel ffmpeg-devel

# require all the plugins
Requires:       %{name}-mp3 = %{version}-%{release}
Requires:       %{name}-aac = %{version}-%{release}
Requires:       %{name}-mms = %{version}-%{release}
Requires:       %{name}-ffaudio = %{version}-%{release}

%description
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This package contains additional plugins for the Audacious media player.


%package        mp3
Summary:        MP3 playback plugin for Audacious
Group:          Applications/Multimedia
%{?aud_plugin_dep}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

%description    mp3
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to play MP3 audio files.


%package        aac
Summary:        AAC playback plugin for Audacious
Group:          Applications/Multimedia
%{?aud_plugin_dep}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

%description    aac
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to play AAC audio files.


%package        ffaudio
Summary:        FFMpeg/FAAD2 based input plugin for Audacious
Group:          Applications/Multimedia
%{?aud_plugin_dep}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

# obsolete discontinued plugins
Obsoletes:      audacious-plugins-freeworld-alac <= 2.1
Obsoletes:      audacious-plugins-freeworld-tta <= 2.1
Obsoletes:      audacious-plugins-freeworld-wma <= 2.1

%description ffaudio
FFMpeg/FAAD2 based input plugin for Audacious.


%package        mms
Summary:        MMS stream plugin for Audacious
Group:          Applications/Multimedia
%{?aud_plugin_dep}

%description    mms
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to access MMS streams.


%prep
%setup -q -n audacious-plugins-%{version}
sed -i '\,^.SILENT:,d' buildsys.mk.in


%build
%configure \
        --disable-rpath \
        --enable-chardet \
        --disable-sse2 \
        --disable-altivec \
        --disable-dependency-tracking
make V=1 %{?_smp_mflags} -C src/mpg123
make V=1 %{?_smp_mflags} -C src/aac
make V=1 %{?_smp_mflags} -C src/ffaudio
make V=1 %{?_smp_mflags} -C src/mms


%install
make -C src/mpg123 install DESTDIR=$RPM_BUILD_ROOT
make -C src/aac install DESTDIR=$RPM_BUILD_ROOT
make -C src/ffaudio install DESTDIR=$RPM_BUILD_ROOT
make -C src/mms install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
    %{SOURCE1}

desktop-file-install --vendor livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
    %{SOURCE2}

desktop-file-install --vendor "" \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
    %{SOURCE3}

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%post mp3
update-desktop-database %{_datadir}/applications

%postun mp3
update-desktop-database %{_datadir}/applications

%post aac
update-desktop-database %{_datadir}/applications

%postun aac
update-desktop-database %{_datadir}/applications

%post ffaudio
update-desktop-database %{_datadir}/applications

%postun ffaudio
update-desktop-database %{_datadir}/applications


%files

%files mp3
%doc COPYING
%{_libdir}/audacious/Input/madplug.so
%{_datadir}/applications/livna-audacious-mp3.desktop

%files aac
%doc COPYING
%{_libdir}/audacious/Input/aac.so
%{_datadir}/applications/livna-audacious-aac.desktop

%files ffaudio
%doc COPYING
%{_libdir}/audacious/Input/ffaudio.so
%{_datadir}/applications/audacious-ffaudio.desktop

%files mms
%doc COPYING
%{_libdir}/audacious/Transport/mms.so


%changelog
* Sun Sep 23 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 3.3.2-1
- Upgrade to 3.3.2

* Tue Jul 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.3-0.2.alpha1
- Rebuilt for mpeg123

* Sun Jun 24 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 3.3-0.1.alpha1
- Upgrade to 3.3-alpha1

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.2-3
- Rebuilt for x264/FFmpeg

* Sun Jan 29 2012 Hans de Goede <j.w.r.degoede@gmail.com> 3.2-2
- Silence false error printf's when reaching EOF on mp3 files

* Sun Jan 29 2012 Hans de Goede <j.w.r.degoede@gmail.com> 3.2-1
- Upgrade to 3.2

* Thu Nov  3 2011 Hans de Goede <j.w.r.degoede@gmail.com> 3.0.4-1
- Upgrade to 3.0.4

* Sun Sep  4 2011 Hans de Goede <j.w.r.degoede@gmail.com> 3.0.2-2
- Rebuild for ffmpeg-0.8

* Sat Aug 27 2011 Hans de Goede <j.w.r.degoede@gmail.com> 3.0.2-1
- Update to 3.0.2

* Wed Jun 22 2011 Hans de Goede <j.w.r.degoede@gmail.com> 2.5.2-1
- Update to 2.5.2
- Drop Provides + Obsoletes for upgrade path from livna / freshrpms

* Fri Apr 29 2011 Hans de Goede <j.w.r.degoede@gmail.com> 2.4.5-1
- Update to 2.4.5

* Mon Apr 11 2011 Hans de Goede <j.w.r.degoede@gmail.com> 2.4.4-1
- Update to 2.4.4

* Fri Jan 28 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4.3-2
- Change audacious version require to use the new Fedora packages
  audacious(plugin-api) provides, for proper detection of plugin ABI changes

* Thu Jan 20 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4.3-1
- Update to 2.4.3

* Sun Aug 29 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4.0-1
- Update to 2.4.0

* Tue Aug 24 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.4-0.1.rc2
- Update to 2.4-rc2

* Fri Jan 29 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2-3
- Fix another hang in the madplug plugin (rf1061)

* Mon Jan 25 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2-2
- Don't hang when trying to identify unknown files as mp3 files (rf1031)

* Sat Dec 19 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 2.2-1
- Update to 2.2

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.5.1-2
- rebuild for new F11 features

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.5.1-1
- Update to 1.5.1

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.4.5-2
- obsolete nonfree -plugins from livna 
- add metapackage that requires all the plugins and obsoletes the 
 -extras package from freshrpms

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
