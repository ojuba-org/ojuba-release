%define release_name Thirty Eight
%define ar_release_name الثامنة والثلاثون
%define dist_version 25
%define bug_version 25
%define oj_version 38
%define bug_release 38
%define dist_release 0
%define oj_release 0

Summary(ar):        ملفات نظام أعجوبة
Summary:            Ojuba release files
Name:               ojuba-release
Version:            %{oj_version}
Release:            %{oj_release}
License:            WAQFv2 and GPLv2
Group:              System Environment/Base
URL:                http://ojuba.org
Source0:            ojuba-release-%{oj_version}.tar.bz2

Requires:           ojuba-release-extra = %{dist_version}-%{dist_release}
BuildArch:          noarch


%description -l ar
الملفات الأساسية الخاصة بتعريف نظام أعجوبة.

%description
Ojuba release files such as various /etc/ files that define the release.

%package rawhide
Summary:            Rawhide repo definitions
Requires:           ojuba-repo = %{dist_version}-%{dist_release}
Obsoletes:          fedora-release-rawhide <= %{dist_version}
Provides:           fedora-release-rawhide
Provides:           fedora-release-rawhide(%{dist_version})
BuildArch:          noarch
Conflicts:          fedora-release-rawhide

%description rawhide
This package provides the rawhide repo definitions.

%package extra
Summary:            Extra Ojuba Release
Version:            %{dist_version}
Release:            %{oj_release}
Requires:           ojuba-repos = %{oj_version}-%{oj_release}
Requires:           ojuba-release = %{oj_version}-%{oj_release}
# needed for captive portal support
Requires:           NetworkManager-config-connectivity-fedora
Requires(post):     /usr/bin/glib-compile-schemas
Requires(postun):   /usr/bin/glib-compile-schemas

# Kill off the fedora-release-nonproduct package
Provides:           fedora-release-nonproduct = %{dist_version}
Obsoletes:          fedora-release-nonproduct <= 23-0.3
Provides:           fedora-release-standard = 22-0.8
Obsoletes:          fedora-release-standard < 22-0.8

Provides:           system-release-workstation
Provides:           system-release-workstation(%{dist_version})
Provides:           fedora-release-workstation = %{dist_version}-%{dist_release}
Obsoletes:          fedora-release-workstation <= %{dist_version}

Provides:           system-release-product

Obsoletes:          redhat-release
Provides:           redhat-release
Provides:           system-release
Provides:           system-release(%{version})

Obsoletes:          fedora-release <= %{dist_version}
Provides:           fedora-release = %{dist_version}-%{dist_release}

Conflicts:          fedora-release
Conflicts:          system-release-workstation
Conflicts:          fedora-release-workstation

%description extra
Extra files of Ojuba release.

%package -n ojuba-repos
Summary(ar):        ملفات مستودعات أعجوبة
Summary:            Ojuba repository release files
Group:              System Environment/Base
URL:                http://ojuba.org
Obsoletes:          fedora-repos <= %{dist_version}
Obsoletes:          fedora-repos-anaconda < 22-0.3
Obsoletes:          fedora-repos-rawhide <= %{dist_version}-%{dist_release}
Provides:           fedora-repos = %{dist_version}-%{dist_release}
Provides:           fedora-repos(%{dist_version})


%description -l ar -n ojuba-repos
إضافة مستودعات أعجوبة لأي نظام موافق.

%description -n ojuba-repos
Ojuba and fedora package repository files for yum and dnf along with gpg public keys

