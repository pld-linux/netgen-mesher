# TODO:
# USE_SPDLOG?
# USE_CGNS? (requires cgnslib.h + libsgns, <https://github.com/CGNS/CGNS>)
#
# Conditional build:
%bcond_with	mpich		# build mpich packages
#
Summary:	Automatic mesh generation tool
Summary(pl.UTF-8):	Narzędzie do automatycznego generowania siatek
Name:		netgen-mesher
Version:	6.2.2404
Release:	5
License:	LGPL v2
Group:		Applications/Science
Source0:	https://github.com/NGSolve/netgen/archive/v%{version}/netgen-%{version}.tar.gz
# Source0-md5:	0d1dd5b8858e35ed2564ec86703ff602
Source1:	%{name}.png
Source2:	%{name}.desktop
# Set a default NETGENDIR appropriate for the fedora packaging
Patch0:		netgen-5.3.0_netgendir.patch
# Make some includes relative (needed for when headers are in -private subpackage)
Patch1:		netgen-5.3.0_relative-includes.patch
# Rename shared libaries (the original names are often way too generic), add library version
Patch2:		0002-Rename-libraries-add-library-versions.patch
# Rename binary in cmake so that exported modules work correctly
Patch3:		0010-rename-netgen-binary.patch
# Link against libjpeg and ffmpeg
Patch4:		link-libraries.patch
# Fix fallback version
# See https://bugzilla.redhat.com/show_bug.cgi?id=1993574#c11
Patch5:		netgen_fallback-version.patch
# Fix Status typedef symbol collision by re-ordering includes
# /usr/include/mpich-x86_64/mpicxx.h:160:18: error: expected identifier before ‘int’
#   160 |     friend class Status;
Patch6:		netgen_include-order.patch
# Fix invalid egg-info version
Patch7:		%{name}_egg-info-version.patch
Patch8:		std-namespace.patch
Patch9:		%{name}-arch.patch
URL:		https://www.ngsolve.org/
BuildRequires:	OpenCASCADE-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	ffmpeg-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	metis-devel
%{?with_mpich:BuildRequires:	mpich-c++-devel}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-pybind11
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk-devel >= 8.5
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	zlib-devel
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
ExclusiveArch:	%{x8664} %{arm} aarch64 i686 pentium2 pentium3 pentium4 athlon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# false negative _ZN6ngcore11TaskManager9thread_idE from libngcore
%define		skip_post_check_so	libnglib.so.*

%description
NETGEN is an automatic 3D tetrahedral mesh generator. It accepts input
from constructive solid geometry (CSG) or boundary representation
(BRep) from STL file format. The connection to a geometry kernel
allows the handling of IGES and STEP files. NETGEN contains modules
for mesh optimization and hierarchical mesh refinement.

%description -l pl.UTF-8
NETGEN to automatyczny generator siatek tetraedralnych 3D. Przyjmuje
na wejściu pliki w formacie CSG (Constructive Solid Geometry) lub STL
(reprezentację ograniczeń - BRep). Połączenie z jądrem geometrycznym
pozwala na obsługę plików IGES oraz STEP. NETGEN zawiera moduły do
optymalizacji oraz hierarchicznego zagęszczania siatki.

%package common
Summary:	Common files for netgen
Summary(pl.UTF-8):	Wspólne pliki netgen
Group:		Applications/Science
Requires:	hicolor-icon-theme
Requires:	tix
BuildArch:	noarch

%description common
Common files for netgen.

%description common -l pl.UTF-8
Wspólne pliki netgen.

%package libs
Summary:	Netgen libraries
Summary(pl.UTF-8):	Biblioteki Netgen
Group:		Libraries

%description libs
Netgen libraries.

%description libs -l pl.UTF-8
Biblioteki Netgen.

%package devel
Summary:	Development files for Netgen
Summary(pl.UTF-8):	Pliki programistyczne Netgen
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for Netgen.

%description devel -l pl.UTF-8
Pliki programistyczne Netgen.

%package devel-private
Summary:	Private headers of Netgen
Summary(pl.UTF-8):	Prywatne pliki nagłówkowe Netgen
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description devel-private
Private headers of Netgen, needed to build certain netgen based
software packages.

