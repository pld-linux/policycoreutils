Summary:	SELinux policy core utilities
Summary(pl):	Podstawowe narz�dzia dla polityki SELinux
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
Security-enhanced Linux is a patch of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux. The Security-enhanced Linux kernel
contains new architectural components originally developed to improve
the security of the Flask operating system. These architectural
components provide general support for the enforcement of many kinds
of mandatory access control policies, including those based on the
concepts of Type Enforcement®, Role-based Access Control, and
Multi-level Security.

policycoreutils contains the policy core utilities that are required
for basic operation of a SELinux system. These utilities include
load_policy to load policies, setfiles to label filesystems, newrole
to switch roles, and run_init to run /etc/init.d scripts in the proper
context.

%description -l pl
Security-enhanced Linux jest prototypem j�dra Linuksa i wielu
aplikacji u�ytkowych o funkcjach podwy�szonego bezpiecze�stwa.
Zaprojektowany jest tak, aby w prosty spos�b ukaza� znaczenie
mandatowej kontroli dost�pu dla spo�eczno�ci Linuksowej. Ukazuje
r�wnie� jak tak� kontrol� mo�na doda� do istniej�cego systemu typu
Linux. J�dro SELinux zawiera nowe sk�adniki architektury pierwotnie
opracowane w celu ulepszenia bezpiecze�stwa systemu operacyjnego
Flask. Te elementy zapewniaj� og�lne wsparcie we wdra�aniu wielu typ�w
polityk mandatowej kontroli dost�pu, w��czaj�c te wzorowane na: Type
Enforcement (TE), kontroli dost�pu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

policycoreutils zawiera narz�dzia do ustalania polityki, kt�re s�
niezb�dne do podstawowych operacji na systemie SELinux. Pakiet zawiera
load_policy do wczytywania polityki, setfiles do znaczenia systemu
plik�w, newrole do prze��czania r�l i run_init do uruchamiania we
w�a�ciwym kontek�cie skrypt�w zawartych w /etc/rc.d/init.d.

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
