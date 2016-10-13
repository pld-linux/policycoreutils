# TODO:
# - PLDify init.d/{mcstrans,restorecond} (uses bashisms instead of our nls)
# - PLDify and package init.d/sandbox script; sandbox to subpackage? (seems to use python+pygtk)
#
# Conditional build:
%bcond_without  restorecond   # don't build restorecond (glibc>=2.4)
#
%include	/usr/lib/rpm/macros.perl
Summary:	SELinux policy core utilities
Summary(pl.UTF-8):	Podstawowe narzędzia dla polityki SELinux
Name:		policycoreutils
Version:	2.5
Release:	1
# some parts strictly v2, some v2+
License:	GPL v2
Group:		Applications/System
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20160223/%{name}-%{version}.tar.gz
# Source0-md5:	9ad9331b2133262fb3f774359a7f4761
Source1:	%{name}-newrole.pamd
Source2:	%{name}-run_init.pamd
Patch0:		%{name}-libdir.patch
Patch1:		%{name}-pythondir.patch
URL:		https://github.com/SELinuxProject/selinux/wiki
BuildRequires:	audit-libs-devel
%{?with_restorecond:BuildRequires:	dbus-devel >= 1.0}
BuildRequires:	gettext-tools
%{?with_restorecond:BuildRequires:	glib2-devel >= 2.0}
%{?with_restorecond:BuildRequires:	glibc-devel >= 6:2.4}
BuildRequires:	libcap-ng-devel
BuildRequires:	libcgroup-devel
BuildRequires:	libselinux-devel >= 2.5
BuildRequires:	libsemanage-devel >= 2.5
BuildRequires:	libsepol-static >= 2.5
%{?with_restorecond:BuildRequires:	pkgconfig}
BuildRequires:	pam-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
%{!?with_restorecond:BuildRequires:	sed >= 4.0}
# for sepolicy/sepolgen
BuildRequires:	setools-devel >= 3
Requires:	libselinux >= 2.5
Requires:	libsemanage >= 2.5
Requires:	python
Requires:	python-modules
Requires:	python-semanage >= 2.0
# for audit2allow
Requires:	python-sepolgen
Obsoletes:	policycoreutils-tools-perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Security-enhanced Linux is a patch of the Linux kernel and a number of
utilities with enhanced security functionality designed to add
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

%description -l pl.UTF-8
Security-enhanced Linux jest prototypem jądra Linuksa i wielu
aplikacji użytkowych o funkcjach podwyższonego bezpieczeństwa.
Zaprojektowany jest tak, aby w prosty sposób ukazać znaczenie
obowiązkowej kontroli dostępu dla społeczności linuksowej. Ukazuje
również jak taką kontrolę można dodać do istniejącego systemu typu
Linux. Jądro SELinux zawiera nowe składniki architektury pierwotnie
opracowane w celu ulepszenia bezpieczeństwa systemu operacyjnego
Flask. Te elementy zapewniają ogólne wsparcie we wdrażaniu wielu typów
polityk obowiązkowej kontroli dostępu, włączając te wzorowane na: Type
Enforcement (TE), kontroli dostępu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

policycoreutils zawiera narzędzia do ustalania polityki, które są
niezbędne do podstawowych operacji na systemie SELinux. Pakiet zawiera
load_policy do wczytywania polityki, setfiles do znaczenia systemu
plików, newrole do przełączania ról i run_init do uruchamiania we
właściwym kontekście skryptów zawartych w /etc/rc.d/init.d.

%package restorecond
Summary:	restorecond - daemon which corrects contexts of newly created files
Summary(pl.UTF-8):	restorecond - demon poprawiający konteksty nowo tworzonych plików
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description restorecond
restorecond daemon uses inotify to watch files listed in the
/etc/selinux/restorecond.conf, when they are created, this daemon will
make sure they have the correct file context associated with the
policy.

%description restorecond -l pl.UTF-8
Demon restorecond używa inotify do śledzenia plików wymienionych w
pliku /etc/selinux/restorecond.conf, aby przy ich tworzeniu upewnić
się, że mają przypisane właściwe konteksty plików z polityki.

%package sepolicy
Summary:	SELinux Policy Inspection tool
Summary(pl.UTF-8):	Narzędzie do inspekcji polityk SELinuksa
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	gobject-introspection
Requires:	gtk+2 >= 2
Requires:	python-dbus
Requires:	python-pygobject >= 2
Requires:	python-pygobject3 >= 2
Requires:	python-selinux
Requires:	python-sepolgen
Requires:	python-slip-dbus

