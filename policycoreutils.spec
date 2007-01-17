# TODO: PLDify init.d/restorecond (uses bashisms instead of our nls)
#
# Conditional build:
%bcond_with	restorecond	# build restorecond (glibc>2.4)
#
%include	/usr/lib/rpm/macros.perl
Summary:	SELinux policy core utilities
Summary(pl):	Podstawowe narz�dzia dla polityki SELinux
Name:		policycoreutils
Version:	1.32
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
# Source0-md5:	78b90e86173cd31bfc17a7a154461a0c
Source1:	%{name}-newrole.pamd
Source2:	%{name}-run_init.pamd
Source3:	%{name}-pl.po
BuildRequires:	audit-libs-devel
BuildRequires:	gettext-devel
%{?with_restorecond:BuildRequires:	glibc-devel >= 6:2.4}
BuildRequires:	libselinux-devel >= 0:1.32
BuildRequires:	libsemanage-devel >= 1.8
BuildRequires:	libsepol-static >= 1.14
BuildRequires:	pam-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
Requires:	libselinux >= 0:1.32
Requires:	libsemanage >= 1.8
Requires:	python
Requires:	python-modules
Requires:	python-semanage >= 1.8
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
Security-enhanced Linux jest prototypem j�dra Linuksa i wielu
aplikacji u�ytkowych o funkcjach podwy�szonego bezpiecze�stwa.
Zaprojektowany jest tak, aby w prosty spos�b ukaza� znaczenie
obowi�zkowej kontroli dost�pu dla spo�eczno�ci linuksowej. Ukazuje
r�wnie� jak tak� kontrol� mo�na doda� do istniej�cego systemu typu
Linux. J�dro SELinux zawiera nowe sk�adniki architektury pierwotnie
opracowane w celu ulepszenia bezpiecze�stwa systemu operacyjnego
Flask. Te elementy zapewniaj� og�lne wsparcie we wdra�aniu wielu typ�w
polityk obowi�zkowej kontroli dost�pu, w��czaj�c te wzorowane na: Type
Enforcement (TE), kontroli dost�pu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

policycoreutils zawiera narz�dzia do ustalania polityki, kt�re s�
niezb�dne do podstawowych operacji na systemie SELinux. Pakiet zawiera
load_policy do wczytywania polityki, setfiles do znaczenia systemu
plik�w, newrole do prze��czania r�l i run_init do uruchamiania we
w�a�ciwym kontek�cie skrypt�w zawartych w /etc/rc.d/init.d.

%package tools-perl
Summary:	policycoreutils tools written in Perl
Summary(pl):	Zestaw narz�dzi i skrypt�w policycoreutils napisanych w Perlu
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description tools-perl
policycoreutils tools written in Perl.

%description tools-perl -l pl
Zestaw narz�dzi i skrypt�w policycoreutils napisanych w Perlu.

%package restorecond
Summary:	restorecond - daemon which corrects contexts of newly created files
Summary(pl):	restorecond - demon poprawiaj�cy konteksty nowo tworzonych plik�w
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description restorecond
restorecond daemon uses inotify to watch files listed in the
/etc/selinux/restorecond.conf, when they are created, this daemon will
make sure they have the correct file context associated with the
policy.

%description restorecond -l pl
Demon restorecond u�ywa inotify do �ledzenia plik�w wymienionych w
pliku /etc/selinux/restorecond.conf, aby przy ich tworzeniu upewni�
si�, �e maj� przypisane w�a�ciwe konteksty plik�w z polityki.

%prep
%setup -q

cp -f %{SOURCE3} po/pl.po
%{!?with_restorecond:sed -i 's/restorecond//' Makefile}

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
%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post restorecond
/sbin/chkconfig --add restorecond
%service restorecond restart

%preun restorecond
if [ "$1" = "0" ]; then
	%service restorecond stop
	/sbin/chkconfig --del restorecond
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog
%attr(4755,root,root) %{_bindir}/chcat
%attr(4755,root,root) %{_bindir}/newrole
%attr(4755,root,root) %{_bindir}/secon
%attr(4755,root,root) %{_bindir}/semodule_*
%attr(755,root,root) /sbin/fixfiles
%attr(755,root,root) /sbin/restorecon
%attr(755,root,root) /sbin/setfiles
%attr(755,root,root) %{_sbindir}/audit2why
%attr(755,root,root) %{_sbindir}/genhomedircon
%attr(755,root,root) %{_sbindir}/load_policy
%attr(755,root,root) %{_sbindir}/open_init_pty
%attr(755,root,root) %{_sbindir}/run_init
%attr(755,root,root) %{_sbindir}/semanage
%attr(755,root,root) %{_sbindir}/semodule
%attr(755,root,root) %{_sbindir}/setsebool
%attr(755,root,root) %{_sbindir}/sestatus
%{py_sitescriptdir}/*.py[co]
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/newrole
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/run_init
%config(missingok) /etc/security/console.apps/*
%config(noreplace) %verify(not md5 mtime size) /etc/sestatus.conf
%{_mandir}/man1/newrole.1*
%{_mandir}/man1/secon.1*
%{_mandir}/man8/audit2why.8*
%{_mandir}/man8/chcat.8*
%{_mandir}/man8/fixfiles.8*
%{_mandir}/man8/genhomedircon.8*
%{_mandir}/man8/load_policy.8*
%{_mandir}/man8/open_init_pty.8*
%{_mandir}/man8/restorecon.8*
%{_mandir}/man8/run_init.8*
%{_mandir}/man8/semanage.8*
%{_mandir}/man8/semodule*.8*
%{_mandir}/man8/sestatus.8*
%{_mandir}/man8/setfiles.8*
%{_mandir}/man8/setsebool.8*

%files tools-perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/audit2allow
%{_mandir}/man1/audit2allow.1*

%if %{with restorecond}
%files restorecond
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/restorecond
%attr(754,root,root) /etc/rc.d/init.d/restorecond
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/selinux/restorecond.conf
%{_mandir}/man8/restorecond.8*
%endif
