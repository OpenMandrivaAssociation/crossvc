Name:		crossvc
Version:	1.5.2
Release:	%{mkrel 2}
Summary:	Graphical version control (frontend to CVS and SVN)
License:	GPLv2+
Group:		Development/Other
URL:		https://crossvc.com/
Source0:	http://crossvc.com/download/%{name}-%{version}-0-generic-src.tgz
Source1:	lincvs_16.png
Source2:	lincvs_32.png
Source3:	lincvs_48.png
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:	qt3-devel
Suggests:	cvs
Suggests:	subversion
Provides:	lincvs = %{version}-%{release}
Obsoletes:	lincvs < %{version}-%{release}

%description
CrossVC is a graphical version control program. You can manage the
versions of source code files. Access to all versions of a file is
available at any time. You can track the modifications from version to
version. Together with CVS or Subversion CrossVC provides network-wide
access to a repository for all members of a team. The team members can
work on the files concurrently, they can merge their modifications,
can develop on multiple branches and much more. 

%prep
%setup -q -n CrossVC
chmod a+rw ts/*

%build
# Generate Makefile
#%{_prefix}/lib/qt3/bin/qmake -o Makefile lincvs.pro QTDIR=%{_prefix}/lib/qt3
%qmake_qt3 -o Makefile lincvs.pro
%make QTDIR=%{_prefix}/lib/qt3

%install
rm -rf %{buildroot}
%makeinstall_std QTDIR=%{_prefix}/lib/qt3 INSTALL_ROOT=%{buildroot}%{_libdir}/apps/
install -d %{buildroot}%{_bindir}

# Generate a wrapper script
echo \#\!/bin/bash > %{buildroot}%{_bindir}/%{name}
echo exec\ \"%{_libdir}/apps/CrossVC/crossvc.bin\" >> %{buildroot}%{_bindir}/%{name}
chmod 755 %{buildroot}%{_bindir}/%{name}

# Fix permissions
find %{buildroot}%{_libdir}/apps/CrossVC/{Help,Messages}/ -type f -depth -exec chmod 644 {} \;
find %{buildroot}%{_libdir}/apps/CrossVC/Tools/ -type f -depth -exec chmod 755 {} \;

# Make symlink for docs
mkdir -p %{buildroot}%{_datadir}/doc
cd %{buildroot}%{_datadir}/doc
ln -s ../../..%{_libdir}/apps/CrossVC/Help %{name}

# Menu
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Icon=%{name}
StartupNotify=true
Categories=Qt;Development;
Name=CrossVC
Comment=CrossVC is a graphical interface for CVS / Subversion
EOF
  
#icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m644 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE2} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE3} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
 
%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(755,root,root)
%{_bindir}/%{name}
%{_libdir}/apps/CrossVC
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/doc/%{name}

