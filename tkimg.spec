Summary:	Image support library for Tk
Name:		tkimg
Version:	1.4
Release:	1
License:	BSD
Group:		System/Libraries
Url:		http://sourceforge.net/projects/tkimg
Source0:	%{name}%{version}.tar.bz2
Patch0:		tkimg-zlib.patch
Patch1:		tkimg-jpg.patch
Patch2:		tkimg-libpng.patch
Patch3:		tkimg-libtiff.patch
Patch4:		tkimg-libpng15.patch
Patch5:		tkimg-libtiff4.patch
# gzgetc is now defined as a macro in zlib, which causes tkimg to ftbfs
# because it wants to define all of its functions internally to map to the 
# tcl/tk bits. The simple fix is to use the abstraction function "gzgetc_"
# which avoids the problem. See: https://bugzilla.redhat.com/show_bug.cgi?id=844462
Patch6:		tkimg-zlib127-gzgetc_fix.patch
BuildRequires:	tcl-tcllib
BuildRequires:	jpeg-devel
BuildRequires:	tcl-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)
Requires:	tcl

%description
This package contains a collection of image format handlers for the Tk
photo image type, and a new image type, pixmaps.
The provided format handlers include bmp, gif, ico, jpeg, pcx, png,
ppm, ps, sgi, sun, tga, tiff, xbm, and xpm.

%files
%doc README
%{_libdir}/*.so
%{tcl_sitearch}/Img1.4
%exclude %{tcl_sitearch}/Img1.4/*.a
%{_mandir}/mann/*.n*

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Requires:	jpeg-devel
Requires:	tcl-devel
Requires:	pkgconfig(libpng)
Requires:	pkgconfig(libtiff-4)
Requires:	pkgconfig(tk)
Requires:	pkgconfig(zlib)

%description devel
These are the header files needed to develop a %{name} application.

%files devel
%doc README
%{_includedir}/*
%{_libdir}/*.sh
%{tcl_sitearch}/Img1.4/*.a

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}%{version}
%patch0 -p1 -b .zlib
rm -rf compat/zlib
%patch1 -p1 -b .jpeg
rm -rf compat/libjpeg
%patch2 -p1 -b .libpng
rm -rf compat/libpng
%patch3 -p1 -b .libtiff
rm -rf compat/libtiff
%patch4 -p1 -b .png15
%patch5 -p1 -b .tiff4
%patch6 -p1 -b .gzgetc_fix

%build
%configure2_5x \
	--with-tcl=%{tcl_sitearch} \
	--with-tk=%{_libdir} \
	--libdir=%{tcl_sitearch} \
	--disable-threads
%make

%install
make INSTALL_ROOT=%{buildroot} install

# Fixing some permissions
find %{buildroot}/%{tcl_sitearch} -name "*.sh" |xargs chmod 644
find %{buildroot}/%{tcl_sitearch} -name "*.tcl" |xargs chmod 644
find %{buildroot}/%{tcl_sitearch} -name "*.a" |xargs chmod 644
find %{buildroot}/%{tcl_sitearch} -name "*.so" |xargs chmod 755

# Make library links
mv %{buildroot}%{tcl_sitearch}/*.sh %{buildroot}%{_libdir}
for tcllibs in %{buildroot}%{tcl_sitearch}/Img1.4/*tcl*.so; do
    btcllibs=`basename $tcllibs`
    ln -s tcl%{tcl_version}/Img1.4/$btcllibs %{buildroot}%{_libdir}/$btcllibs
done

