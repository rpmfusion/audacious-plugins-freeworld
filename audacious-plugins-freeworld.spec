# TODO:
# - add more mime types to .desktop file for 'ffaudio' plugin
# - add BR sidplay2-devel and find a way to make the built sid.so
#   plugin an alternative to Fedora's sidplay1 based sid.so

%global         aud_plugin_api %(grep '[ ]*#define[ ]*__AUDACIOUS_PLUGIN_API__' %{_includedir}/audacious/plugin.h | sed 's!.*__AUDACIOUS_PLUGIN_API__[ ]*\\([0-9]\\+\\).*!\\1!')

Name:           audacious-plugins-freeworld
Version:        2.4.3
Release:        2%{?dist}
Summary:        Additional plugins for the Audacious media player

Group:          Applications/Multimedia
License:        GPLv3
URL:            http://audacious-media-player.org/
Source0:        http://distfiles.atheme.org/audacious-plugins-%{version}.tgz
Source1:        audacious-mp3.desktop
Source2:        audacious-aac.desktop
Source3:        audacious-ffaudio.desktop
Patch0:         audacious-plugins-2.4-sys-mpg123.patch
Patch1:         audacious-plugins-2.4-ffaudio-metadata.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  audacious-devel >= %{version}
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

# obsolete old freshrpms package
Provides:       audacious-plugins-extras = %{version}-%{release}
Obsoletes:      audacious-plugins-extras < %{version}-%{release}

%description
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This package contains additional plugins for the Audacious media player.


%package        mp3
Summary:        MP3 playback plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious(plugin-api) = %{aud_plugin_api}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

# obsolete old livna package
Provides:       audacious-plugins-nonfree-mp3 = %{version}-%{release}
Obsoletes:      audacious-plugins-nonfree-mp3 < %{version}-%{release}

%description    mp3
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to play MP3 audio files.


%package        aac
Summary:        AAC playback plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious(plugin-api) = %{aud_plugin_api}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

# obsolete old livna package
Provides:       audacious-plugins-nonfree-aac = %{version}-%{release}
Obsoletes:      audacious-plugins-nonfree-aac < %{version}-%{release}

%description    aac
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to play AAC audio files.


%package ffaudio
Summary: FFMpeg/FAAD2 based input plugin for Audacious
Group: Applications/Multimedia
Requires: audacious(plugin-api) = %{aud_plugin_api}

Requires(post):  desktop-file-utils >= 0.9
Requires(postun): desktop-file-utils >= 0.9

# obsolete discontinued plugins
Obsoletes: audacious-plugins-freeworld-alac <= 2.1
Obsoletes: audacious-plugins-freeworld-tta <= 2.1
Obsoletes: audacious-plugins-freeworld-wma <= 2.1

# obsolete old livna packages
Obsoletes: audacious-plugins-nonfree-alac < %{version}-%{release}
Obsoletes: audacious-plugins-nonfree-tta < %{version}-%{release}
Obsoletes: audacious-plugins-nonfree-wma < %{version}-%{release}

%description ffaudio
FFMpeg/FAAD2 based input plugin for Audacious.


%package        mms
Summary:        MMS stream plugin for Audacious
Group:          Applications/Multimedia
Requires:       audacious(plugin-api) = %{aud_plugin_api}

# obsolete old livna package
Provides:       audacious-plugins-nonfree-mms = %{version}-%{release}
Obsoletes:      audacious-plugins-nonfree-mms < %{version}-%{release}

%description    mms
Audacious is a media player that currently uses a skinned
user interface based on Winamp 2.x skins. It is based on ("forked off")
BMP.

This is the plugin needed to access MMS streams.


%prep
%setup -q -n audacious-plugins-%{version}
# We want to use the system mpg123
rm -r src/mpg123/libmpg123
%patch0 -p1
%patch1 -p1
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
rm -rf $RPM_BUILD_ROOT
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

%post ffaudio
update-desktop-database %{_datadir}/applications

%postun ffaudio
update-desktop-database %{_datadir}/applications


%files
%defattr(-,root,root,-)
%doc COPYING

%files mp3
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/madplug.so
%{_datadir}/applications/livna-audacious-mp3.desktop

%files aac
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/aac.so
%{_datadir}/applications/livna-audacious-aac.desktop

%files ffaudio
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/ffaudio.so
%{_datadir}/applications/audacious-ffaudio.desktop

%files mms
%defattr(-,root,root,-)
%{_libdir}/audacious/Transport/mms.so


%changelog
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
