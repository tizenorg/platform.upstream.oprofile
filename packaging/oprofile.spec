Name:           oprofile
Version:        0.9.8
Release:        0
License:        GPL-2.0+ and LGPL-2.1+
Summary:        System wide profiler
Url:            http://oprofile.sf.net
Group:          Base/Tools
Source:         %{name}-%{version}.tar.gz
BuildRequires:  binutils-devel
BuildRequires:  pkgconfig(popt)
Requires:       which
Requires(pre): pwdutils

%description
OProfile is a profiling system for systems running Linux. The
profiling runs transparently during the background, and profile data
can be collected at any time. OProfile makes use of the hardware performance
counters provided on Intel P6, and AMD Athlon family processors, and can use
the RTC for profiling on other x86 processor types.

See the HTML documentation for further details.

%package devel
Summary:        Header files and libraries for developing apps which will use oprofile
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Header files and libraries for developing apps which will use oprofile.

%package jit
Summary:        Libraries required for profiling Java and other JITed code
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description jit
This package includes a base JIT support library, as well as a Java
agent library.

%prep
%setup -q

%build
%configure --enable-gui=no
make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/oprofile" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/oprofile-%{_arch}.conf

rm -rf %{buildroot}%{_datadir}/doc

%pre
getent group oprofile >/dev/null || groupadd -r -g 16 oprofile
getent passwd oprofile >/dev/null || \
useradd -g oprofile -d /var/lib/oprofile -M -r -u 16 -s /sbin/nologin \
    -c "Special user account to be used by OProfile" oprofile
exit 0

%postun
# do not try to remove existing oprofile user or group

%post jit -p /sbin/ldconfig

%postun jit -p /sbin/ldconfig

%docs_package

%files
%license COPYING
%{_bindir}/ophelp
%{_bindir}/opimport
%{_bindir}/opannotate
%{_bindir}/opcontrol
%{_bindir}/opgprof
%{_bindir}/opreport
%{_bindir}/oprofiled
%{_bindir}/oparchive
%{_bindir}/opjitconv
%{_bindir}/op-check-perfevents
%{_bindir}/operf
%{_datadir}/oprofile

%files devel
%{_includedir}/opagent.h

%files jit
%config %{_sysconfdir}/ld.so.conf.d/*
%{_libdir}/oprofile
