Summary:	Automatic mesh generation tool
Name:		netgen-mesher
Version:	5.3.1
Release:	0.1
License:	LGPLv2
Group:		Libraries
URL:		http://sourceforge.net/projects/netgen-mesher/
Source0:	http://downloads.sourceforge.net/netgen-mesher/netgen-%{version}.tar.gz
# Source0-md5:	afd5a9b0b1296c242a9c554f06af6510
Source1:	%{name}.png
Source2:	%{name}.desktop
# Fix various configure.ac and Makefiles issues:
# - Fix configure.ac to correctly detect dependencies
# - Fix makefile for togl
# - Rename shared libaries, the original names are often way too generic
# - Add missing libraries to LIBADD
# - Fix nglib invalid soname
Patch0:		netgen-5.3.1_build.patch
# Some fixes to the code (taken from salome netgen plugin)
Patch1:		netgen-5.3.0_fixes.patch
# Fix build against recent metis
Patch2:		netgen-5.3.0_metis.patch
# Set a default NETGENDIR appropriate for the fedora packaging
Patch3:		netgen-5.3.0_netgendir.patch
# Remove some MSC_VER ifdefs (why are they there?)
Patch4:		netgen-5.3.0_msc-ver.patch
# Make some includes relative (needed for when headers are in -private subpackage)
Patch5:		netgen-5.3.0_relative-includes.patch
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	OCE-devel
BuildRequires:	Togl-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libtool
BuildRequires:	metis-devel
BuildRequires:	mpich-devel
BuildRequires:	tk-devel
BuildRequires:	xorg-lib-libXmu-devel
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description
NETGEN is an automatic 3d tetrahedral mesh generator. It accepts input
from constructive solid geometry (CSG) or boundary representation
(BRep) from STL file format. The connection to a geometry kernel
allows the handling of IGES and STEP files. NETGEN contains modules
for mesh optimization and hierarchical mesh refinement.

%package        common
Summary:	Common files for netgen
Requires:	hicolor-icon-theme
Requires:	tix
BuildArch:	noarch

%description    common
Common files for netgen.

%package        libs
Summary:	Netgen libraries

%description    libs
Netgen libraries.

%package        devel
Summary:	Development files for netgen
Requires:	%{name} = %{version}-%{release}

%description    devel
Development files for netgen.

%package        devel-private
Summary:	Private headers of netgen
Requires:	%{name}-devel = %{version}-%{release}

%description    devel-private
Private headers of netgen, needed to build certain netgen based
software packages.



###############################################################################

%package        openmpi
Summary:	Netgen compiled against openmpi
# Require explicitly for dir ownership and to guarantee the pickup of the right runtime
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{name}-openmpi-libs = %{version}-%{release}
Requires:	openmpi

%description    openmpi
Netgen compiled against openmpi.

%package        openmpi-libs
Summary:	Netgen libraries compiled against openmpi

%description    openmpi-libs
Netgen libraries compiled against openmpi.

%package        openmpi-devel
Summary:	Development files for Netgen compiled against openmpi
# Require explicitly for dir ownership
Requires:	%{name}-openmpi = %{version}-%{release}
Requires:	openmpi-devel

%description    openmpi-devel
Development files for Netgen compiled against openmpi.



###############################################################################

%package        mpich
Summary:	Netgen compiled against mpich
# Require explicitly for dir ownership and to guarantee the pickup of the right runtime
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{name}-mpich-libs = %{version}-%{release}
Requires:	mpich

%description    mpich
Netgen compiled against mpich.

%package        mpich-libs
Summary:	Netgen libraries compiled against mpich

%description    mpich-libs
Netgen libraries compiled against mpich.

%package        mpich-devel
Summary:	Development files for Netgen compiled against mpich
# Require explicitly for dir ownership
Requires:	%{name}-mpich = %{version}-%{release}
Requires:	mpich-devel

%description    mpich-devel
Development files for Netgen compiled against mpich.


###############################################################################

%prep
%setup -q -n netgen-%{version}

# Convert line endings
find . -type f -exec dos2unix {} \;

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1


%build
autoreconf -ifv
### serial version ###
mkdir serial
cd serial
%configure --enable-occ --with-togl=%{tcl_sitearch}/Togl1.7 --enable-jpeglib \
		   --includedir=%{_includedir}/%{name} --datadir=%{_datadir}/%{name}
#		  --enable-ffmpeg
# Fix unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%{__make} %{?_smp_mflags}
cd ..

### openmpi version ###
%{_openmpi_load}
export CXX=mpicxx
mkdir openmpi
cd openmpi
%configure --enable-occ --with-togl=%{tcl_sitearch}/Togl1.7 --enable-jpeglib --enable-parallel \
		   --bindir=$MPI_BIN --libdir=$MPI_LIB --includedir=$MPI_INCLUDE/%{name} --datadir=%{_datadir}/%{name}
#		  --enable-ffmpeg
# Fix unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%{__make} %{?_smp_mflags}
cd ..
%{_openmpi_unload}

### mpich version ###
%{_mpich_load}
export CXX=mpicxx
mkdir mpich
cd mpich
%configure --enable-occ --with-togl=%{tcl_sitearch}/Togl1.7 --enable-jpeglib --enable-parallel \
		   --bindir=$MPI_BIN --libdir=$MPI_LIB --includedir=$MPI_INCLUDE/%{name} --datadir=%{_datadir}/%{name}
