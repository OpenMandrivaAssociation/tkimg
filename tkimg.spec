%define svnversion 20081115

Name:		tkimg
Version:	1.4
Release:	%mkrel 0.%{svnversion}.2
Summary:	More Image Formats for Tk
Group:		System/Libraries
License:	BSD
URL:		http://sourceforge.net/projects/tkimg
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export -r 173 https://tkimg.svn.sourceforge.net/svnroot/tkimg/trunk tkimg-20081115
#  tar -czvf tkimg-20081115.tar.gz  tkimg-20081115
Source0:	%{name}-%{svnversion}.tar.gz
# A request to allow building with system libraries has been submitted
# https://sourceforge.net/tracker/index.php?func=detail&aid=2292032&group_id=52039&atid=465495
Patch0:		tkimg-20081115-syslibs-zlib.patch
Patch1:		tkimg-20081115-syslibs-png.patch
Patch2:		tkimg-20081115-syslibs-tiff.patch
Patch3:		tkimg-20081115-syslibs-jpg.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroo
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	libtiff-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	zlib-devel
Requires:	tcl

%description
This package contains a collection of image format handlers for the Tk
photo image type, and a new image type, pixmaps.
The provided format handlers include bmp, gif, ico, jpeg, pcx, png,
ppm, ps, sgi, sun, tga, tiff, xbm, and xpm.

%package devel
Summary:	Libraries, includes, etc. used to develop an application with %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	tcl-devel
Requires:	tk-devel
Requires:	libtiff-devel
Requires:	libpng-devel
Requires:	libjpeg-devel
Requires:	zlib-devel

%description devel
This are the header files needed to develop a %{name} application.

%prep
%setup -q -n %{name}-%{svnversion}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure2_5x --with-tcl=%{tcl_sitearch} --with-tk=%{_libdir} --libdir=%{tcl_sitearch} --disable-threads
%make

%install
%{__rm} -fr %{buildroot}
make INSTALL_ROOT=%{buildroot} install

# Fixing some permissions
find %{buildroot}/%{tcl_sitearch} -name "*.sh" |xargs chmod 644
find %{buildroot}/%{tcl_sitearch} -name "*.tcl" |xargs chmod 644
find %{buildroot}/%{tcl_sitearch} -name "*.a" |xargs chmod 644
find %{buildroot}/%{tcl_sitearch} -name "*.so" |xargs chmod 755

# Make library links
%{__mv} %{buildroot}/%{tcl_sitearch}/*.sh %{buildroot}/%{_libdir}
for tcllibs in %{buildroot}/%{tcl_sitearch}/Img1.4/*tcl*.so; do
btcllibs=`basename $tcllibs`
%{__ln_s} tcl%{tcl_version}/Img1.4/$btcllibs %{buildroot}/%{_libdir}/$btcllibs
done

%clean
%{__rm} -fr %{buildroot}

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/*.so
%{tcl_sitearch}/Img1.4
%exclude %{tcl_sitearch}/Img1.4/*.a

%files devel
%defattr(-,root,root,-)
%doc README
%{_includedir}/*
%{_libdir}/*.sh
%{tcl_sitearch}/Img1.4/*.a

