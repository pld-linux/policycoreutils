Summary:	SELinux policy core utilities
Summary(pl):	Podstawowe narzêdzia dla polityki SELinux
Name:		policycoreutils
Version:	1.2
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
# Source0-md5:	eca60ac3947353128e226f64cb9adc55
BuildRequires:	glibc-static
BuildRequires:	libselinux-static
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
mandatowej kontroli dostêpu dla spo³eczno¶ci Linuksowej. Ukazuje
równie¿ jak tak± kontrolê mo¿na dodaæ do istniej±cego systemu typu
Linux. J±dro SELinux zawiera nowe sk³adniki architektury pierwotnie
opracowane w celu ulepszenia bezpieczeñstwa systemu operacyjnego
Flask. Te elementy zapewniaj± ogólne wsparcie we wdra¿aniu wielu typów
polityk mandatowej kontroli dostêpu, w³±czaj±c te wzorowane na: Type
Enforcement (TE), kontroli dostêpu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

policycoreutils zawiera narzêdzia do ustalania polityki, które s±
niezbêdne do podstawowych operacji na systemie SELinux. Pakiet zawiera
load_policy do wczytywania polityki, setfiles do znaczenia systemu
plików, newrole do prze³±czania ról i run_init do uruchamiania we
w³a¶ciwym kontek¶cie skryptów zawartych w /etc/rc.d/init.d.

%prep
%setup -q

%build
# CFLAGS must be passed in environment, not as make argument
# (because of CFLAGS+=...)
CFLAGS="%{rpmcflags}" \
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8},/etc/pam.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/setfiles
%attr(755,root,root) %{_sbindir}/load_policy
%attr(755,root,root) %{_sbindir}/run_init
%attr(755,root,root) %{_bindir}/newrole
%config(noreplace) %verify(not size mtime md5) /etc/pam.d/newrole
%config(noreplace) %verify(not size mtime md5) /etc/pam.d/run_init
%{_mandir}/man[18]/*