%description sepolicy
SELinux Policy Inspection tool.

%description sepolicy -l pl.UTF-8
Narzędzie do inspekcji polityk SELinuksa.

%package mcstrans
Summary:	MCS (Multiple Category System) SELinux service
Summary(pl.UTF-8):	Usługa SELinuksa MCS (Multiple Category System)
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description mcstrans
MCS (Multiple Category System) SELinux service.

%description mcstrans -l pl.UTF-8
Usługa SELinuksa MCS (Multiple Category System).

%package -n bash-completion-%{name}
Summary:	Bash completion for policycoreutils commands
Summary(pl.UTF-8):	Bashowe dopełnianie składni poleceń policycoreutils
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2

%description -n bash-completion-%{name}
Bash completion for policycoreutils commands.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie składni poleceń policycoreutils.

%package -n system-config-selinux
Summary:	Graphical SELinux Management tool
Summary(pl.UTF-8):	Graficzne narzędzie do zarządzania SELinuksem
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-sepolicy = %{version}-%{release}
Requires:	python-gnome >= 2
Requires:	python-pygobject >= 2
Requires:	python-pygtk-glade >= 2:2
Requires:	python-pygtk-gtk >= 2:2
Requires:	python-selinux
Requires:	polkit

%description -n system-config-selinux
system-config-selinux provides a graphical interface for managing the
SELinux configuration.

%description -n system-config-selinux -l pl.UTF-8
system-config-selinux dostarcza graficzny interfejs do zarządzania
konfiguracją SELinuksa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{!?with_restorecond:%{__sed} -i 's/restorecond//' Makefile}

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LIBDIR="%{_libdir}"

CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -W -Wundef -Wmissing-noreturn -Wmissing-format-attribute" \
%{__make} -C mcstrans \
	CC="%{__cc}" \
	LIBDIR="%{_libdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8},/etc/{pam.d,security/console.apps}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBEXECDIR=$RPM_BUILD_ROOT%{_libdir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	PYTHONLIBDIR=$RPM_BUILD_ROOT%{py_scriptdir} \
	SYSTEMDDIR=$RPM_BUILD_ROOT/lib/systemd

%{__make} -C mcstrans install \
	DESTDIR=$RPM_BUILD_ROOT \
	SYSTEMDDIR=$RPM_BUILD_ROOT/lib/systemd

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/newrole
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/run_init
:> $RPM_BUILD_ROOT/etc/security/console.apps/run_init

# fix symlink pointing to buildroot
ln -sf /sbin/load_policy $RPM_BUILD_ROOT%{_sbindir}/load_policy

%py_comp $RPM_BUILD_ROOT%{py_sitedir}/sepolicy
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/sepolicy
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{_datadir}/system-config-selinux
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/system-config-selinux
%py_postclean

# empty versions of short-code locales
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{af_ZA,bn_BD,cs_CZ,es_ES,eu_ES,fa_IR,hr_HR,it_IT,ja_JP,lt_LT,lv_LV,ms_MY,ru_RU,si_LK,ta_IN,uk_UA,vi_VN,zh_CN.GB2312,zh_TW.Big5}

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

%post mcstrans
/sbin/chkconfig --add mcstrans
%service mcstrans restart

%preun mcstrans
if [ "$1" = "0" ]; then
	%service mcstrans stop
	/sbin/chkconfig --del mcstrans
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_bindir}/audit2allow
%attr(755,root,root) %{_bindir}/audit2why
%attr(755,root,root) %{_bindir}/chcat
%attr(4755,root,root) %{_bindir}/newrole
%attr(755,root,root) %{_bindir}/sandbox
%attr(755,root,root) %{_bindir}/secon
%attr(755,root,root) %{_bindir}/semodule_*
%attr(755,root,root) %{_bindir}/sepolgen-ifgen
%attr(755,root,root) %{_bindir}/sepolgen-ifgen-attr-helper
%attr(755,root,root) /sbin/fixfiles
%attr(755,root,root) /sbin/load_policy
%attr(755,root,root) /sbin/restorecon
%attr(755,root,root) /sbin/setfiles
%attr(755,root,root) %{_sbindir}/genhomedircon
%attr(755,root,root) %{_sbindir}/load_policy
%attr(755,root,root) %{_sbindir}/open_init_pty
%attr(755,root,root) %{_sbindir}/run_init
%attr(755,root,root) %{_sbindir}/semanage
%attr(755,root,root) %{_sbindir}/semodule
%attr(755,root,root) %{_sbindir}/setsebool
%attr(755,root,root) %{_sbindir}/sestatus
%attr(755,root,root) %{_sbindir}/seunshare
%dir %{_libdir}/selinux/hll
%attr(755,root,root) %{_libdir}/selinux/hll/pp
%{py_sitescriptdir}/seobject.py[co]
#%attr(754,root,root) /etc/rc.d/init.d/sandbox
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/newrole
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/run_init
%config(missingok) /etc/security/console.apps/run_init
%config(noreplace) %verify(not md5 mtime size) /etc/sestatus.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/sandbox
%dir %{_datadir}/sandbox
%attr(755,root,root) %{_datadir}/sandbox/*.sh
%attr(755,root,root) %{_datadir}/sandbox/start
%{_mandir}/man1/audit2allow.1*
%{_mandir}/man1/audit2why.1*
%{_mandir}/man1/newrole.1*
%{_mandir}/man1/secon.1*
%{_mandir}/man5/sandbox.5*
%{_mandir}/man5/selinux_config.5*
%{_mandir}/man5/sestatus.conf.5*
%{_mandir}/man8/chcat.8*
%{_mandir}/man8/genhomedircon.8*
%{_mandir}/man8/fixfiles.8*
%{_mandir}/man8/load_policy.8*
%{_mandir}/man8/open_init_pty.8*
%{_mandir}/man8/restorecon.8*
%{_mandir}/man8/run_init.8*
%{_mandir}/man8/sandbox.8*
%{_mandir}/man8/semanage*.8*
%{_mandir}/man8/semodule*.8*
%{_mandir}/man8/sestatus.8*
%{_mandir}/man8/setfiles.8*
%{_mandir}/man8/setsebool.8*
%{_mandir}/man8/seunshare.8*

%if %{with restorecond}
%files restorecond
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/restorecond
%attr(754,root,root) /etc/rc.d/init.d/restorecond
%{systemdunitdir}/restorecond.service
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/selinux/restorecond.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/selinux/restorecond_user.conf
%{_mandir}/man8/restorecond.8*
%{_sysconfdir}/xdg/autostart/restorecond.desktop
%{_datadir}/dbus-1/services/org.selinux.Restorecond.service
%endif

%files sepolicy
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sepolgen
%attr(755,root,root) %{_bindir}/sepolicy
%dir %{py_sitedir}/sepolicy
%attr(755,root,root) %{py_sitedir}/sepolicy/_policy.so
%{py_sitedir}/sepolicy/*.py[co]
%{py_sitedir}/sepolicy/sepolicy.glade
%dir %{py_sitedir}/sepolicy/help
%{py_sitedir}/sepolicy/help/__init__.py[co]
%{py_sitedir}/sepolicy/help/*.png
%{py_sitedir}/sepolicy/help/*.txt
%dir %{py_sitedir}/sepolicy/templates
%{py_sitedir}/sepolicy/templates/*.py[co]
%{py_sitedir}/sepolicy-1.1-py*.egg-info
%{_mandir}/man8/sepolgen.8*
%{_mandir}/man8/sepolicy*.8*
/etc/dbus-1/system.d/org.selinux.conf
%{_datadir}/dbus-1/system-services/org.selinux.service
%{_datadir}/polkit-1/actions/org.selinux.policy

%files mcstrans
%defattr(644,root,root,755)
%doc mcstrans/{ChangeLog,TODO}
%attr(755,root,root) /sbin/mcstransd
%attr(754,root,root) /etc/rc.d/init.d/mcstrans
%{systemdunitdir}/mcstrans.service
%{_mandir}/man8/mcs.8*
%{_mandir}/man8/mcstransd.8*
%{_mandir}/man8/setrans.conf.8*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/semanage
%{bash_compdir}/sepolicy
%{bash_compdir}/setsebool

%files -n system-config-selinux
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/system-config-selinux
%{_datadir}/system-config-selinux
%{_datadir}/polkit-1/actions/org.selinux.config.policy
%{_iconsdir}/hicolor/*/apps/sepolicy.png
%{_iconsdir}/hicolor/24x24/apps/system-config-selinux.png
%{_pixmapsdir}/sepolicy.png
%{_pixmapsdir}/system-config-selinux.png
%{_mandir}/man8/selinux-polgengui.8*
%{_mandir}/man8/system-config-selinux.8*