%prep
rm -rf %{_topdir}/BUILD/*

%setup -q
tar xjf fedora-repos-*.tar.bz2 -C ./ --strip-components=1
tar xjf fedora-release-*.tar.bz2 -C ./ --strip-components=1

sed -i 's|@@VERSION@@|%{dist_version}|g' Fedora-Legal-README.txt
sed -i 's|@@DIST_NAME@@|%{release_name} (%{oj_version})|g' ojuba-release.repo
#cp %{SOURCE2} %{SOURCE3} %{SOURCE4} ./

#cp ojuba.repo repo-ojuba.repo
sed -i -e 's/enabled=1/enabled=1\nexclude=ojuba-release ojuba-release-notes ojuba-logos/' ojuba-release.repo
sed -i -e 's/enabled=1/enabled=1\nexclude=fedora-release fedora-logos/' *.repo

%build
#Nothing to build.

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "Ojuba OS release %{oj_version} (%{release_name})" > $RPM_BUILD_ROOT/etc/ojuba-release
echo "cpe:/o:ojubaproject:ojuba:%{oj_version}" > $RPM_BUILD_ROOT/etc/system-release-cpe

# Symlink the -release files
ln -s ojuba-release $RPM_BUILD_ROOT/etc/fedora-release
ln -s ojuba-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s ojuba-release $RPM_BUILD_ROOT/etc/system-release

# Create the common os-release file
install -d $RPM_BUILD_ROOT/usr/lib/os.release.d/
cat << EOF >>$RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-ojuba
NAME=Ojuba
VERSION="%{oj_version} (%{release_name})"
ID=ojuba
VERSION_ID=%{oj_version}
PRETTY_NAME="Ojuba %{oj_version} (%{release_name})"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:ojubaproject:ojuba:%{oj_version}"
HOME_URL="http://ojuba.org/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
PRIVACY_POLICY_URL=https://fedoraproject.org/wiki/Legal:PrivacyPolicy
EOF
ln -s ./os-release-ojuba $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-fedora

# extra
cp -p $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-ojuba \
      $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-extra
echo "VARIANT=\"Ojuba Edition\"" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-extra
echo "VARIANT_ID=ojubaextra" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-extra
#sed -i -e "s|(%{release_name})|(Ojuba Extra Edition)|g" $RPM_BUILD_ROOT/usr/lib/os.release.d/os-release-extra

# Create the common /etc/issue
echo "\S" > $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-ojuba
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-ojuba
echo >> $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-ojuba
ln -s ./issue-ojuba $RPM_BUILD_ROOT/usr/lib/os.release.d/issue-fedora

# Create /etc/issue.net
echo "\S" > $RPM_BUILD_ROOT/usr/lib/issue.net
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/usr/lib/issue.net
ln -s ../usr/lib/issue.net $RPM_BUILD_ROOT/etc/issue.net

# Create the symlink for /etc/os-release
# This will be standard until %post when the
# release packages will link the appropriate one into
# /usr/lib/os-release
ln -s ../usr/lib/os-release $RPM_BUILD_ROOT/etc/os-release
ln -s ./os.release.d/os-release-ojuba $RPM_BUILD_ROOT/usr/lib/os-release

# Create the symlink for /etc/issue
# This will be standard until %post when the
# release packages will link the appropriate one into
# /usr/lib/os-release
ln -s ../usr/lib/issue $RPM_BUILD_ROOT/etc/issue
ln -s ./os.release.d/issue-ojuba $RPM_BUILD_ROOT/usr/lib/issue


# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%ojuba                %{oj_version}
%%dist                .oj%{oj_version}
%%oj%{oj_version}                1
%%fedora                %{dist_version}
%%fc%{dist_version}                   1
EOF


# Add presets
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/user-preset/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
mkdir -p $RPM_BUILD_ROOT/usr/lib/os.release.d/presets

# Default system wide
install -m 0644 85-display-manager.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -m 0644 90-default.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/
install -m 0644 99-default-disable.preset $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/

# Fedora Workstation
install -m 0644 80-workstation.preset $RPM_BUILD_ROOT%{_prefix}/lib/os.release.d/presets/

# Override the list of enabled gnome-shell extensions for Workstation
mkdir -p $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/
install -m 0644 org.gnome.shell.gschema.override $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/


# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    arches=$(sed -ne "s/^${key}://p" $RPM_BUILD_DIR/fedora-release-%{dist_version}/archmap) \
        || echo "WARNING: no archmap entry for $key"
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-fedora-%{dist_version}-primary RPM-GPG-KEY-%{dist_version}-fedora
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in *.repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

%clean
rm -rf $RPM_BUILD_ROOT

%posttrans
# Only on installation
if [ $1 = 0 ]; then
    # If no fedora-release-$edition subpackage was installed,
    # make sure to link /etc/os-release to the standard version
    test -e /usr/lib/os-release || \
        ln -sf ./os-release.d/os-release-fedora /usr/lib/os-release
fi

%post extra
# Run every time
# If there is no link to os-release yet from some other
# release package, create it
test -e /usr/lib/os-release || \
    ln -sf ./os.release.d/os-release-extra /usr/lib/os-release

# If os-release isn't a link or it exists but it points to a
# non-productized version, replace it with this one
if [ \! -h /usr/lib/os-release -o "x$(readlink /usr/lib/os-release)" = "xos.release.d/os-release-ojuba" ]; then
    ln -sf ./os.release.d/os-release-extra /usr/lib/os-release || :
fi

if [ $1 -eq 1 ] ; then
    # Initial installation

    # fix up after %%systemd_post in packages
    # possibly installed before our preset file was added
    units=$(sed -n 's/^disable//p' \
        < %{_prefix}/lib/systemd/system-preset/80-workstation.preset)
    /usr/bin/systemctl preset $units >/dev/null 2>&1 || :
fi

%postun extra
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

    # If os-release is now a broken symlink or missing replace it
    # with a symlink to basic version
    test -e /usr/lib/os-release || \
        ln -sf ./os.release.d/os-release-ojuba /usr/lib/os-release || :
fi

%posttrans extra
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files rawhide
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%files
%defattr(-,root,root,-)
#%doc GPL Fedora-Legal-README.txt waqf2-ar.pdf
%doc Fedora-Legal-README.txt waqf2-ar.pdf

%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir /usr/lib/systemd/user-preset/
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset

%files extra
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-extra
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override
%ghost %{_prefix}/lib/systemd/system-preset/80-workstation.preset
%config %attr(0644,root,root) /usr/lib/os.release.d/presets/80-workstation.preset

%dir /usr/lib/os.release.d
%dir /usr/lib/os.release.d/presets
%config %attr(0644,root,root) /usr/lib/os.release.d/os-release-ojuba
%config(noreplace) /usr/lib/os.release.d/os-release-fedora
%ghost /usr/lib/os-release
/etc/os-release
%config %attr(0644,root,root) /etc/ojuba-release
%config(noreplace) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config %attr(0644,root,root) /usr/lib/os.release.d/issue-ojuba
%config(noreplace) /usr/lib/os.release.d/issue-fedora
%ghost /usr/lib/issue
%config(noreplace) /etc/issue
%config %attr(0644,root,root) /usr/lib/issue.net
%config(noreplace) /etc/issue.net

%files -n ojuba-repos
%defattr(-,root,root,-)
%doc waqf2-ar.pdf
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/ojuba-release.repo
%config(noreplace) /etc/yum.repos.d/fedora*.repo
#%config(noreplace) /etc/yum.repos.d/fedora-updates*.repo
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%changelog
* Tue Nov 15 2016 Ehab El-Gedawy <ehabsas@gmail.com> - 38-0
- setup for Ojuba 38, fedora 25 base 

* Mon Dec 14 2015 Ehab El-Gedawy <ehabsas@gmail.com> - 37-1
- setup for Ojuba 37 

* Mon Jul 20 2015 Mosaab Alzoubi <moceap@hotmail.com> - 36-2
- Rename ojuba.repo to ojub-release.repo

* Mon Apr 06 2015 Ehab El-Gedawy <ehabsas@gmail.com> - 36-1
- Retrieve extra package.

* Mon Apr 06 2015 Ehab El-Gedawy <ehabsas@gmail.com> - 36-1
- Ojuba 36 release.

* Fri Feb 28 2014 Mosaab Alzoubi <moceap@hotmail.com> - 35-5
- General Fixes.

* Fri Feb 21 2014 Mosaab Alzoubi <moceap@hotmail.com> - 35-4
- General Fixes.

* Wed Feb 12 2014 Mosaab Alzoubi <moceap@hotmail.com> - 35-1
- Ojuba release 35 built upon Fedora release 20-1
- Tricks From past Ojuba release spec and from Korora one,
- Also from Kenzy one.

* Wed Nov 27 2013 Dennis Gilmore <dennis@ausil.us> - 20-1
- enabled metadata caching for fedora
- disable updates-testing
- obsolete fedora-release-rawhide < the last shipped rawhide build

* Wed Nov 13 2013 Dennis Gilmore <dennis@ausil.us> - 20-0.8
- patch from Will Woods to use a archmap file for linking gpg keys
- add f21 keys
- add fields to /etc/os-release for rhbz#951119
- set skip_if_unavailable=False for rhbz#985354

* Tue Sep 03 2013 Dennis Gilmore <dennis@ausil.us> - 20-0.7
- set Fedora 20 release name

* Fri Aug 30 2013 Dennis Gilmore <dennis@ausil.us> - 20-0.6
- update the fedora 20 secondary arch key it had been created incorrectly

* Tue Aug 20 2013 Dennis Gilmore <dennis@ausil.us> - 20-0.5
- disable rawhide
- enable fedora, updates and updates-testing
- disable 7d metadata cache for fedora
- Obsolete older fedora-release-rawhide

* Wed Jul 31 2013 Dennis Gilmore <dennis@ausil.us> - 20-0.4
- link armhfp gpg key to primary since its now living there

* Mon Jul 08 2013 Dennis Gilmore <dennis@ausil.us> - 20-0.3
- fix up typo

* Wed Jun 19 2013 Dennis Gilmore <dennis@ausil.us> - 20-0.2
- add f20 keys
- switch mirrorlist= to metalink= bz#948788
- add bugzilla fields to os-release for brokeness in abrt bz#961477
- add releasever into gpgkey paths
- use consistent macros for dist_release value

* Tue Mar 12 2013 Dennis Gilmore <dennis@ausil.us> - 20-0.1
- setup for f20
- 64 bit arm arch is aarch64 not arm64
- drop sparc arches

* Wed Aug 08 2012 Dennis Gilmore <dennis@ausil.us> - 19-0.1
- setup for f19

* Mon Aug 06 2012 Dennis Gilmore <dennis@ausil.us> - 18-0.6
- sync up from dist-git
- replace the fedora 18 gpg keys
- bring the Fedora-Legal-README file into upstream

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 29 2012 Tom Callaway <spot@fedoraproject.org> - 18-0.4
- add Fedora-Legal-README.txt

* Mon Feb 27 2012 Dennis Gilmore <dennis@ausil.us> - 18-0.3
 add CPE info to os-release file bz#790509

* Wed Feb 08 2012 Dennis Gilmore <dennis@ausil.us> - 18-0.2
- add /etc/os-release file for bz#733117

* Tue Jan 10 2012 Dennis Gilmore <dennis@ausil.us> - 18-0.1
- setup for fedora 18
- add the fedora 18 gpg keys

* Tue Jan 10 2012 Dennis Gilmore <dennis@ausil.us> - 17-0.4
- install the fedora 17 gpg keys

* Wed Dec 28 2011 Dennis Gilmore <dennis@ausil.us> - 17-0.3
- symlink the secondary arch key for the armhfp and arm64 basearch

* Tue Jul 26 2011 Dennis Gilmore <dennis@ausil.us> - 17-0.2
- set dist_version to 17

* Tue Jul 26 2011 Dennis Gilmore <dennis@ausil.us> - 17-0.1
- build for Fedora 17

* Thu Feb 10 2011 Dennis Gilmore <dennis@ausil.us> - 16-0.1
- Build for Fedora 16

* Wed Feb 09 2011 Dennis Gilmore <dennis@ausil.us> - 15-0.5
- Add the Fedora 15 key

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 29 2010 Jesse Keating <jkeating@redhat.com> - 15-0.1
- Build for Fedora 15

* Fri Jul 23 2010 Jesse Keating <jkeating@redhat.com> - 14-0.6
- Add the Fedora 14 key

* Thu May 06 2010 Dennis Gilmore <dennis@ausil.us> - 14-0.5
- link sparc key
- drop ppc ppc64 from primary arch list

* Tue Mar 02 2010 Jesse Keating <jkeating@redhat.com> - 14-0.4
- When in rawhide, require the -rawhide subpackage.

* Thu Feb 18 2010 Jesse Keating <jkeating@redhat.com> - 14-0.3
- Fix the key path in the updates-testing repo

* Thu Feb 18 2010 Jesse Keating <jkeating@redhat.com> - 14-0.2
- Fix the -rawhide requires
- Fix the -rawhide files
- Switch to bz2 source

* Mon Feb 15 2010 Jesse Keating <jkeating@redhat.com> - 14-0.1
- Update for Fedora 14
- Move the rawhide repo file to it's own subpackage

* Tue Jan 19 2010 Jesse Keating <jkeating@redhat.com> - 13-0.3
- Put the right key in the key file this time

* Tue Jan 19 2010 Jesse Keating <jkeating@redhat.com> - 13-0.2
- Add the key for Fedora 13

* Thu Aug 27 2009 Jesse Keating <jkeating@redhat.com> - 13-0.1
- Bump for Fedora 13's rawhide.
- Put the version at 13 from the start.

* Fri Aug 07 2009 Jesse Keating <jkeating@redhat.com> - 11.91-3
- Bump for new tarball

* Fri Aug 07 2009 Jesse Keating <jkeating@redhat.com> - 11.91-2
- Fix the gpg key file name

* Fri Aug 07 2009 Jesse Keating <jkeating@redhat.com> - 11.91-1
- Update for F12-Alpha
- Replace F11 key with F12
- Drop old keys and inactive secondary arch keys
- Fix metalink urls to be https
- Drop the compose stuff

* Mon Mar 30 2009 Jesse Keating <jkeating@redhat.com> - 11.90-1
- Build for F12 collection

* Mon Mar 09 2009 Jesse Keating <jkeating@redhat.com> - 10.92-1
- Bump for F11 Beta
- Add the (giant) F11 Test key

* Thu Mar 05 2009 Jesse Keating <jkeating@redhat.com> - 10.91-4
- Drop req on fedora-release-notes (#483018)

* Tue Mar 03 2009 Jesse Keating <jkeating@redhat.com> - 10.91-3
- Move metalink urls to mirrorlist for helping anaconda

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Jesse Keating <jkeating@redhat.com> - 10.91-1
- Use the correct CPE name (#481287)

* Wed Jan 21 2009 Jesse Keating <jkeating@redhat.com> - 10.91-1
- Update for Fedora 11 Alpha
- Use metalink urls to get mirror information

* Wed Oct 01 2008 Jesse Keating <jkeating@redhat.com> - 10.90-1
- Initial build for Fedora 11.

* Mon Sep 15 2008 Jesse Keating <jkeating@redhat.com> - 9.91-1
- Update for Fedora 10 beta
- Add the new keys for F10
- Remove F8/9 keys
- Update compose configs
- Clarify rawhide repo definition

* Wed Jun 11 2008 Jesse Keating <jkeating@redhat.com> - 9.90-2
- Package up the ia64 key as the first secondary arch
- Mark config files correctly
- Stop using download.fedora.redhat.com and use download.fedoraproject.org instead

* Mon Mar 31 2008 Jesse Keating <jkeating@redhat.com> - 9.90-1
- Update for Fedora 10 rawhide.

* Thu Mar 13 2008 Jesse Keating <jkeating@redhat.com> - 8.92-1
- Update for 9 Beta
- Update the compose files for 9 Beta
- Add system-release-cpe (from Mark Cox)
- Add terminal to issue (#436387)
- Rename development to rawhide where appropriate.

* Wed Oct 10 2007 Jesse Keating <jkeating@redhat.com> - 8.90-3
- Bump for cvs oopsie

* Wed Oct 10 2007 Jesse Keating <jkeating@redhat.com> - 8.90-2
- Add the gpg info to the devel repo

* Wed Oct 03 2007 Jesse Keating <jkeating@redhat.com> - 8.90-1
- First build for Fedora 9 development.

* Fri Sep 28 2007 Jesse Keating <jkeating@redhat.com> - 7.92-1
- Bump for F8 Test2.
- Package up the compose kickstart files

* Fri Sep 14 2007 Jesse Keating <jkeating@redhat.com> - 7.91-2
- Use failovermethod=priority in yum configs (243698)

* Thu Aug 30 2007 Jesse Keating <jkeating@redhat.com> - 7.91-1
- Provide system-release, useful for spinoffs.
- Also link system-release to fedora-release for file level checks
- Bump for F8 Test2
- Fix license tag

* Fri Jul 27 2007 Jesse Keating <jkeating@redhat.com> - 7.90-1
- Bump for F8 Test1

* Thu Jun 28 2007 Jesse Keating <jkeating@redhat.com> - 7.89-3
- Cleanups from review
- Don't (noreplace) the dist tag macro file

* Tue Jun 19 2007 Jesse Keating <jkeating@redhat.com> - 7.89-2
- Define the dist macros in this package since we define everyting else here

* Wed May 30 2007 Jesse Keating <jkeating@redhat.com> - 7.89-1
- And we're back to rawhide.  Re-enable devel repos

* Thu May 24 2007 Jesse Keating <jkeating@redhat.com> - 7-3
- We have a name!
- Require the newer release notes

* Mon May 21 2007 Jesse Keating <jkeating@redhat.com> - 7-2
- Use Everything in the non-mirror URL to the release tree

* Mon May 21 2007 Jesse Keating <jkeating@redhat.com> - 7-1
- First build for Fedora 7
- Remove Extras repos (YAY!)
- Remove references to "core" in repo files.
- Adjust repo files for new mirror structure
- Remove Legacy repo

* Fri Apr 20 2007 Jesse Keating <jkeating@redhat.com> - 6.93-1
- Bump for Test 4

* Mon Mar 19 2007 Jesse Keating <jkeating@redhat.com> - 6.92-1
- Bump for Test 3
- No more eula in fedora-release, moved to firstboot

* Fri Feb 23 2007 Jesse Keating <jkeating@redhat.com> - 6.91-1
- Bump for Test 2

* Tue Feb 13 2007 Jesse Keating <jkeating@redhat.com> - 6.90-4
- Specfile cleanups

* Mon Feb 05 2007 Jesse Keating <jkeating@redhat.com> - 6.90-3
- Drop the legacy repo file.

* Fri Jan 26 2007 Jesse Keating <jkeating@redhat.com> - 6.90-2
- Core?  What Core?

* Wed Jan 24 2007 Jeremy Katz <katzj@redhat.com> - 6.90-1
- Bump to 6.90.  Keep working with older release notes

* Mon Oct 16 2006 Jesse Keating <jkeating@redhat.com> - 6-89
- Keep version 6, bump release.  Saves from having to rebuild
  release notes all the time

* Sun Oct 15 2006 Jesse Keating <jkeating@redhat.com> - 6.89-1
- Rebuild for rawhide

* Thu Oct 12 2006 Jesse Keating <jkeating@redhat.com> - 6-3
- version has to stay the same, safe to use.

* Thu Oct  5 2006 Jesse Keating <jkeating@redhat.com> - 6-2
- replace old mirror files with new mirrorlist cgi system

* Thu Oct  5 2006 Jesse Keating <jkeating@redhat.com> - 6-1
- Rebuild for Fedora Core 6 release

* Tue Sep  5 2006 Jesse Keating <jkeating@redhat.com> - 5.92-1
- Bump for FC6 Test3

* Thu Jul 27 2006 Jesse Keating <jkeating@redhat.com> - 5.91.1-1
- Convert deprecated gtk calls. (#200242)
- Fix some of the versioning

* Sun Jul 23 2006 Jesse Keating <jkeating@redhat.com> - 5.91-4
- Bump for FC6 Test2
- Remove release-notes content, now standalone package
- Don't replace issue and issue.net if the end user has modified it
- Require fedora-release-notes
- Cleanups

* Mon Jun 19 2006 Jesse Keating <jkeating@redhat.com> - 5.90-3
- Cleanups

* Thu Jun 15 2006 Jesse Keating <jkeating@redhat.com> - 5.90-1
- Update for 5.90

* Wed May 24 2006 Jesse Keating <jkeating@redhat.com> - 5.89-rawhide.2
- Update to get new devel repo file
- merge minor changes from external cvs .spec file

* Wed Apr 19 2006 Jesse Keating <jkeating@redhat.com> - 5.89-rawhide.1
- Look, a changelog!
- Removed duplicate html/css content from doc dir.
- Add lynx as a buildreq
