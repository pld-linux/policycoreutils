%include	/usr/lib/rpm/macros.perl
Summary:	SELinux policy core utilities
Summary(pl):	Podstawowe narzêdzia dla polityki SELinux
Name:		policycoreutils
Version:	1.30
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
# Source0-md5:	02a05b3d24483e492bace1a219425567
Source1:	%{name}-newrole.pamd
Source2:	%{name}-run_init.pamd
Source3:	%{name}-pl.po
BuildRequires:	audit-libs-devel
BuildRequires:	gettext-devel
BuildRequires:	libselinux-devel >= 0:1.30
BuildRequires:	libsemanage-devel >= 1.6
BuildRequires:	libsepol-static >= 1.12
BuildRequires:	pam-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
Requires:	libselinux >= 0:1.30
Requires:	libsemanage >= 1.6
Requires:	python
Requires:	python-modules
Requires:	python-semanage >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Security-enhanced Linux is a patch of the Linux kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux. The Security-enhanced Linux kernel
contains new architectural components originally developed to improve
the security of the Flask operating system. These architectural
components provide general support for the enforcement of many kinds
of mandatory access control policies, including those based on the
concepts of Type Enforcement, Role-based Access Control, and
Multi-level Security.

policycoreutils contains the policy core utilities that are required
for basic operation of a SELinux system. These utilities include
load_policy to load policies, setfiles to label filesystems, newrole
to switch roles, and run_init to run /etc/init.d scripts in the proper
context.

%description -l pl
Security-enhanced Linux jest prototypem j±dra Linuksa i wielu
aplikacji u¿ytkowych o funkcjach podwy¿szonego bezpieczeñstwa.
Zaprojektowany jest tak, aby w prosty sposób ukazaæ znaczenie
obowi±zkowej kontroli dostêpu dla spo³eczno¶ci linuksowej. Ukazuje
równie¿ jak tak± kontrolê mo¿na dodaæ do istniej±cego systemu typu
Linux. J±dro SELinux zawiera nowe sk³adniki architektury pierwotnie
opracowane w celu ulepszenia bezpieczeñstwa systemu operacyjnego
Flask. Te elementy zapewniaj± ogólne wsparcie we wdra¿aniu wielu typów
polityk obowi±zkowej kontroli dostêpu, w³±czaj±c te wzorowane na: Type
Enforcement (TE), kontroli dostêpu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

policycoreutils zawiera narzêdzia do ustalania polityki, które s±
niezbêdne do podstawowych operacji na systemie SELinux. Pakiet zawiera
load_policy do wczytywania polityki, setfiles do znaczenia systemu
plików, newrole do prze³±czania ról i run_init do uruchamiania we
w³a¶ciwym kontek¶cie skryptów zawartych w /etc/rc.d/init.d.

%package tools-perl
Summary:	policycoreutils tools written in Perl
Summary(pl):	Zestaw narzêdzi i skryptów policycoreutils napisanych w Perlu
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description tools-perl
policycoreutils tools written in Perl.

%description tools-perl -l pl
Zestaw narzêdzi i skryptów policycoreutils napisanych w Perlu.

%prep
%setup -q

cp -f %{SOURCE3} po/pl.po

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LIBDIR="%{_libdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8},/etc/{pam.d,security/console.apps}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	PYTHONLIBDIR=$RPM_BUILD_ROOT%{py_scriptdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/newrole
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/run_init
:> $RPM_BUILD_ROOT/etc/security/console.apps/run_init

%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/*.py

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog
%attr(4755,root,root) %{_bindir}/chcat
%attr(4755,root,root) %{_bindir}/newrole
%attr(4755,root,root) %{_bindir}/semodule_*
%attr(755,root,root) /sbin/fixfiles
%attr(755,root,root) /sbin/restorecon
%attr(755,root,root) %{_sbindir}/audit2why
%attr(755,root,root) %{_sbindir}/genhomedircon
%attr(755,root,root) %{_sbindir}/load_policy
%attr(755,root,root) %{_sbindir}/open_init_pty
%attr(755,root,root) %{_sbindir}/run_init
%attr(755,root,root) %{_sbindir}/semanage
%attr(755,root,root) %{_sbindir}/semodule
%attr(755,root,root) %{_sbindir}/setfiles
%attr(755,root,root) %{_sbindir}/setsebool
%attr(755,root,root) %{_sbindir}/sestatus
%{py_sitescriptdir}/seobject.py[co]
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/newrole
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/run_init
%config(missingok) /etc/security/console.apps/*
%config(noreplace) %verify(not md5 mtime size) /etc/sestatus.conf
%{_mandir}/man1/newrole.1*
%{_mandir}/man8/*

%files tools-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/audit2allow
%{_mandir}/man1/audit2allow.1*
