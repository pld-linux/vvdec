#
# Conditional build:
%bcond_with	sse4		# SSE4.1 (obligatory) and optionally AVX+ instructions
#
Summary:	Fraunhofer Versatile Video Decoder (VVdeC)
Summary(pl.UTF-8):	VVdeC - dekoder obrazu Fraunhofer Versatile Video
Name:		vvdec
Version:	2.3.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/fraunhoferhhi/vvdec/releases
Source0:	https://github.com/fraunhoferhhi/vvdec/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	68a2aca2c08be29810ed4997e8c92f19
Patch0:		%{name}-pc.patch
Patch1:		%{name}-no-simd.patch
URL:		https://github.com/fraunhoferhhi/vvdec
BuildRequires:	cmake >= 3.12.0
# C++14
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with sse4}
Requires:	cpuinfo(sse4_1)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VVdeC, the Fraunhofer Versatile Video Decoder, is a fast software
H.266/VVC decoder implementation supporting all features of the VVC
Main10 profile.

%description -l pl.UTF-8
VVdeC (Fraunhofer Versatile Video Decoder) to szybka implementacja
programowego dekodera H.266/VVC, obsługująca całą funkcjonalność
profilu VVC Main10.

%package devel
Summary:	Header files for VVdeC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki VVdeC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:5

%description devel
Header files for VVdeC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki VVdeC.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_SKIP_INSTALL_RPATH=ON \
	%{!?with_sse41:-DVVDEC_ENABLE_X86_SIMD=OFF} \
	-DVVDEC_INSTALL_VVDECAPP=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -dp build/source/Lib/vvdec/libvvdec.so* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md LICENSE.txt README.md
%attr(755,root,root) %{_libdir}/libvvdec.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvvdec.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvvdec.so
%{_libdir}/cmake/vvdec
%{_includedir}/vvdec
%{_pkgconfigdir}/libvvdec.pc