%description devel-private -l pl.UTF-8
Prywatne pliki nagłówkowe Netgen, potrzebne do budowania niektórych
pakietów oprogramowania opartego na netgen.

%package -n python3-%{name}
Summary:	Python 3 interface for Netgen
Summary(pl.UTF-8):	Interfejs Pythona 3 do Netgen
Group:		Libraries/Python
%{?python_provide:%python_provide python3-netgen}
Requires:	%{name}-libs = %{version}-%{release}

%description -n python3-%{name}
Python 3 interface for Netgen.

%description -n python3-%{name} -l pl.UTF-8
Interfejs Pythona 3 do Netgen.

%package mpich
Summary:	Netgen compiled against mpich
Summary(pl.UTF-8):	Netgen skompilowany z obsługą mpich
Group:		Applications/Science
# Require explicitly for dir ownership and to guarantee the pickup of the right runtime
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{name}-mpich-libs = %{version}-%{release}
Requires:	mpich

%description mpich
Netgen compiled against mpich.

%description mpich -l pl.UTF-8
Netgen skompilowany z obsługą mpich.

%package mpich-libs
Summary:	Netgen libraries compiled against mpich
Summary(pl.UTF-8):	Biblioteki Netgen skompilowane z obsługą mpich
Group:		Development/Libraries

%description mpich-libs
Netgen libraries compiled against mpich.

%description mpich-libs -l pl.UTF-8
Biblioteki Netgen skompilowane z obsługą mpich.

%package mpich-devel
Summary:	Development files for Netgen compiled against mpich
Summary(pl.UTF-8):	Pliki programistyczne Netgen z obsługą mpich
Group:		Development/Libraries
# Require explicitly for dir ownership
Requires:	%{name}-mpich = %{version}-%{release}
Requires:	mpich-devel

%description mpich-devel
Development files for Netgen compiled against mpich.

%description mpich-devel -l pl.UTF-8
Pliki programistyczne Netgen z obsługą mpich.

%prep
%setup -q -n netgen-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1
%patch -P 8 -p1
%patch -P 9 -p1

%build
%cmake -B build \
	-DUSE_SUPERBUILD=OFF \
	-DUSE_NATIVE_ARCH=OFF \
	-DNG_INSTALL_SUFFIX=netgen-mesher \
	-DNG_INSTALL_DIR_INCLUDE=%{_includedir}/%{name} \
	-DNG_INSTALL_DIR_LIB=%{_libdir} \
	-DNG_INSTALL_DIR_CMAKE=%{_libdir}/cmake/%{name} \
	-DNG_INSTALL_DIR_PYTHON=%{py3_sitedir} \
	-DPREFER_SYSTEM_PYBIND11=ON \
	-DUSE_JPEG=ON \
	-DUSE_MPEG=ON \
	-DUSE_OCC=ON \
	-DOpenGL_GL_PREFERENCE=GLVND

%{__make} -C build

### mpich version ###
%if %{with mpich}
export CXX=mpicxx
%cmake -B build-mpich \
	-DUSE_SUPERBUILD=OFF \
	-DUSE_NATIVE_ARCH=OFF \
	-DNG_INSTALL_SUFFIX=netgen-mesher \
	-DNG_INSTALL_DIR_INCLUDE=%{_includedir}/mpich/%{name} \
	-DNG_INSTALL_DIR_BIN=%{_libdir}/mpich/bin/ \
	-DNG_INSTALL_DIR_LIB=%{_libdir}/mpich/lib/ \
	-DNG_INSTALL_DIR_CMAKE=%{_libdir}/mpich/lib/cmake/%{name} \
	-DNG_INSTALL_DIR_PYTHON=%{_libdir}/mpich/python%{python3_version}/site-packages \
	-DPREFER_SYSTEM_PYBIND11=ON \
	-DUSE_JPEG=ON \
	-DUSE_MPEG=ON \
	-DUSE_OCC=ON \
	-DUSE_MPI=ON \
	-DOpenGL_GL_PREFERENCE=GLVND

%{__make} -C build-mpich
%endif

