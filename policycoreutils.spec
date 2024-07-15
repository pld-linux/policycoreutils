Summary:	SELinux policy core utilities
Summary(pl.UTF-8):	Podstawowe narzędzia dla polityki SELinux
Name:		policycoreutils
Version:	3.7
Release:	1
# some parts strictly v2, some v2+
License:	GPL v2
Group:		Applications/System
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b240edcce09c9909db8287cc7fdf1dc0
Source1:	%{name}-newrole.pamd
Source2:	%{name}-run_init.pamd
URL:		https://github.com/SELinuxProject/selinux/wiki
BuildRequires:	audit-libs-devel
BuildRequires:	gettext-tools
BuildRequires:	libselinux-devel >= 3.7
BuildRequires:	libsemanage-devel >= 3.7
BuildRequires:	libsepol-devel >= 3.7
BuildRequires:	pam-devel
BuildRequires:	rpm-build >= 4.6
Requires:	libselinux >= 3.7
Requires:	libsemanage >= 3.7
Requires:	libsepol >= 3.7
Obsoletes:	policycoreutils-tools-perl < 2.2
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
to switch roles, and run_init to run /etc/rc.d/init.d scripts in the
proper context.

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

%package -n bash-completion-%{name}
Summary:	Bash completion for policycoreutils commands
Summary(pl.UTF-8):	Bashowe dopełnianie składni poleceń policycoreutils
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2
BuildArch:	noarch

%description -n bash-completion-%{name}
Bash completion for policycoreutils commands.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie składni poleceń policycoreutils.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,security/console.apps}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBEXECDIR=%{_libexecdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/newrole
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/run_init
:> $RPM_BUILD_ROOT/etc/security/console.apps/run_init

# empty versions of short-code locales
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{bn_BD,lt_LT,lv_LV,si_LK,vi_VN,zh_CN.GB2312,zh_TW.Big5}
# not supported by glibc (as of 2.30)
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{aln,bal,ilo}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(4755,root,root) %{_bindir}/newrole
%attr(755,root,root) %{_bindir}/secon
%attr(755,root,root) %{_bindir}/sestatus
%attr(755,root,root) /sbin/restorecon
%attr(755,root,root) /sbin/restorecon_xattr
%attr(755,root,root) /sbin/setfiles
%attr(755,root,root) %{_sbindir}/fixfiles
%attr(755,root,root) %{_sbindir}/genhomedircon
%attr(755,root,root) %{_sbindir}/load_policy
%attr(755,root,root) %{_sbindir}/open_init_pty
%attr(755,root,root) %{_sbindir}/run_init
%attr(755,root,root) %{_sbindir}/semodule
%attr(755,root,root) %{_sbindir}/setsebool
%attr(755,root,root) %{_sbindir}/sestatus
%dir %{_libexecdir}/selinux/hll
%attr(755,root,root) %{_libexecdir}/selinux/hll/pp
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/newrole
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/run_init
%config(missingok) /etc/security/console.apps/run_init
%config(noreplace) %verify(not md5 mtime size) /etc/sestatus.conf
%{_mandir}/man1/newrole.1*
%{_mandir}/man1/secon.1*
%{_mandir}/man5/selinux_config.5*
%{_mandir}/man5/sestatus.conf.5*
%{_mandir}/man8/genhomedircon.8*
%{_mandir}/man8/fixfiles.8*
%{_mandir}/man8/load_policy.8*
%{_mandir}/man8/open_init_pty.8*
%{_mandir}/man8/restorecon.8*
%{_mandir}/man8/restorecon_xattr.8*
%{_mandir}/man8/run_init.8*
%{_mandir}/man8/semodule.8*
%{_mandir}/man8/sestatus.8*
%{_mandir}/man8/setfiles.8*
%{_mandir}/man8/setsebool.8*

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/setsebool
