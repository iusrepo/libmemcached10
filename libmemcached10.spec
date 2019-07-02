%global with_tests       %{?_with_tests:1}%{!?_with_tests:0}

%global real_name libmemcached
%global name libmemcached10
%global base_ver 1.0

Name:      %{name}
Summary:   Client library and command line tools for memcached server
Version:   1.0.16
Release:   1.ius%{?dist}
License:   BSD
Group:     System Environment/Libraries
URL:       http://libmemcached.org/
Source:    http://launchpad.net/libmemcached/1.0/%{version}/+download/%{real_name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cyrus-sasl-devel

BuildRequires: flex bison
Conflicts: %{real_name} < %{base_ver}
%if %{with_tests}
BuildRequires: memcached
%endif

#RHEL 5 needs a newer verison than stock gcc and gcc-c++
%if 0%{?rhel} < 6
BuildRequires: gcc44 gcc44-c++
%else
BuildRequires: gcc gcc-c++
%endif

%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildRequires: systemtap-sdt-devel
%endif
%if 0%{?fedora} >= 11 || 0%{?rhel} >= 5
BuildRequires: libevent-devel
%endif


%description
libmemcached is a C/C++ client library and tools for the memcached server
(http://memcached.org/). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

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
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: cyrus-sasl-devel%{?_isa}

%description devel
This package contains the header files and development libraries
for %{real_name}. If you like to develop programs using %{real_name}, 
you will need to install %{real_name}-devel.


%prep
%setup -q -n %{real_name}-%{version}

mkdir examples
cp -p tests/*.{cc,h} examples/

# Will be regenerated during build
%if 0%{?fedora} > 9 || 0%{?rhel} > 5
rm -f libmemcached/csl/{parser,scanner}.cc
%endif

# Temporary fix for SASL detection
#sed -i -e s/ax_cv_sasl/ac_enable_sasl/ configure


%build
%if 0%{?rhel} < 6
export CC=/usr/bin/gcc44
export CXX=/usr/bin/g++44
%endif
# option --with-memcached=false to disable server binary check (as we don't run test)
%configure --disable-static \
#%if ! %{with_tests}
#   --with-memcached=false
#%endif

make %{_smp_mflags}


%install
rm -rf %{buildroot}
make install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""


%check
%if %{with_tests}
# test suite cannot run in mock (same port use for memcache servers on all arch)
# All tests completed successfully
# diff output.res output.cmp fails but result depend on server version
make test
%else
echo 'Test suite disabled (missing "--with tests" option)'
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%exclude %{_libdir}/lib*.la
%{_libdir}/libhashkit.so.2*
%{_libdir}/libmemcached.so.11*
%{_libdir}/libmemcachedutil.so.2*


%files devel
%defattr (-,root,root,-) 
%doc examples
%{_includedir}/libmemcached
%{_includedir}/libmemcached-1.0
%{_includedir}/libhashkit
%{_includedir}/libhashkit-1.0
%{_includedir}/libmemcachedutil-1.0
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_datadir}/aclocal/ax_libmemcached.m4


%changelog
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