%install
%define writepkgconfig() \
install -d -m 0755 $RPM_BUILD_ROOT/$MPI_LIB/pkgconfig; \
cat > $RPM_BUILD_ROOT/$MPI_LIB/pkgconfig/%{name}.pc << EOF\
prefix=%{_prefix}\
exec_prefix=${prefix}\
libdir=$MPI_LIB\
includedir=$MPI_INCLUDE/%{name}\
\
Name: %{name}\
Description: %{summary}\
Version: %{version}\
Libs: -L\\\${libdir} -lnglib\
Libs.private: -lngcore
Cflags: -I\\\${includedir}\
EOF\
%{nil}

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/%{name}/private,%{_iconsdir}/hicolor/48x48/apps,%{_desktopdir}}

### mpich version ###
%if %{with mpich}
%{__make} -C build-mpich install \
	DESTDIR=$RPM_BUILD_ROOT
%writepkgconfig
# Avoid conflicts with netgen, remove data files (are correctly installed below)
%{__mv} $RPM_BUILD_ROOT/$MPI_BIN/netgen $RPM_BUILD_ROOT/$MPI_BIN/%{name}
%{__rm} $RPM_BUILD_ROOT/$MPI_BIN/*.tcl rm -f $RPM_BUILD_ROOT/$MPI_BIN/*.ocf
%endif

### serial version ###
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

export MPI_LIB=%{_libdir}
export MPI_INCLUDE=%{_includedir}
%writepkgconfig

# Install icon and desktop file
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png
desktop-file-install --dir $RPM_BUILD_ROOT%{_desktopdir}/ %{SOURCE2}

# Install the nglib.h header
cp -p nglib/nglib.h $RPM_BUILD_ROOT%{_includedir}/%{name}/nglib.h

# Install private headers
cd libsrc
find \( -name *.hpp -or -name *.hxx -or -name *.h -or -name *.ixx -or -name *.jxx \) -exec install -Dp {} $RPM_BUILD_ROOT%{_includedir}/%{name}/private/{} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post common
%update_desktop_database
%update_icon_cache hicolor

%postun common
%update_desktop_database
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/netgen-mesher

%files common
%defattr(644,root,root,755)
%doc AUTHORS doc/ng4.pdf
%{_datadir}/%{name}
%{_iconsdir}/hicolor/48x48/apps/netgen-mesher.png
%{_desktopdir}/netgen-mesher.desktop

%files libs
%defattr(644,root,root,755)
%{_libdir}/libngcore.so.*.*
%{_libdir}/libnggui.so.*.*
%{_libdir}/libnglib.so.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libngcore.so
%{_libdir}/libnggui.so
%{_libdir}/libnglib.so
%{_libdir}/libngtogl.a
%{_includedir}/%{name}
%exclude %{_includedir}/%{name}/private
%{_pkgconfigdir}/netgen-mesher.pc
%{_libdir}/cmake/netgen-mesher

%files devel-private
%defattr(644,root,root,755)
%{_includedir}/%{name}/private

%files -n python3-%{name}
%defattr(644,root,root,755)
%dir %{py3_sitedir}/netgen-mesher
%{py3_sitedir}/netgen-mesher/*.py
%{py3_sitedir}/netgen-mesher/libngguipy.so
%{py3_sitedir}/netgen-mesher/libngpy.so
%{py3_sitedir}/netgen-mesher/config
%{py3_sitedir}/netgen_mesher-py3.egg-info
%dir %{py3_sitedir}/pyngcore
%{py3_sitedir}/pyngcore/*.py
%{py3_sitedir}/pyngcore/pyngcore.*.so

%if %{with mpich}
%files mpich
%defattr(644,root,root,755)
%{_libdir}/mpich/bin/*

%files mpich-libs
%defattr(644,root,root,755)
%{_libdir}/mpich/lib/libng*.so.*.*

%files mpich-devel
%defattr(644,root,root,755)
%{_includedir}/mpich*/%{name}
%{_libdir}/mpich/lib/libng*.so
%{_libdir}/mpich/lib/pkgconfig/netgen-mesher.pc
%exclude %{_libdir}/mpich/lib/libnglib-%{version}.so
%endif
