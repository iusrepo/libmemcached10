%global real_name libmemcached
%global base_ver 1.0

Name:      libmemcached10
Summary:   Client library and command line tools for memcached server
Version:   1.0.18
Release:   1%{?dist}
License:   BSD
URL:       http://libmemcached.org/
# Original sources:
#   http://launchpad.net/libmemcached/1.0/%%{version}/+download/libmemcached-%%{version}.tar.gz
# Fedora sources:
Source0:   https://src.fedoraproject.org/lookaside/pkgs/libmemcached/libmemcached-%{version}-exhsieh.tar.gz/b4cd7ccfa1bca8b2563300342b9fd01f/libmemcached-%{version}-exhsieh.tar.gz

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: cyrus-sasl-devel
BuildRequires: flex
BuildRequires: bison
Conflicts: %{real_name} < %{base_ver}
BuildRequires: systemtap-sdt-devel
BuildRequires: libevent-devel

Patch0: libmemcached-fix-linking-with-libpthread.patch
# Fix: ISO C++ forbids comparison between pointer and integer [-fpermissive]
# https://bugs.launchpad.net/libmemcached/+bug/1663985
Patch1: libmemcached-build.patch


%description
libmemcached is a C/C++ client library and tools for the memcached server
(http://memcached.org/). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memaslap    Load testing and benchmarking a server
memcapable  Checking a Memcached server capibilities and compatibility
memcat      Copy the value of a key to standard output
memcp       Copy data to a server
memdump     Dumping your server
memerror    Translate an error code to a string
memexist    Check for the existance of a key
memflush    Flush the contents of your servers
memparse    Parse an option string
memping     Test to see if a server is available.
memrm       Remove a key(s) from the server
memslap     Generate testing loads on a memcached cluster
memstat     Dump the stats of your servers to standard output
memtouch    Touches a key


%package devel
Summary: Header files and development libraries for %{real_name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: cyrus-sasl-devel%{?_isa}

%description devel
This package contains the header files and development libraries
for %{real_name}. If you like to develop programs using %{real_name}, 
you will need to install %{real_name}-devel.


%prep
%setup -q -n %{real_name}-%{version}
%patch0 -p1 -b .link
%patch1 -p1 -b .build

mkdir examples
cp -p tests/*.{cc,h} examples/


%build
# option --with-memcached=false to disable server binary check (as we don't run test)
%configure \
   --with-memcached=false \
   --enable-sasl \
   --enable-libmemcachedprotocol \
   --enable-memaslap \
   --enable-dtrace \
   --disable-static

# for warning: unknown option after '#pragma GCC diagnostic' kind
sed -e 's/-Werror//' -i Makefile

make %{_smp_mflags} V=1


%install
make install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%{_mandir}/man1/mem*
%exclude %{_libdir}/lib*.la
%{_libdir}/libhashkit.so.2*
%{_libdir}/libmemcached.so.11*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.2*


%files devel
%doc examples
%{_includedir}/libmemcached
%{_includedir}/libmemcached-1.0
%{_includedir}/libhashkit
%{_includedir}/libhashkit-1.0
%{_includedir}/libmemcachedprotocol-0.0
%{_includedir}/libmemcachedutil-1.0
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_datadir}/aclocal/ax_libmemcached.m4
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/libhashkit*
%{_mandir}/man3/memcached*
%{_mandir}/man3/hashkit*


%changelog
* Tue Jul 02 2019 Carl George <carl@george.computer> - 1.0.18-1
- Latest upstream
- Add patch0 and patch1 from Fedora

* Thu Aug 29 2013 Ben Harper <ben.harper@rackspace.com> - 1.0.16-1.ius
- latest release, 1.0.16
- removed unpackaged files from %files
- enabling SASL

* Tue Nov 13 2012 Ben Harper <ben.harper@rackspace.com> - 1.0.13-2.ius
- ported from changes made by booi from Remi's build see
  https://bugs.launchpad.net/ius/+bug/1052542/comments/11
- added support for RHEL 5

* Thu Nov 01 2012 Ben Harper <ben.harper@rackspace.com> - 1.0.13-1.ius
- porting from Remi's build
- disabling SASL per http://bugs.launchpad.net/ius/+bug/1052542

* Sun May 27 2012 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8

* Sun Apr 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- update to 1.0.7
- regenerate parser using flex/bison (#816766)

* Sun Apr 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.6-2
- workaround for SASL detection

* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6
- soname bump to libmemcached.so.10 and libhashkit.so.2

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4
- soname bump to libmemcached.so.9
- update description

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Sun Oct 16 2011 Remi Collet <remi@fedoraproject.org> - 0.53-1
- update to 0.53

* Sat Sep 17 2011 Remi Collet <remi@fedoraproject.org> - 0.52-1
- update to 0.52

* Sun Jul 31 2011 Remi Collet <remi@fedoraproject.org> - 0.51-1
- update to 0.51 (soname bump libmemcached.so.8)

* Thu Jun 02 2011 Remi Collet <Fedora@famillecollet.com> - 0.49-1
- update to 0.49
- add build option : --with tests

* Mon Feb 28 2011 Remi Collet <Fedora@famillecollet.com> - 0.47-1
- update to 0.47
- remove patch merged upstream

* Sun Feb 20 2011 Remi Collet <Fedora@famillecollet.com> - 0.46-2
- patch Makefile.in instead of include.am (to avoid autoconf)
- donc requires pkgconfig with arch

* Fri Feb 18 2011 Remi Collet <Fedora@famillecollet.com> - 0.46-1
- update to 0.46

* Sat Feb 12 2011 Remi Collet <Fedora@famillecollet.com> - 0.44-6
- arch specific requires

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Joe Orton <jorton@redhat.com> - 0.44-4
- repackage source tarball to remove non-free Hsieh hash code

* Sat Oct 02 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-3
- improves SASL patch

* Sat Oct 02 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-2
- enable SASL support

* Fri Oct 01 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-1
- update to 0.44
- add soname version in %%file to detect change

* Fri Jul 30 2010 Remi Collet <Fedora@famillecollet.com> - 0.43-1
- update to 0.43

* Wed Jul 07 2010 Remi Collet <Fedora@famillecollet.com> - 0.42-1
- update to 0.42

* Tue May 04 2010 Remi Collet <Fedora@famillecollet.com> - 0.40-1
- update to 0.40 (new soname for libmemcached.so.5)
- new URI (site + source)

* Sat Mar 13 2010 Remi Collet <Fedora@famillecollet.com> - 0.38-1
- update to 0.38

* Sat Feb 06 2010 Remi Collet <Fedora@famillecollet.com> - 0.37-1
- update to 0.37 (soname bump)
- new libhashkit (should be a separated project in the futur)

* Sun Sep 13 2009 Remi Collet <Fedora@famillecollet.com> - 0.31-1
- update to 0.31

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Remi Collet <Fedora@famillecollet.com> - 0.30-1
- update to 0.30

* Tue May 19 2009 Remi Collet <Fedora@famillecollet.com> - 0.29-1
- update to 0.29

* Fri May 01 2009 Remi Collet <Fedora@famillecollet.com> - 0.28-2
- add upstream patch to disable nonfree hsieh hash method

* Sat Apr 25 2009 Remi Collet <Fedora@famillecollet.com> - 0.28-1
- Initial RPM from Brian Aker spec
- create -devel subpackage
- add %%post %%postun %%check section
