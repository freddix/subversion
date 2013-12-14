Summary:	Open source version control system
Name:		subversion
Version:	1.7.14
Release:	1
License:	Apache/BSD Style
Group:		Development/Version Control
Source0:	http://www.apache.org/dist/subversion/%{name}-%{version}.tar.bz2
# Source0-md5:	cfff541f079f3b4b30795e08ee7aafa7
URL:		http://subversion.apache.org/
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	expat-devel
BuildRequires:	expat-devel
BuildRequires:	gettext-devel
BuildRequires:	libmagic-devel
BuildRequires:	libsasl2-devel
BuildRequires:	libtool
BuildRequires:	neon-devel
BuildRequires:	perl-devel
BuildRequires:	sqlite3-devel
BuildRequires:	texinfo
BuildRequires:	which
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Subversion is an open source version control system.

%package libs
Summary:	Subversion libraries and modules
Group:		Libraries

%description libs
Subversion libraries and modules.

%package devel
Summary:	Header files and develpment documentation for subversion
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files and develpment documentation for subversion.

%prep
%setup -q

%build
chmod +x ./autogen.sh && ./autogen.sh
%{__libtoolize}
%configure \
	--disable-neon-version-check	\
	--disable-static		\
	--with-editor=vi		\
	--with-neon=%{_prefix}		\
	--with-zlib=%{_libdir}		\
	--without-apxs			\
	--without-berkeley-db		\
	--without-swig
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT \

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	devel -p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES INSTALL LICENSE README
%doc doc/*/*.html
%doc tools/xslt/*
%attr(755,root,root) %{_bindir}/svn*
%exclude %{_bindir}/svnserve
%{_mandir}/man1/*

%files libs -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/%{name}*
%{_libdir}/lib*.la