#		  --enable-ffmpeg
# Fix unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%{__make} %{?_smp_mflags}
cd ..
%{_mpich_unload}

%install
%define writepkgconfig() \
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/$MPI_LIB/pkgconfig; \
cat > $RPM_BUILD_ROOT/$MPI_LIB/pkgconfig/%{name}.pc << EOF\
prefix=%{_prefix}\
exec_prefix=${prefix}\
libdir=$MPI_LIB\
includedir=$MPI_INCLUDE/%{name}\
\
Name: %{name}\
Description:  %{summary}\
Version: %{version}\
Libs: -L\\\${libdir} -lnglib\
Libs.private: -lngcgs -lnggeom2d -lngmesh -lngocc -lngstl\
Cflags: -I\\\${includedir}\
EOF\
%{nil}

### openmpi version ###
%{_openmpi_load}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT -C openmpi
%writepkgconfig
# Avoid conflicts with netgen, remove data files (are correctly installed below)
mv $RPM_BUILD_ROOT/$MPI_BIN/netgen $RPM_BUILD_ROOT/$MPI_BIN/%{name}
rm -f $RPM_BUILD_ROOT/$MPI_BIN/*.tcl rm -f $RPM_BUILD_ROOT/$MPI_BIN/*.ocf
%{_openmpi_unload}

### mpich version ###
%{_mpich_load}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT -C mpich
%writepkgconfig
# Avoid conflicts with netgen, remove data files (are correctly installed below)
mv $RPM_BUILD_ROOT/$MPI_BIN/netgen $RPM_BUILD_ROOT/$MPI_BIN/%{name}
rm -f $RPM_BUILD_ROOT/$MPI_BIN/*.tcl rm -f $RPM_BUILD_ROOT/$MPI_BIN/*.ocf
%{_mpich_unload}

### serial version ###
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT -C serial
export MPI_LIB=%{_libdir}
export MPI_INCLUDE=%{_includedir}
%writepkgconfig
# Avoid conflicts with netgen, move data files to correct place
mv $RPM_BUILD_ROOT/%{_bindir}/netgen $RPM_BUILD_ROOT/%{_bindir}/%{name}
mv $RPM_BUILD_ROOT%{_bindir}/*.tcl $RPM_BUILD_ROOT%{_bindir}/*.ocf $RPM_BUILD_ROOT%{_datadir}/%{name}
chmod -x $RPM_BUILD_ROOT%{_datadir}/%{name}/*.tcl $RPM_BUILD_ROOT%{_datadir}/%{name}/*.ocf

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Install icon and desktop file
install -Dpm 0644 %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
desktop-file-install --dir $RPM_BUILD_ROOT/%{_desktopdir}/ %SOURCE2

# Delete the doc folder, the files are in %%doc below
rm -rf $RPM_BUILD_ROOT/%{_docdir}

# Install private headers
(
cd libsrc
find \( -name *.hpp -or -name *.hxx -or -name *.h -or -name *.ixx -or -name *.jxx \) -exec install -Dpm 0644 {} $RPM_BUILD_ROOT%{_includedir}/%{name}/private/{} \;
)


%post common
%update_desktop_database
/bin/%update_icon_cache_post hicolor &>/dev/null || :

%postun common
%update_desktop_database
if [ $1 -eq 0 ] ; then
    /bin/%update_icon_cache_post hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans common
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post openmpi-libs -p /sbin/ldconfig
%postun openmpi-libs -p /sbin/ldconfig

%post mpich-libs -p /sbin/ldconfig
%postun mpich-libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(644,root,root,755)
%doc AUTHORS doc/ng4.pdf
%{_datadir}/%{name}/
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_desktopdir}/%{name}.desktop

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%files libs
%defattr(644,root,root,755)
%{_libdir}/*.so.*
%{_libdir}/libnglib-%{version}.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%exclude %{_includedir}/%{name}/private
%{_libdir}/*.so
%exclude %{_libdir}/libnglib-%{version}.so
%{_pkgconfigdir}/%{name}.pc

%files devel-private
%defattr(644,root,root,755)
%{_includedir}/%{name}/private

%files openmpi
%defattr(644,root,root,755)
%{_libdir}/openmpi/bin/*

%files openmpi-libs
%defattr(644,root,root,755)
%{_libdir}/openmpi/lib/*.so.*
%{_libdir}/openmpi/lib/libnglib-%{version}.so

%files openmpi-devel
%defattr(644,root,root,755)
%{_includedir}/openmpi*/%{name}
%{_libdir}/openmpi/lib/*.so
%{_libdir}/openmpi/lib/pkgconfig/%{name}.pc
%exclude %{_libdir}/openmpi/lib/libnglib-%{version}.so

%files mpich
%defattr(644,root,root,755)
%{_libdir}/mpich/bin/*

%files mpich-libs
%defattr(644,root,root,755)
%{_libdir}/mpich/lib/*.so.*
%{_libdir}/mpich/lib/libnglib-%{version}.so

%files mpich-devel
%defattr(644,root,root,755)
%{_includedir}/mpich*/%{name}
%{_libdir}/mpich/lib/*.so
%{_libdir}/mpich/lib/pkgconfig/%{name}.pc
%exclude %{_libdir}/mpich/lib/libnglib-%{version}.so
