%include	/usr/lib/rpm/macros.perl
Summary:	SELinux policy core utilities
Summary(pl):	Podstawowe narzêdzia dla polityki SELinux
Name:		policycoreutils
Version:	1.10
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
# Source0-md5:	50c449595b8d415e2e00afd1bea2abe0
Source1:	%{name}-newrole.pamd
Source2:	%{name}-run_init.pamd
Source3:	%{name}-pl.po
BuildRequires:	gettext-devel
BuildRequires:	libselinux-devel >= 0:1.10
BuildRequires:	pam-devel
BuildRequires:	rpm-perlprov
Requires:	libselinux >= 0:1.10
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Security-enhanced Linux is a patch of the LinuxÂ® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux. The Security-enhanced Linux kernel
contains new architectural components originally developed to improve
the security of the Flask operating system. These architectural
components provide general support for the enforcement of many kinds
of mandatory access control policies, including those based on the
concepts of Type EnforcementÂ®, Role-based Access Control, and
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
obowi±zkowej kontroli dostêpu dla spo³eczno¶ci Linuksowej. Ukazuje
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
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8},/etc/{pam.d,security/console.apps}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/newrole
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/run_init
:> $RPM_BUILD_ROOT/etc/security/console.apps/run_init

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(4755,root,root) %{_bindir}/newrole
%attr(755,root,root) %{_sbindir}/genhomedircon
%attr(755,root,root) %{_sbindir}/load_policy
%attr(755,root,root) /sbin/restorecon
%attr(755,root,root) %{_sbindir}/run_init
%attr(755,root,root) %{_sbindir}/setfiles
%attr(755,root,root) %{_sbindir}/sestatus
%config(noreplace) %verify(not size mtime md5) /etc/pam.d/newrole
%config(noreplace) %verify(not size mtime md5) /etc/pam.d/run_init
%config(missingok) /etc/security/console.apps/*
%config(noreplace) %verify(not size mtime md5) /etc/sestatus.conf
%{_mandir}/man[18]/*

%files tools-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/audit2allow
