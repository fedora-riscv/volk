Name:          volk
Version:       2.4.1
Release:       2%{?dist}
Summary:       The Vector Optimized Library of Kernels
License:       GPLv3+
URL:           https://github.com/gnuradio/%{name}
Source0:       https://github.com/gnuradio/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:       https://github.com/gnuradio/volk/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
Source2:       https://github.com/gnuradio/volk/releases/download/v2.4.1/gpg_volk_release_key.asc

BuildRequires: gnupg2
BuildRequires: make
BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: python3-devel
BuildRequires: python3-mako
BuildRequires: orc-devel
BuildRequires: sed
Conflicts:     python3-gnuradio < 3.9.0.0
Conflicts:     gnuradio-devel < 3.9.0.0

%description
VOLK is the Vector-Optimized Library of Kernels. It is a library that contains
kernels of hand-written SIMD code for different mathematical operations.
Since each SIMD architecture can be very different and no compiler has yet
come along to handle vectorization properly or highly efficiently, VOLK
approaches the problem differently. VOLK is a sub-project of GNU Radio.


%package devel
Summary:       Development files for VOLK
Requires:      %{name}%{?_isa} = %{version}-%{release}


%description devel
%{summary}.


%package doc
Summary:       Documentation files for VOLK
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch


%description doc
%{summary}.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

# fix shebangs
pushd python/volk_modtool
sed -i '1 {/#!\s*\/usr\/bin\/env\s\+python/ d}' __init__.py cfg.py
popd

%build
# workaround, the code is not yet compatible with the strict-aliasing
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="$CFLAGS"
%cmake
%cmake_build

cd %{_vpath_builddir}
make volk_doc %{?_smp_mflags}


# temporally disabled the testsuite due to https://github.com/gnuradio/volk/issues/442
# gnuradio (and all volk consumers) could coredump on s390x and ppc64le under some
# circumstances, see https://bugzilla.redhat.com/show_bug.cgi?id=1917625#c6
#%%check
#cd %{_vpath_builddir}
#make test


%install
%cmake_install

# docs
mkdir -p %{buildroot}%{_docdir}/%{name}
pushd %{_vpath_builddir}
cp -a html %{buildroot}%{_docdir}/%{name}
popd

# drop static objects
rm -f %{buildroot}%{_libdir}/libcpu_features.a

%files
%license COPYING
%doc README.md CHANGELOG.md
%{_bindir}/list_cpu_features
%{_bindir}/volk-config-info
%{_bindir}/volk_modtool
%{_bindir}/volk_profile
%{_libdir}/libvolk*.so.*
%{python3_sitearch}/volk_modtool


%files devel
%{_includedir}/volk
%{_includedir}/cpu_features
%{_libdir}/libvolk.so
%{_libdir}/cmake/volk
%{_libdir}/cmake/CpuFeatures
%{_libdir}/pkgconfig/*.pc


%files doc
%doc %{_docdir}/%{name}/html


%changelog
* Tue Jan 19 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-2
- Fixed according to the review
  Related: rhbz#1917625

* Mon Jan 18 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-1
- Initial release
  Related: rhbz#1917167
